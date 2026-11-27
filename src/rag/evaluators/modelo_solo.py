"""La variante «modelo solo»: las preguntas directo al LLM, sin el manual.

Sirve para saber cuánto ya sabe el modelo sin buscar nada, y así ver qué aporta el sistema.
Las de opciones se miden por la opción elegida y las libres, por el dato clave.
"""

from langchain_core.messages import HumanMessage, SystemMessage
from pydantic import BaseModel, Field

from src.rag.evaluators.sistema import acierta

SISTEMA = ("Respondé preguntas del examen teórico de la licencia de conducir de la Provincia de Buenos Aires. "
           "Elegí una opción y copiá su texto exacto.")
SISTEMA_LIBRE = ("Respondé en pocas líneas preguntas sobre el examen teórico de la licencia de conducir "
                 "de la Provincia de Buenos Aires.")


class Eleccion(BaseModel):
    """La opción que eligió el modelo."""

    opcion: str = Field(description="Texto exacto de la opción elegida.")


def mensajes(pregunta: dict) -> list:
    """La pregunta (y sus opciones, si tiene), sin ningún fragmento del manual."""
    if not pregunta["opciones"]:
        return [SystemMessage(SISTEMA_LIBRE), HumanMessage(pregunta["pregunta"])]
    opciones = "\n".join(f"- {opcion}" for opcion in pregunta["opciones"])
    return [SystemMessage(SISTEMA), HumanMessage(f"{pregunta['pregunta']}\n\nOpciones:\n{opciones}")]


def fila(pregunta: dict, resultado, opcion: str | None, texto: str) -> dict:
    """Lo que eligió o respondió el modelo y si acertó. Si la llamada falló, cuenta como error y no como acierto."""
    error = type(resultado).__name__ if isinstance(resultado, Exception) else None
    return {"id": pregunta["id"], "forma": "opciones" if pregunta["opciones"] else "libre",
            "opcion_elegida": opcion, "respuesta": texto,
            "acierta": False if error else acierta(pregunta, opcion, texto), "error": error}


def responder_sin_manual(llm, preguntas: list[dict]) -> list[dict]:
    """Una fila por pregunta: qué respondió el modelo y si acertó."""
    config = {"max_concurrency": 5}
    con_opciones = [p for p in preguntas if p["opciones"]]
    libres = [p for p in preguntas if not p["opciones"]]
    elegidas = llm.with_structured_output(Eleccion).batch([mensajes(p) for p in con_opciones], config=config, return_exceptions=True)
    respuestas = llm.batch([mensajes(p) for p in libres], config=config, return_exceptions=True) if libres else []
    filas = [fila(p, e, None if isinstance(e, Exception) else e.opcion, "") for p, e in zip(con_opciones, elegidas)]
    filas += [fila(p, r, None, "" if isinstance(r, Exception) else r.text) for p, r in zip(libres, respuestas)]
    orden = {p["id"]: i for i, p in enumerate(preguntas)}
    return sorted(filas, key=lambda f: orden[f["id"]])
