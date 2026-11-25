"""La memoria de la conversación: lo que se habló antes en la misma sesión.

La charla se guarda con el checkpointer de LangGraph y, cuando se alarga, se resume con
SummarizationNode de langmem.
"""

from langchain_core.messages import AIMessage, AnyMessage, HumanMessage, SystemMessage
from langmem.short_term import SummarizationNode

from src.agents.esquemas import Estado


def crear_memoria(llm, config: dict) -> SummarizationNode:
    """Nodo que prepara la charla anterior para los agentes: si pasa de max_tokens, la resume."""
    memoria = config["memoria"]
    return SummarizationNode(
        model=llm,
        max_tokens=memoria["max_tokens"],
        max_summary_tokens=memoria["max_tokens_resumen"],
        input_messages_key="conversacion",
        output_messages_key="conversacion_resumida",
    )


def recordar(estado: Estado) -> dict:
    """Nodo final: suma a la charla la pregunta y la respuesta que recibió quien estudia."""
    return {"conversacion": [HumanMessage(estado["pregunta"]), AIMessage(estado["borrador"].respuesta)]}


def formatear_conversacion(mensajes: list[AnyMessage]) -> str:
    """Arma el texto de la charla anterior para los agentes, entre marcas, para que la lean como datos."""
    renglones = []
    for mensaje in mensajes:
        if isinstance(mensaje, SystemMessage):
            renglones.append(mensaje.content)  # el resumen de la charla hasta ese momento
        elif isinstance(mensaje, HumanMessage):
            renglones.append(f"Estudiante: {mensaje.content}")
        else:
            renglones.append(f"Tutor: {mensaje.content}")
    return "<conversacion>\n" + "\n".join(renglones) + "\n</conversacion>"
