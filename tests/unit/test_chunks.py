"""Tests del chunking. Usan secciones chicas inventadas, no el manual real."""

import pytest

from src.rag.ingestion.chunks import armar_chunks, ventanas


def seccion(numero, paginas, capitulo=1):
    """Arma una sección de prueba. paginas es una lista de (número de página, texto, origen)."""
    return {
        "capitulo": capitulo,
        "titulo_capitulo": "EL CONDUCTOR",
        "seccion": numero,
        "titulo_seccion": f"SECCIÓN {numero}",
        "paginas": [{"pagina": p, "texto": t, "origen": o} for p, t, o in paginas],
    }


def palabras(desde, hasta):
    """Texto de prueba: 'p1 p2 p3 ...'. Cada palabra es un token."""
    return " ".join(f"p{i}" for i in range(desde, hasta + 1))


def test_solapamiento():
    """Cada chunk repite las últimas palabras del anterior."""
    texto = palabras(1, 10)
    tramos = [texto[a:b].strip() for a, b in ventanas(texto, max_tokens=4, solapamiento=2)]
    assert tramos == ["p1 p2 p3 p4", "p3 p4 p5 p6", "p5 p6 p7 p8", "p7 p8 p9 p10"]


def test_solapamiento_invalido():
    """Si el solapamiento no es menor que el tamaño del chunk, da un error."""
    with pytest.raises(ValueError):
        ventanas("p1 p2 p3", max_tokens=4, solapamiento=4)


def test_no_cruza_secciones():
    """Un chunk nunca mezcla texto de dos secciones."""
    secciones = [
        seccion("1.1", [(4, palabras(1, 5), "pdf")]),
        seccion("1.2", [(4, palabras(6, 10), "pdf")]),
    ]
    chunks = armar_chunks(secciones, max_tokens=200, solapamiento=60, fuente="manual.pdf")
    assert [c["texto"] for c in chunks] == [palabras(1, 5), palabras(6, 10)]
    assert [c["metadata"]["seccion"] for c in chunks] == ["1.1", "1.2"]


def test_paginas():
    """Un chunk que cruza de página guarda la página de inicio y la de fin."""
    secciones = [seccion("1.1", [(4, palabras(1, 3), "pdf"), (5, palabras(4, 6), "pdf")])]
    chunks = armar_chunks(secciones, max_tokens=200, solapamiento=60, fuente="manual.pdf")
    assert (chunks[0]["metadata"]["pagina_inicio"], chunks[0]["metadata"]["pagina_fin"]) == (4, 5)


def test_origen():
    """Los chunks con texto transcripto a mano quedan marcados. Los demás dicen 'pdf'."""
    secciones = [
        seccion("4.3", [(56, palabras(1, 6), "pdf")]),
        seccion("4.4", [(58, palabras(7, 12), "transcripcion_manual")]),
    ]
    chunks = armar_chunks(secciones, max_tokens=200, solapamiento=60, fuente="manual.pdf")
    assert [c["metadata"]["origen"] for c in chunks] == ["pdf", "transcripcion_manual"]


def test_ids():
    """Los ids indican capítulo, sección y número de chunk. La introducción no tiene sección."""
    secciones = [
        seccion("6.2", [(95, palabras(1, 3), "pdf")], capitulo=6),
        seccion(None, [(90, palabras(1, 3), "pdf")], capitulo=6),
    ]
    chunks = armar_chunks(secciones, max_tokens=200, solapamiento=60, fuente="manual.pdf")
    assert [c["id"] for c in chunks] == ["pba2019-c06-s6.2-001", "pba2019-c06-intro-001"]
