"""La variante «modelo solo»: las preguntas con opciones, directo al LLM, sin el manual.

Sirve para saber cuánto ya sabe el modelo sin buscar nada, y así ver qué aporta el sistema.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from src.rag.evaluators.sistema import acierta

SISTEMA = ("Respondé preguntas del examen teórico de la licencia de conducir de la Provincia de Buenos Aires. "
           "Elegí una opción y copiá su texto exacto.")


class Eleccion(BaseModel):
    """La opción que eligió el modelo."""

    opcion: str = Field(description="Texto exacto de la opción elegida.")


def mensajes(pregunta: dict) -> list:
    """La pregunta y sus opciones, sin ningún fragmento del manual."""
    opciones = "\n".join(f"- {opcion}" for opcion in pregunta["opciones"])
    return [SystemMessage(SISTEMA), HumanMessage(f"{pregunta['pregunta']}\n\nOpciones:\n{opciones}")]


def responder_sin_manual(llm, preguntas: list[dict]) -> list[dict]:
    """Una fila por pregunta con opciones: qué eligió el modelo y si acertó. Si una llamada falla, cuenta como error."""
    con_opciones = [p for p in preguntas if p["opciones"]]
    elegidas = llm.with_structured_output(Eleccion).batch(
        [mensajes(p) for p in con_opciones], config={"max_concurrency": 5}, return_exceptions=True)
    filas = []
    for pregunta, eleccion in zip(con_opciones, elegidas):
        opcion = None if isinstance(eleccion, Exception) else eleccion.opcion
        filas.append({"id": pregunta["id"], "opcion_elegida": opcion, "acierta": bool(acierta(pregunta, opcion)),
                      "error": type(eleccion).__name__ if isinstance(eleccion, Exception) else None})
    return filas
