"""Evaluación de la búsqueda con métricas de recuperación.

Adaptado de la evaluación de la búsqueda del código de la cátedra. Lo que cambia: se
comparan cuatro variantes en lugar de dos (antes y después del re-ranking), los
fragmentos se convierten en páginas del manual y se mide cuánto tarda cada búsqueda.
"""

import logging
import time

import pandas as pd

from src.rag.evaluators.metricas import mrr, ndcg_at_k, precision_at_k, recall_at_k

log = logging.getLogger(__name__)


def a_paginas(metadatos: list[dict], relevantes: set[int]) -> list[int]:
    """Convierte fragmentos en páginas del manual, en el mismo orden y sin repetir.

    Un fragmento puede ocupar más de una página. Si toca una página relevante, cuenta
    como esa página. Si no, cuenta como la primera que ocupa.
    """
    paginas = []
    for metadata in metadatos:
        ocupa = range(metadata["pagina_inicio"], metadata["pagina_fin"] + 1)
        paginas.append(next((p for p in ocupa if p in relevantes), metadata["pagina_inicio"]))
    return list(dict.fromkeys(paginas))


def buscar_variantes(buscador, consulta: str, k: int) -> dict[str, tuple[list[str], float]]:
    """Los ids de los k primeros fragmentos de cada variante y los segundos que tardó cada una."""
    busquedas = {
        "bm25": lambda: [buscador.bm25.ids[i] for i, _ in buscador.bm25.buscar(consulta, k)],
        "embeddings": lambda: [id_ for id_, _ in buscador.densa.buscar(consulta, k)],
        "hibrida": lambda: buscador.candidatos(consulta)[:k],
        "hibrida_reranking": lambda: [r["id"] for r in buscador.buscar(consulta, k)],
    }
    resultados = {}
    for variante, buscar in busquedas.items():
        inicio = time.perf_counter()
        ids = buscar()
        resultados[variante] = (ids, time.perf_counter() - inicio)
    return resultados


def evaluar(buscador, preguntas: list[dict], ks: tuple[int, ...]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Calcula las métricas de cada variante para cada pregunta, y sus promedios por variante y k.

    k cuenta fragmentos, como los que recibe el tutor: se toman los k primeros y recién
    ahí se pasan a páginas.
    """
    if not preguntas or not ks or min(ks) <= 0:
        raise ValueError("Se necesitan preguntas y valores de k mayores que 0.")
    filas = []
    for pregunta in preguntas:
        relevantes = set(pregunta["paginas"])
        for variante, (ids, segundos) in buscar_variantes(buscador, pregunta["pregunta"], max(ks)).items():
            metadatos = [buscador.chunks[id_]["metadata"] for id_ in ids]
            for k in ks:
                paginas = a_paginas(metadatos[:k], relevantes)
                filas.append({
                    "id": pregunta["id"],
                    "eleccion": pregunta["eleccion"],
                    "variante": variante,
                    "k": k,
                    "precision": precision_at_k(paginas, relevantes, k),
                    "recall": recall_at_k(paginas, relevantes, k),
                    "ndcg": ndcg_at_k(paginas, relevantes, k),
                    "mrr": mrr(paginas, relevantes),
                    "segundos": segundos,
                })
    por_pregunta = pd.DataFrame(filas)
    promedios = por_pregunta.groupby(["variante", "k"], sort=False).mean(numeric_only=True).reset_index()
    return por_pregunta, promedios


def tiempos(por_pregunta: pd.DataFrame) -> pd.DataFrame:
    """Segundos por búsqueda de cada variante: la mediana (p50) y el percentil 95 (p95)."""
    una_por_busqueda = por_pregunta.drop_duplicates(["id", "variante"])
    resumen = una_por_busqueda.groupby("variante", sort=False)["segundos"].quantile([0.5, 0.95]).unstack()
    resumen.columns = ["p50", "p95"]
    return resumen.reset_index()
