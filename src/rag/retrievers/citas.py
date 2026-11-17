"""Citas de los fragmentos del manual, armadas por el código desde los metadatos.

Las arma el código y no el modelo, para que no pueda inventar páginas ni secciones.
"""

import re

ENTRE_PARENTESIS = re.compile(r"\(([^)]*)\)")


def a_oracion(titulo: str) -> str:
    """Pasa un título de MAYÚSCULAS a formato oración. Las siglas entre paréntesis se conservan.

    «LA VERIFICACIÓN TÉCNICA VEHICULAR (VTV)» queda «La verificación técnica vehicular (VTV)».
    """
    texto = titulo.capitalize()
    return ENTRE_PARENTESIS.sub(lambda m: f"({m.group(1).upper()})", texto)


def formatear_cita(metadata: dict) -> str:
    """Arma la cita de un fragmento: documento, capítulo, sección y páginas."""
    partes = [
        f"{metadata['documento']} {metadata['edicion']}",
        f"cap. {metadata['capitulo']} ({a_oracion(metadata['titulo_capitulo'])})",
    ]
    if metadata["seccion"]:
        partes.append(f"secc. {metadata['seccion']} ({a_oracion(metadata['titulo_seccion'])})")
    else:
        partes.append("introducción del capítulo")
    inicio, fin = metadata["pagina_inicio"], metadata["pagina_fin"]
    partes.append(f"p. {inicio}" if inicio == fin else f"p. {inicio}–{fin}")
    return ", ".join(partes)
