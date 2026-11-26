"""El tutor: decide qué buscar en el manual y redacta la respuesta con citas.

Es un agente con una sola herramienta (buscar_en_manual), armado con create_agent de
LangChain. Si el verificador no aprueba la respuesta, el tutor sigue su misma conversación
(con sus búsquedas, los fragmentos y su respuesta) y recibe como mensaje nuevo el motivo
y, si hay, una consulta sugerida para buscar de nuevo.
"""

from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, ToolMessage

from src.agents.esquemas import Estado, Fragmento, RespuestaTutor
from src.agents.memoria import formatear_conversacion
from src.agents.prompts import TUTOR


def mensajes_para_tutor(estado: Estado) -> list[AnyMessage]:
    """Arma lo que recibe el tutor en cada vuelta.

    En la primera, la charla anterior de la sesión (si hay), la pregunta y las opciones. En
    las siguientes, su conversación anterior más un mensaje con lo que observó el verificador.
    """
    veredicto = estado["veredicto"]
    if veredicto is None:
        partes = []
        if estado["conversacion_resumida"]:
            partes.append("Charla anterior:\n" + formatear_conversacion(estado["conversacion_resumida"]))
        partes.append(f"Pregunta: {estado['pregunta']}")
        if estado["opciones"]:
            partes.append("Opciones:\n" + "\n".join(f"- {opcion}" for opcion in estado["opciones"]))
        return [HumanMessage("\n\n".join(partes))]
    observacion = f"Tu respuesta no se aprobó. Motivo: {veredicto.motivo}"
    if veredicto.consulta_sugerida:
        observacion += f"\n\nBuscá con esta consulta: {veredicto.consulta_sugerida}"
    observacion += "\n\nEscribí de nuevo la respuesta completa, para quien estudia, sin mencionar esta revisión."
    return estado["mensajes_tutor"] + [HumanMessage(observacion)]


def juntar_fragmentos(anteriores: list[Fragmento], nuevos: list[Fragmento]) -> list[Fragmento]:
    """Suma los fragmentos nuevos a los de vueltas anteriores, sin repetir.

    Se conservan los anteriores porque el verificador revisa contra todo lo encontrado y
    las citas pueden venir de cualquier vuelta.
    """
    juntos = list(anteriores)
    vistos = {f.id for f in anteriores}
    for fragmento in nuevos:
        if fragmento.id not in vistos:
            juntos.append(fragmento)
            vistos.add(fragmento.id)
    return juntos


class Tutor:
    """Nodo del grafo que corre el agente tutor."""

    def __init__(self, llm, herramienta, max_busquedas: int):
        self.agente = create_agent(
            model=llm,
            tools=[herramienta],
            system_prompt=TUTOR,
            response_format=RespuestaTutor,
            # Tope de búsquedas por vuelta: si lo pasa, la herramienta no se ejecuta y el
            # tutor tiene que responder con lo que ya encontró.
            middleware=[ToolCallLimitMiddleware(run_limit=max_busquedas)],
        )

    def __call__(self, estado: Estado) -> dict:
        mensajes = mensajes_para_tutor(estado)
        resultado = self.agente.invoke({"messages": mensajes})
        # Solo los mensajes de esta vuelta: los anteriores ya se procesaron.
        de_esta_vuelta = resultado["messages"][len(mensajes):]
        # Los fragmentos vienen aparte del texto, en el artifact de cada respuesta de la herramienta.
        nuevos = [f for m in de_esta_vuelta if isinstance(m, ToolMessage) and m.artifact for f in m.artifact]
        # Las consultas que se buscaron, para el registro. Las que frenó el tope de búsquedas no cuentan.
        buscadas = {m.tool_call_id for m in de_esta_vuelta if isinstance(m, ToolMessage) and m.status == "success"}
        consultas = [
            llamada["args"].get("consulta", "")
            for m in de_esta_vuelta if isinstance(m, AIMessage)
            for llamada in m.tool_calls if llamada["name"] == "buscar_en_manual" and llamada["id"] in buscadas
        ]
        borrador = resultado["structured_response"]
        vuelta = estado["vueltas"] + 1
        return {
            "borrador": borrador,
            "fragmentos": juntar_fragmentos(estado["fragmentos"], nuevos),
            "vueltas": vuelta,
            "mensajes_tutor": resultado["messages"],
            "registro": estado["registro"] + [{
                "agente": "tutor", "vuelta": vuelta, "consultas": consultas,
                "fragmentos": [f.id for f in nuevos], "respuesta": borrador.respuesta,
                "opcion_elegida": borrador.opcion_elegida, "citas": borrador.citas,
            }],
        }
