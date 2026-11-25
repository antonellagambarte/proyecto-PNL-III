"""Tests de la evaluación de la búsqueda. Usan metadatos inventados, no el manual real."""

from src.rag.evaluators.busqueda import a_paginas


def test_a_paginas():
    """Un fragmento de dos páginas cuenta como la relevante, y las páginas no se repiten."""
    metadatos = [
        {"pagina_inicio": 56, "pagina_fin": 57},    # toca la 57, que es la relevante
        {"pagina_inicio": 57, "pagina_fin": 57},    # repite la 57
        {"pagina_inicio": 102, "pagina_fin": 103},  # no toca ninguna relevante: cuenta como la 102
    ]
    assert a_paginas(metadatos, {57}) == [57, 102]
