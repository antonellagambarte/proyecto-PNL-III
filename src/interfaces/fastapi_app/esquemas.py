"""Qué recibe y qué devuelve la API."""

from pydantic import BaseModel, Field


class Consulta(BaseModel):
    """Lo que manda quien estudia."""

    pregunta: str = Field(min_length=1, description="La pregunta, escrita como le salga a quien estudia.")
    opciones: list[str] | None = Field(default=None, description="Las opciones, si la pregunta es de opción múltiple.")
    sesion: str | None = Field(
        default=None, description="El id de la charla. Si no viene, la API crea uno y lo devuelve para la próxima pregunta."
    )


class Metricas(BaseModel):
    """Cuánto tardó y cuánto gastó la consulta."""

    segundos: float
    tokens_entrada: int
    tokens_salida: int


class Respuesta(BaseModel):
    """Lo que recibe quien estudia."""

    respuesta: str
    opcion_elegida: str | None
    citas: list[str]
    veredicto: str = Field(description="El último veredicto del verificador: aprobada, corregir o buscar_mas.")
    vueltas: int
    pasos: list[dict] = Field(description="Qué buscó y respondió el tutor y qué dijo el verificador, en orden.")
    sesion: str
    metricas: Metricas
