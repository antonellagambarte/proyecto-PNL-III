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
from src.rag.retrievers.hibrida import crear_buscador
from src.runtime.providers.llm import crear_llm
from src.tools.builtin.buscar_en_manual import crear_buscar_en_manual

SIN_RESPALDO = "No encontré respaldo suficiente en el manual para responder esta pregunta con seguridad."


def sin_respaldo(estado: Estado) -> dict:
    """Nodo final cuando se acabaron las vueltas sin aprobación: reemplaza el borrador por el aviso."""
    return {"borrador": RespuestaTutor(respuesta=SIN_RESPALDO, opcion_elegida=None, citas=[])}


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
    grafo.add_node("sin_respaldo", sin_respaldo)
    grafo.add_node("recordar", recordar)
    grafo.add_edge(START, "memoria")
    grafo.add_edge("memoria", "tutor")
    grafo.add_edge("tutor", "verificador")
    grafo.add_conditional_edges("verificador", rutear, {"fin": "recordar", "tutor": "tutor", "sin_respaldo": "sin_respaldo"})
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
        "citas": [cita_de[id_] for id_ in borrador.citas if id_ in cita_de],
        "veredicto": estado["veredicto"].veredicto,
        "vueltas": estado["vueltas"],
        "registro": estado["registro"],
    }


def entrada(pregunta: str, opciones: list[str] | None) -> dict:
    """Lo que empieza de cero en cada pregunta. La charla de la sesión no se toca: la trae el checkpointer."""
    return {"pregunta": pregunta, "opciones": opciones, "fragmentos": [], "borrador": None,
            "veredicto": None, "vueltas": 0, "mensajes_tutor": [], "registro": []}


class TutorVerificador:
    """El sistema completo: carga una vez los modelos y la búsqueda, y responde preguntas."""

    def __init__(self, config: dict):
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
        es independiente (así se evalúa).
        """
        config = {"configurable": {"thread_id": sesion or str(uuid4())}}
        with get_usage_metadata_callback() as uso:
            final = self.grafo.invoke(entrada(pregunta, opciones), config)
        respuesta = armar_respuesta(final)
        respuesta["tokens"] = uso.usage_metadata
        return respuesta
