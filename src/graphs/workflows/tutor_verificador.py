"""El grafo tutor → verificador con LangGraph.

Primero se prepara la charla anterior de la sesión. Después el tutor responde, el
verificador revisa y, según el veredicto, el código decide el camino: terminar, volver al
tutor o, si se acabaron las vueltas, avisar que no hay respaldo en el manual. Ningún LLM
elige el camino. Al final, la pregunta y la respuesta se suman a la charla de la sesión.
"""

from uuid import uuid4

from langchain_core.callbacks import get_usage_metadata_callback
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph import END, START, StateGraph

from src.agents.esquemas import Estado, RespuestaTutor
from src.agents.memoria import crear_memoria, recordar
from src.agents.tutor import Tutor
from src.agents.verificador import Verificador
from src.common.config import resolver_ruta
from src.common.telemetry.auditoria import Auditoria
from src.policies.entrada import revisar_entrada
from src.policies.salida import PARA_MIRAR, controlar_salida
from src.rag.retrievers.hibrida import crear_buscador
from src.runtime.providers.llm import crear_llm
from src.tools.builtin.buscar_en_manual import crear_buscar_en_manual

SIN_RESPALDO = "No encontré respaldo suficiente en el manual para responder esta pregunta con seguridad."


def sin_respaldo(estado: Estado) -> dict:
    """Nodo final cuando se acabaron las vueltas sin aprobación: reemplaza el borrador por el aviso."""
    return {"borrador": RespuestaTutor(respuesta=SIN_RESPALDO, opcion_elegida=None, citas=[])}


def control_salida(estado: Estado) -> dict:
    """Nodo después de la aprobación: aplica el control de salida antes de mostrar y guardar la respuesta."""
    encontrados = {fragmento.id for fragmento in estado["fragmentos"]}
    borrador, cambios = controlar_salida(estado["borrador"], estado["opciones"], encontrados)
    return {"borrador": borrador,
            "registro": estado["registro"] + [{"agente": "control_salida", "vuelta": estado["vueltas"], "cambios": cambios}]}


def crear_grafo(tutor, verificador, memoria, max_vueltas: int):
    """Arma el grafo con los dos agentes y la memoria. El ruteo después del verificador lo decide el código.

    El checkpointer guarda el estado de cada sesión, así la pregunta siguiente recibe la charla anterior.
    """

    def rutear(estado: Estado) -> str:
        if estado["veredicto"].veredicto == "aprobada":
            return "fin"
        if estado["vueltas"] < max_vueltas:
            return "tutor"
        return "sin_respaldo"

    grafo = StateGraph(Estado)
    grafo.add_node("memoria", memoria)
    grafo.add_node("tutor", tutor)
    grafo.add_node("verificador", verificador)
    grafo.add_node("control_salida", control_salida)
    grafo.add_node("sin_respaldo", sin_respaldo)
    grafo.add_node("recordar", recordar)
    grafo.add_edge(START, "memoria")
    grafo.add_edge("memoria", "tutor")
    grafo.add_edge("tutor", "verificador")
    grafo.add_conditional_edges("verificador", rutear, {"fin": "control_salida", "tutor": "tutor", "sin_respaldo": "sin_respaldo"})
    grafo.add_edge("control_salida", "recordar")
    grafo.add_edge("sin_respaldo", "recordar")
    grafo.add_edge("recordar", END)
    return grafo.compile(checkpointer=InMemorySaver())


def armar_respuesta(estado: Estado) -> dict:
    """La respuesta final: texto, opción, citas, cómo terminó y el registro de cada vuelta.

    Las citas las arma el código con los metadatos de los fragmentos, no el modelo. Si el
    tutor nombra un id que no está entre los fragmentos recuperados, no se cita.
    """
    borrador = estado["borrador"]
    cita_de = {f.id: f.cita for f in estado["fragmentos"]}
    return {
        "respuesta": borrador.respuesta,
        "opcion_elegida": borrador.opcion_elegida,
        # Dos fragmentos de la misma página dan la misma cita: se muestra una sola vez.
        "citas": list(dict.fromkeys(cita_de[id_] for id_ in borrador.citas if id_ in cita_de)),
        "veredicto": estado["veredicto"].veredicto,
        "vueltas": estado["vueltas"],
        "registro": estado["registro"],
    }


def entrada(pregunta: str, opciones: list[str] | None) -> dict:
    """Lo que empieza de cero en cada pregunta. La charla de la sesión no se toca: la trae el checkpointer."""
    return {"pregunta": pregunta, "opciones": opciones, "fragmentos": [], "borrador": None,
            "veredicto": None, "vueltas": 0, "mensajes_tutor": [], "registro": []}


