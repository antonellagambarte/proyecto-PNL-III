"""Tests de la búsqueda. Usan chunks chicos inventados y no cargan los modelos.

La búsqueda por significado y el re-ranker se reemplazan por objetos falsos que
devuelven resultados fijos. Así se prueba la lógica propia sin descargar modelos.
"""

import pytest

from src.rag.retrievers.bm25 import IndiceBM25, tokenizar
from src.rag.retrievers.citas import formatear_cita
from src.rag.retrievers.hibrida import BuscadorHibrido, rrf


def chunk(id_, seccion, texto):
    """Arma un chunk de prueba con los mismos campos que los del manual."""
    return {
        "id": id_,
        "texto": texto,
        "metadata": {
            "documento": "Manual del conductor PBA",
            "edicion": "2019",
            "capitulo": int(seccion.split(".")[0]),
            "titulo_capitulo": "CAPÍTULO DE PRUEBA",
            "seccion": seccion,
            "titulo_seccion": "SECCIÓN DE PRUEBA",
            "pagina_inicio": 10,
            "pagina_fin": 10,
            "fuente": "manual.pdf",
            "origen": "pdf",
        },
    }


CHUNKS = [
    chunk("a", "4.3", "La velocidad máxima en avenidas es de 60 km/h."),
    chunk("b", "6.10", "Antes de estacionar, verifique que no haya un cartel que lo prohíba."),
    chunk("c", "1.2", "La clase A.1.1 se puede obtener desde los 16 años."),
    chunk("d", "4.4", "El cinturón de seguridad es obligatorio para todos los ocupantes."),
]


class DensaFalsa:
    """Reemplaza la búsqueda por significado: devuelve siempre la misma lista."""

    def __init__(self, resultados):
        self.resultados = resultados

    def buscar(self, consulta, k):
        return self.resultados[:k]


class RerankerFalso:
    """Reemplaza al re-ranker: le da a cada id un puntaje fijo."""

    def __init__(self, puntajes):
        self.puntajes = puntajes

    def reordenar(self, consulta, candidatos):
        salida = [(id_, self.puntajes[id_]) for id_, _ in candidatos]
        return sorted(salida, key=lambda par: par[1], reverse=True)


def test_tokenizar():
    """Saca tildes y mayúsculas, y deja enteros los códigos y los números de ley."""
    assert tokenizar("¿Qué dice la Ley 24.449 sobre la clase A.1.1?") == [
        "que", "dice", "la", "ley", "24.449", "sobre", "la", "clase", "a.1.1",
    ]


def test_bm25_buscar():
    """Devuelve las posiciones de mejor a peor, solo de chunks con alguna palabra en común."""
    indice = IndiceBM25.desde_chunks(CHUNKS)
    resultados = indice.buscar("velocidad máxima y estacionar", k=4)
    # El chunk a tiene dos palabras de la consulta y el b una. El c y el d, ninguna.
    assert [posicion for posicion, _ in resultados] == [0, 1]


def test_bm25_sin_coincidencias():
    """Si ninguna palabra de la consulta está en los chunks, no devuelve nada."""
    indice = IndiceBM25.desde_chunks(CHUNKS)
    assert indice.buscar("neumáticos", k=4) == []


def test_bm25_guardar_y_cargar(tmp_path):
    """El índice guardado en JSON y vuelto a cargar da los mismos resultados."""
    indice = IndiceBM25.desde_chunks(CHUNKS)
    ruta = tmp_path / "bm25.json"
    indice.guardar(ruta)
    cargado = IndiceBM25.cargar(ruta)
    consulta = "velocidad máxima y estacionar"
    assert cargado.ids == indice.ids
    assert cargado.buscar(consulta, k=4) == indice.buscar(consulta, k=4)


def test_rrf():
    """Un id que está en las dos listas le gana a uno que está primero en una sola."""
    assert rrf(["A", "B"], ["C", "B"])[0] == "B"


def test_limite_por_seccion():
    """De una misma sección quedan como mucho dos chunks. El lugar libre lo ocupa otra sección."""
    chunks = [chunk(f"4.3-{n}", "4.3", "texto") for n in (1, 2, 3)] + [chunk("6.6-1", "6.6", "texto")]
    buscador = BuscadorHibrido(None, None, None, chunks, k_candidatos=30, max_por_seccion=2)
    reordenados = [("4.3-1", 0.9), ("4.3-2", 0.8), ("4.3-3", 0.7), ("6.6-1", 0.6)]
    elegidos = buscador.limitar_por_seccion(reordenados, k=3)
    assert [id_ for id_, _ in elegidos] == ["4.3-1", "4.3-2", "6.6-1"]


def test_buscar():
    """Devuelve los k mejores según el re-ranker, cada uno con su cita. Con k fuera de rango da error."""
    # BM25 encuentra a y b. La búsqueda por significado (falsa) encuentra d y a.
    # El re-ranker (falso) pone b primero, aunque en la fusión a estaba arriba.
    buscador = BuscadorHibrido(
        bm25=IndiceBM25.desde_chunks(CHUNKS),
        densa=DensaFalsa([("d", 0.8), ("a", 0.7)]),
        reranker=RerankerFalso({"a": 0.2, "b": 0.9, "c": 0.5, "d": 0.1}),
        chunks=CHUNKS,
        k_candidatos=3,
        max_por_seccion=2,
    )
    resultados = buscador.buscar("velocidad máxima y estacionar", k=2)
    assert [r["id"] for r in resultados] == ["b", "a"]
    assert set(resultados[0]) == {"id", "texto", "metadata", "cita", "puntaje"}
    assert resultados[0]["cita"].startswith("Manual del conductor PBA 2019, cap. 6")
    with pytest.raises(ValueError):
        buscador.buscar("velocidad", k=4)


def test_cita():
    """La cita lleva capítulo, sección y páginas. La introducción de un capítulo no tiene sección."""
    metadata = {
        "documento": "Manual del conductor PBA",
        "edicion": "2019",
        "capitulo": 7,
        "titulo_capitulo": "FUNCIONAMIENTO DEL VEHÍCULO",
        "seccion": "7.3",
        "titulo_seccion": "LA VERIFICACIÓN TÉCNICA VEHICULAR (VTV)",
        "pagina_inicio": 115,
        "pagina_fin": 116,
    }
    assert formatear_cita(metadata) == (
        "Manual del conductor PBA 2019, cap. 7 (Funcionamiento del vehículo), "
        "secc. 7.3 (La verificación técnica vehicular (VTV)), p. 115–116"
    )
    introduccion = metadata | {
        "capitulo": 6,
        "titulo_capitulo": "LAS REGLAS DE SU SEGURIDAD",
        "seccion": None,
        "titulo_seccion": None,
        "pagina_inicio": 90,
        "pagina_fin": 90,
    }
    assert formatear_cita(introduccion) == (
        "Manual del conductor PBA 2019, cap. 6 (Las reglas de su seguridad), introducción del capítulo, p. 90"
    )
