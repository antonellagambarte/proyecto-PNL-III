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


def test_tamanos():
    """Prueba cada cantidad de candidatos y de fragmentos, y deja el buscador como estaba."""
    from src.rag.evaluators.busqueda import probar_tamanos

    class BuscadorFalso:
        """Con 15 candidatos o más, la página 57 sale primera. Con menos, sale cuarta."""
        k_candidatos = 30

        def buscar(self, consulta, k):
            paginas = [57, 1, 2, 3, 4] if self.k_candidatos >= 15 else [1, 2, 3, 57, 4]
            return [{"metadata": {"pagina_inicio": p, "pagina_fin": p}} for p in paginas[:k]]

    buscador = BuscadorFalso()
    tabla = probar_tamanos(buscador, [{"pregunta": "¿Velocidad en avenidas?", "paginas": [57]}], [10, 15], [3, 4])
    recall = {(fila.candidatos, fila.fragmentos): fila.recall for fila in tabla.itertuples()}
    assert recall == {(10, 3): 0.0, (10, 4): 1.0, (15, 3): 1.0, (15, 4): 1.0}
    assert buscador.k_candidatos == 30
