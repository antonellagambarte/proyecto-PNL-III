"""Esquemas de datos de los agentes y estado del grafo.
"""

from typing import Annotated, Any, Literal, TypedDict

from langchain_core.messages import AnyMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field


class Fragmento(BaseModel):
    """Un fragmento del manual que devolvió la búsqueda.

    Lo arma el código con el resultado de la búsqueda, no el LLM. Por eso el verificador
    compara la respuesta del tutor contra el texto real del chunk.
    """

    id: str = Field(description="Identificador del fragmento, por ejemplo pba2019-c04-s4.3-002.")
    cita: str = Field(description="Cita armada desde los metadatos: capítulo, sección y páginas.")
    texto: str = Field(description="Texto del chunk que devolvió la búsqueda.")


class RespuestaTutor(BaseModel):
    """La respuesta que redacta el tutor."""

    respuesta: str = Field(description="Explicación en castellano, basada solo en los fragmentos del manual.")
    opcion_elegida: str | None = Field(
        default=None,
        description="Texto exacto de la opción elegida, si la pregunta tiene opciones. Si no, vacío.",
    )
    citas: list[str] = Field(
        default_factory=list,
        description="Identificadores de los fragmentos que respaldan la respuesta. Vacía si el manual no la respalda.",
    )


class Veredicto(BaseModel):
    """La decisión del verificador sobre la respuesta del tutor."""

    # Lista cerrada: el código decide el camino según este valor, así que el LLM no puede
    # inventar otro camino.
    veredicto: Literal["aprobada", "corregir", "buscar_mas"] = Field(
        description="aprobada si la respuesta está respaldada por los fragmentos, corregir si dice algo que "
        "los fragmentos no respaldan, buscar_mas si a los fragmentos les falta información.",
    )
    motivo: str = Field(description="Qué está mal o qué falta. Si está aprobada, por qué.")
    consulta_sugerida: str | None = Field(
        default=None,
        description="Solo con buscar_mas: otra consulta para buscar en el manual.",
    )


class Estado(TypedDict):
    """Lo que se lleva de un paso al otro del grafo. Cada nodo lee lo que necesita y escribe su resultado."""

    pregunta: str
    opciones: list[str] | None
    fragmentos: list[Fragmento]
    borrador: RespuestaTutor | None
    veredicto: Veredicto | None
    vueltas: int
    # Conversación del tutor (sus búsquedas, los fragmentos y su respuesta). Si el verificador
    # no aprueba, en la vuelta siguiente el tutor la continúa.
    mensajes_tutor: list[AnyMessage]
    # Bitácora de lo que hizo cada agente en cada vuelta, para revisar y auditar. Ningún agente
    # la lee. Empieza vacía en cada pregunta y cada nodo le suma su entrada.
    registro: list[dict]
    # Charla de la sesión: cada pregunta con la respuesta que recibió quien estudia. El
    # checkpointer la guarda entre preguntas y add_messages suma los mensajes nuevos al final.
    conversacion: Annotated[list[AnyMessage], add_messages]
    # Lo que ven los agentes de esa charla: el resumen de lo más viejo y los mensajes recientes.
    conversacion_resumida: list[AnyMessage]
    # Donde langmem guarda el resumen, para extenderlo en la pregunta siguiente.
    context: dict[str, Any]
