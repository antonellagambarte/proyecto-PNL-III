"""Texto con el que se indexa cada chunk, igual para las dos búsquedas."""


def texto_para_indexar(chunk: dict) -> str:
    """Antepone el título de la sección al texto del chunk.

    Así los chunks del medio de una sección, que no nombran su tema, quedan asociados
    a él. El chunk guardado no cambia: esto se usa solo para armar los índices.
    """
    metadatos = chunk["metadata"]
    # La introducción de un capítulo no tiene sección: se usa el título del capítulo.
    titulo = metadatos["titulo_seccion"] or metadatos["titulo_capitulo"]
    return f"{titulo}. {chunk['texto']}"
