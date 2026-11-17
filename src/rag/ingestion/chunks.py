"""Chunking: corta cada sección del manual en fragmentos con solapamiento y metadatos.

Adaptado del chunking del código de la cátedra. Igual que ahí, un token es una
palabra o un número, y cada chunk es una ventana de tokens que se solapa con la
anterior. Lo que cambia: los chunks no cruzan de una sección a otra, y cada uno
guarda en qué páginas está su texto.
"""

import logging
import re

log = logging.getLogger(__name__)

DOCUMENTO = "Manual del conductor PBA"
EDICION = "2019"

# Un token es una palabra (con tildes) o un número.
TOKEN = re.compile(r"[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9]+")
ESPACIOS = re.compile(r"\s+")


def ventanas(texto: str, max_tokens: int, solapamiento: int) -> list[tuple[int, int]]:
    """Devuelve dónde empieza y termina cada chunk dentro del texto (posiciones de caracteres)."""
    if max_tokens <= 0 or not 0 <= solapamiento < max_tokens:
        raise ValueError("Se necesita max_tokens > 0 y 0 <= solapamiento < max_tokens.")
    tokens = list(TOKEN.finditer(texto))
    tramos = []
    inicio = 0
    while inicio < len(tokens):
        fin = min(inicio + max_tokens, len(tokens))
        izquierda = 0 if inicio == 0 else tokens[inicio].start()
        derecha = tokens[fin].start() if fin < len(tokens) else len(texto)
        tramos.append((izquierda, derecha))
        if fin == len(tokens):
            break
        inicio = fin - solapamiento
    return tramos


def chunks_de_seccion(seccion: dict, max_tokens: int, solapamiento: int, fuente: str) -> list[dict]:
    """Corta una sección en chunks y le pone a cada uno su id y sus metadatos."""
    # Se une el texto de todas las páginas, anotando dónde empieza cada una.
    partes, inicios = [], []
    posicion = 0
    for pagina in seccion["paginas"]:
        texto_pagina = ESPACIOS.sub(" ", pagina["texto"]).strip()
        inicios.append((posicion, pagina["pagina"]))
        partes.append(texto_pagina)
        posicion += len(texto_pagina) + 1
    texto = " ".join(partes)
    origen_por_pagina = {p["pagina"]: p.get("origen", "pdf") for p in seccion["paginas"]}

    # La introducción de un capítulo no tiene número de sección.
    nombre_seccion = f"s{seccion['seccion']}" if seccion["seccion"] else "intro"
    chunks = []
    for i, (izquierda, derecha) in enumerate(ventanas(texto, max_tokens, solapamiento), start=1):
        inicio_chunk = _pagina_en(izquierda, inicios)
        fin_chunk = _pagina_en(derecha - 1, inicios)
        # Si el chunk incluye texto de alguna página transcripta a mano, se marca.
        transcripto = any(
            origen == "transcripcion_manual"
            for pagina, origen in origen_por_pagina.items()
            if inicio_chunk <= pagina <= fin_chunk
        )
        chunks.append({
            "id": f"pba{EDICION}-c{seccion['capitulo']:02d}-{nombre_seccion}-{i:03d}",
            "texto": texto[izquierda:derecha].strip(),
            "metadata": {
                "documento": DOCUMENTO,
                "edicion": EDICION,
                "capitulo": seccion["capitulo"],
                "titulo_capitulo": seccion["titulo_capitulo"],
                "seccion": seccion["seccion"],
                "titulo_seccion": seccion["titulo_seccion"],
                "pagina_inicio": inicio_chunk,
                "pagina_fin": fin_chunk,
                "fuente": fuente,
                "origen": "transcripcion_manual" if transcripto else "pdf",
            },
        })
    return chunks


def _pagina_en(posicion: int, inicios: list[tuple[int, int]]) -> int:
    """Devuelve la página que contiene una posición del texto unido."""
    pagina = inicios[0][1]
    for inicio, numero in inicios:
        if inicio <= posicion:
            pagina = numero
    return pagina


def armar_chunks(secciones: list[dict], max_tokens: int, solapamiento: int, fuente: str) -> list[dict]:
    """Corta todas las secciones. Ningún chunk mezcla texto de dos secciones."""
    chunks = []
    for seccion in secciones:
        chunks.extend(chunks_de_seccion(seccion, max_tokens, solapamiento, fuente))
    log.info(
        "Se armaron %d chunks de %d secciones (máximo %d tokens, solapamiento %d)",
        len(chunks), len(secciones), max_tokens, solapamiento,
    )
    return chunks
