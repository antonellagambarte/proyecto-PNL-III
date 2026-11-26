"""Control de salida: revisa la respuesta aprobada antes de mostrarla y de guardarla en la charla.

Tres controles, en código y no en el prompt: sin citas válidas no se muestra, la opción elegida
tiene que estar entre las opciones, y se sacan los enlaces y las imágenes.
"""

import re

from src.agents.esquemas import RespuestaTutor

SIN_INFORMACION = "No encontré en el manual información que permita responder esta pregunta."
ENLACE_QUITADO = "(enlace quitado)"

# Imagen en markdown: ![texto](dirección). Se saca entera.
IMAGEN = re.compile(r"!\[[^\]]*\]\([^)]*\)")
# Enlace en markdown: [texto](dirección). Queda el texto.
ENLACE = re.compile(r"\[([^\]]*)\]\([^)]*\)")
# Dirección suelta, sin el signo de puntuación que la cierra.
DIRECCION = re.compile(r"(https?://|www\.)\S*[^\s.,;:!?)»\"']", re.IGNORECASE)

# Lo que se anota de cada cambio. Los primeros tres son para mirar (warning).
PARA_MIRAR = ("enlaces_quitados", "opcion_inexistente", "citas_inventadas")


def sin_enlaces(texto: str) -> str:
    """Saca las imágenes, deja el texto de los enlaces y reemplaza las direcciones sueltas por un aviso."""
    texto = IMAGEN.sub("", texto)
    texto = ENLACE.sub(r"\1", texto)
    return DIRECCION.sub(ENLACE_QUITADO, texto)


def igual(a: str, b: str) -> bool:
    """Si dos opciones son la misma, sin contar mayúsculas, espacios de más ni el punto final."""
    normalizar = lambda texto: " ".join(texto.split()).strip(" .").casefold()
    return normalizar(a) == normalizar(b)


def controlar_salida(borrador: RespuestaTutor, opciones: list[str] | None,
                     encontrados: set[str]) -> tuple[RespuestaTutor, list[str]]:
    """Aplica los tres controles. Devuelve la respuesta que se muestra y la lista de lo que cambió."""
    cambios = []
    respuesta = sin_enlaces(borrador.respuesta)
    if respuesta != borrador.respuesta:
        cambios.append("enlaces_quitados")

    # Si la opción es una de las dadas, queda con su texto oficial. Si no, se descarta.
    opcion = borrador.opcion_elegida
    if opcion and opciones:
        opcion = next((o for o in opciones if igual(o, borrador.opcion_elegida)), None)
        if opcion is None:
            cambios.append("opcion_inexistente")

    # Sin al menos una cita a un fragmento encontrado, la respuesta no tiene respaldo: no se muestra.
    citas = [id_ for id_ in borrador.citas if id_ in encontrados]
    if not citas:
        cambios.append("citas_inventadas" if borrador.citas else "sin_citas")
        return RespuestaTutor(respuesta=SIN_INFORMACION, opcion_elegida=None, citas=[]), cambios
    return RespuestaTutor(respuesta=respuesta, opcion_elegida=opcion, citas=citas), cambios
