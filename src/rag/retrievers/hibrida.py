"""Búsqueda híbrida: palabras (BM25) más significado (vectores), fusión RRF y re-ranking.

Adaptado del pipeline híbrido del código de la cátedra: la fórmula de fusión y el
re-ranking con un cross-encoder son los mismos. Lo que cambia: la búsqueda por
significado usa Chroma en lugar de Pinecone, y los modelos son multilingües.
"""

import logging

from sentence_transformers import CrossEncoder

from src.common.config import resolver_ruta
from src.common.jsonl import leer_jsonl
from src.rag.retrievers.bm25 import IndiceBM25
from src.rag.retrievers.citas import formatear_cita
from src.rag.retrievers.densa import IndiceDenso, cargar_modelo

log = logging.getLogger(__name__)


def rrf(*listas: list[str], k: float = 60.0) -> list[str]:
    """Fusiona varias listas ordenadas de ids (Reciprocal Rank Fusion).

    Cada id suma 1 / (k + posición) por cada lista en la que aparece, así que los que
    están arriba en varias listas suben. Misma fórmula que el código de la cátedra.
    """
    puntajes: dict[str, float] = {}
    for lista in listas:
        for posicion, id_ in enumerate(lista, start=1):
            puntajes[id_] = puntajes.get(id_, 0.0) + 1.0 / (k + posicion)
    return sorted(puntajes, key=puntajes.get, reverse=True)


class BuscadorHibrido:
    """Junta las dos búsquedas, las fusiona y reordena los candidatos con el re-ranker."""

    def __init__(self, bm25, densa, reranker, chunks: list[dict], k_candidatos: int):
        self.bm25 = bm25
        self.densa = densa
        self.reranker = reranker
        self.chunks = {c["id"]: c for c in chunks}
        self.k_candidatos = k_candidatos

    def candidatos(self, consulta: str) -> list[str]:
        """Los k_candidatos ids que salen de fusionar las dos búsquedas."""
        por_palabras = [id_ for id_, _ in self.bm25.buscar(consulta, self.k_candidatos)]
        por_significado = [id_ for id_, _ in self.densa.buscar(consulta, self.k_candidatos)]
        return rrf(por_palabras, por_significado)[: self.k_candidatos]

    def buscar(self, consulta: str, k: int) -> list[dict]:
        """Devuelve los k chunks más relevantes, con su texto, sus metadatos, su cita y el puntaje del re-ranker."""
        if not 0 < k <= self.k_candidatos:
            raise ValueError(f"k tiene que estar entre 1 y {self.k_candidatos}.")
        ids = self.candidatos(consulta)
        if not ids:
            return []
        # El re-ranker lee la pregunta junto con el texto completo de cada candidato.
        puntajes = self.reranker.predict([(consulta, self.chunks[id_]["texto"]) for id_ in ids])
        mejores = sorted(zip(ids, puntajes), key=lambda par: par[1], reverse=True)[:k]
        return [
            {
                "id": id_,
                "texto": self.chunks[id_]["texto"],
                "metadata": self.chunks[id_]["metadata"],
                "cita": formatear_cita(self.chunks[id_]["metadata"]),
                "puntaje": float(puntaje),
            }
            for id_, puntaje in mejores
        ]


def crear_buscador(config: dict) -> BuscadorHibrido:
    """Arma el buscador con los índices ya guardados y los modelos de la configuración."""
    rutas, busqueda = config["rutas"], config["busqueda"]
    indices = resolver_ruta(rutas["indices"])
    chunks = leer_jsonl(resolver_ruta(rutas["procesados"]) / "chunks.jsonl")
    return BuscadorHibrido(
        bm25=IndiceBM25.cargar(indices / "bm25.json"),
        densa=IndiceDenso(indices / "chroma", cargar_modelo(busqueda["modelo_embeddings"])),
        reranker=CrossEncoder(busqueda["modelo_reranking"]),
        chunks=chunks,
        k_candidatos=busqueda["k_candidatos"],
    )
