"""Búsqueda híbrida: palabras (BM25) más significado (vectores), fusión RRF y re-ranking.

Adaptado del pipeline híbrido del código de la cátedra: la fusión y el re-ranking son
los mismos. Lo que cambia: la búsqueda por significado usa Chroma en lugar de Pinecone,
los modelos son multilingües y cada fragmento sale con su cita.
"""

import logging

from src.common.config import resolver_ruta
from src.common.jsonl import leer_jsonl
from src.rag.retrievers.bm25 import IndiceBM25
from src.rag.retrievers.citas import formatear_cita
from src.rag.retrievers.densa import IndiceDenso, cargar_modelo
from src.rag.retrievers.reranker import Reranker

log = logging.getLogger(__name__)


def rrf(*listas: list[str], k: float = 60.0) -> list[str]:
    """Fusiona varias listas ordenadas de ids (Reciprocal Rank Fusion).

    Cada id suma 1 / (k + puesto) por cada lista en la que aparece, donde el primero de
    la lista tiene puesto 1. Así los que están arriba en varias listas suben.
    """
    puntajes: dict[str, float] = {}
    for lista in listas:
        for posicion, id_ in enumerate(lista):
            puntajes[id_] = puntajes.get(id_, 0.0) + 1.0 / (k + posicion + 1.0)
    ordenados = sorted(puntajes.items(), key=lambda par: par[1], reverse=True)
    return [id_ for id_, _ in ordenados]


class BuscadorHibrido:
    """Junta las dos búsquedas, las fusiona y reordena los candidatos con el re-ranker."""

    def __init__(self, bm25, densa, reranker, chunks: list[dict], k_candidatos: int, max_por_seccion: int):
        self.bm25 = bm25
        self.densa = densa
        self.reranker = reranker
        self.chunks = {c["id"]: c for c in chunks}
        self.k_candidatos = k_candidatos
        self.max_por_seccion = max_por_seccion

    def candidatos(self, consulta: str) -> list[str]:
        """Los k_candidatos ids que salen de fusionar las dos búsquedas."""
        # BM25 devuelve la posición de cada chunk: se traduce a su id para fusionar.
        por_palabras = [self.bm25.ids[i] for i, _ in self.bm25.buscar(consulta, self.k_candidatos)]
        por_significado = [id_ for id_, _ in self.densa.buscar(consulta, self.k_candidatos)]
        return rrf(por_palabras, por_significado)[: self.k_candidatos]

    def limitar_por_seccion(self, reordenados: list[tuple[str, float]], k: int) -> list[tuple[str, float]]:
        """Toma los k mejores, con como mucho max_por_seccion chunks de una misma sección.

        Se aplica después del re-ranking: así el re-ranker ve todos los candidatos y solo
        se descartan los chunks repetidos de una sección que ya tiene sus dos mejores.
        """
        elegidos, por_seccion = [], {}
        for id_, puntaje in reordenados:
            metadatos = self.chunks[id_]["metadata"]
            seccion = (metadatos["capitulo"], metadatos["seccion"])
            if por_seccion.get(seccion, 0) >= self.max_por_seccion:
                continue
            por_seccion[seccion] = por_seccion.get(seccion, 0) + 1
            elegidos.append((id_, puntaje))
            if len(elegidos) == k:
                break
        return elegidos

    def buscar(self, consulta: str, k: int) -> list[dict]:
        """Devuelve los k chunks más relevantes, con su texto, sus metadatos, su cita y el puntaje del re-ranker."""
        if not 0 < k <= self.k_candidatos:
            raise ValueError(f"k tiene que estar entre 1 y {self.k_candidatos}.")
        ids = self.candidatos(consulta)
        reordenados = self.reranker.reordenar(consulta, [(id_, self.chunks[id_]["texto"]) for id_ in ids])
        return [
            {
                "id": id_,
                "texto": self.chunks[id_]["texto"],
                "metadata": self.chunks[id_]["metadata"],
                "cita": formatear_cita(self.chunks[id_]["metadata"]),
                "puntaje": puntaje,
            }
            for id_, puntaje in self.limitar_por_seccion(reordenados, k)
        ]


def crear_buscador(config: dict) -> BuscadorHibrido:
    """Arma el buscador con los índices ya guardados y los modelos de la configuración."""
    rutas, busqueda = config["rutas"], config["busqueda"]
    indices = resolver_ruta(rutas["indices"])
    chunks = leer_jsonl(resolver_ruta(rutas["procesados"]) / "chunks.jsonl")
    return BuscadorHibrido(
        bm25=IndiceBM25.cargar(indices / "bm25.json"),
        densa=IndiceDenso(indices / "chroma", cargar_modelo(busqueda["modelo_embeddings"])),
        reranker=Reranker(busqueda["modelo_reranking"]),
        chunks=chunks,
        k_candidatos=busqueda["k_candidatos"],
        max_por_seccion=busqueda["max_por_seccion"],
    )