def rechazada(motivo: str, control: str) -> dict:
    """La respuesta cuando el control de entrada frena la pregunta: no se llama al LLM."""
    return {"respuesta": motivo, "opcion_elegida": None, "citas": [], "veredicto": "rechazada", "vueltas": 0,
            "registro": [{"agente": "control_entrada", "control": control, "motivo": motivo}], "tokens": {}}


def evento_de_paso(nodo: str, cambios: dict) -> dict | None:
    """Lo que se anota en la auditoría cuando termina un paso del grafo: cantidades y decisiones, sin textos.

    memoria y recordar no se anotan: preparan y guardan la charla, no deciden nada.
    """
    if nodo == "tutor":
        paso = cambios["registro"][-1]
        return {"evento": "tutor", "vuelta": cambios["vueltas"], "busquedas": len(paso.get("consultas", [])),
                "fragmentos": len(paso.get("fragmentos", [])), "citas": len(paso.get("citas", [])),
                "eligio_opcion": bool(paso.get("opcion_elegida"))}
    if nodo == "verificador":
        return {"evento": "verificador", "vuelta": cambios["registro"][-1]["vuelta"], "veredicto": cambios["veredicto"].veredicto}
    if nodo == "control_salida":
        lista = cambios["registro"][-1]["cambios"]
        return {"evento": "salida", "gravedad": "warning" if set(lista) & set(PARA_MIRAR) else "info", "cambios": lista}
    if nodo == "sin_respaldo":
        return {"evento": "sin_respaldo"}
    return None


class TutorVerificador:
    """El sistema completo: carga una vez los modelos y la búsqueda, y responde preguntas."""

    def __init__(self, config: dict):
        self.max_caracteres = config["entrada"]["max_caracteres"]
        self.auditoria = Auditoria(resolver_ruta(config["rutas"]["logs"]))
        llm = crear_llm(config)
        herramienta = crear_buscar_en_manual(crear_buscador(config), config["busqueda"]["k_fragmentos"])
        agentes = config["agentes"]
        self.grafo = crear_grafo(
            Tutor(llm, herramienta, agentes["max_busquedas"]),
            Verificador(llm),
            crear_memoria(llm, config),
            agentes["max_vueltas"],
        )

    def responder(self, pregunta: str, opciones: list[str] | None = None, sesion: str | None = None) -> dict:
        """Responde una pregunta, con o sin opciones. Suma los tokens que usaron todas las llamadas al LLM.

        Con el mismo id de sesión, el sistema recuerda la charla anterior. Sin id, cada pregunta
        es independiente (así se evalúa). Antes pasa por el control de entrada: una pregunta
        rechazada no llega a los agentes ni queda en la charla.

        Cada paso queda en la auditoría en el momento en que termina: por eso el grafo se recorre
        con stream, que avisa al final de cada nodo, en lugar de invoke.
        """
        sesion = sesion or str(uuid4())
        auditoria = self.auditoria.empezar(uuid4().hex[:12], sesion)
        revision = revisar_entrada(pregunta, opciones, self.max_caracteres)
        # Un ataque frenado o algo escondido que se sacó es para mirar: warning.
        auditoria.registrar("entrada", "warning" if revision.motivo or revision.invisibles else "info",
                            resultado="rechazada" if revision.motivo else "aceptada",
                            control=revision.control, invisibles_quitados=revision.invisibles)
        if revision.motivo:
            auditoria.registrar("fin", resultado="rechazada", segundos_total=auditoria.total(),
                                tokens_entrada=0, tokens_salida=0)
            return rechazada(revision.motivo, revision.control)
        config = {"configurable": {"thread_id": sesion}}
        try:
            with get_usage_metadata_callback() as uso:
                for paso in self.grafo.stream(entrada(revision.pregunta, revision.opciones), config, stream_mode="updates"):
                    for nodo, cambios in paso.items():
                        evento = evento_de_paso(nodo, cambios)
                        if evento:
                            auditoria.registrar(**evento)
        except Exception as error:
            # Solo el tipo de error: el mensaje puede traer datos internos.
            auditoria.registrar("error", "error", tipo=type(error).__name__, segundos_total=auditoria.total())
            raise
        respuesta = armar_respuesta(self.grafo.get_state(config).values)
        respuesta["tokens"] = uso.usage_metadata
        if revision.invisibles:
            # Que también se vea en los pasos que el control de entrada sacó algo escondido.
            respuesta["registro"] = [{"agente": "control_entrada", "invisibles": revision.invisibles}] + respuesta["registro"]
        auditoria.registrar(
            "fin", resultado="aprobada" if respuesta["veredicto"] == "aprobada" else "sin_respaldo",
            vueltas=respuesta["vueltas"], citas=len(respuesta["citas"]), segundos_total=auditoria.total(),
            tokens_entrada=sum(u["input_tokens"] for u in uso.usage_metadata.values()),
            tokens_salida=sum(u["output_tokens"] for u in uso.usage_metadata.values()),
        )
        return respuesta
