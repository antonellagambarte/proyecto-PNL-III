"""Evaluación de la búsqueda con métricas de recuperación.

Adaptado de la evaluación de la búsqueda del código de la cátedra. Lo que cambia: se
comparan cuatro variantes en lugar de dos (antes y después del re-ranking), los
fragmentos se convierten en páginas del manual y se mide cuánto tarda cada búsqueda.
Además, si los fragmentos traen las frases de la respuesta: Non-LLM Context Recall, adaptado de RAGAS.
"""

import logging
import re
import time
import unicodedata

import pandas as pd

from src.rag.evaluators.metricas import mrr, ndcg_at_k, precision_at_k, recall_at_k

log = logging.getLogger(__name__)

# Cada frase de evidencia empieza con su página, «p. 57: » o «p. 56–57: », y puede saltear texto con «[...]».
PAGINA_DE_EVIDENCIA = re.compile(r"^p\. \d+(?:–\d+)?: ")
SALTEO = re.compile(r"\[(?:\.\.\.|…)\]")


def comparable(texto: str) -> str:
    """El texto en minúsculas, sin tildes ni signos: solo letras y números separados por un espacio."""
    sin_tildes = unicodedata.normalize("NFKD", texto.lower())
    sin_tildes = "".join(c for c in sin_tildes if not unicodedata.combining(c))
    return " ".join(re.findall(r"[a-z0-9]+", sin_tildes))


def partes(evidencia: str) -> list[str]:
    """Lo que hay que buscar de una frase de evidencia, sin la página del principio.

    Si la frase saltea texto con «[...]», cada parte se busca por separado, pero siguen siendo una sola evidencia.
    """
    sin_pagina = PAGINA_DE_EVIDENCIA.sub("", evidencia)
    return [parte for parte in (comparable(p) for p in SALTEO.split(sin_pagina)) if parte]


def esta(evidencia: list[str], textos: list[str]) -> bool:
    """Si todas las partes de la evidencia aparecen, tal cual, en alguno de los textos."""
    return all(any(parte in texto for texto in textos) for parte in evidencia)


def context_recall(evidencias: list[list[str]], textos: list[str]) -> float | None:
    """Non-LLM Context Recall, adaptado de RAGAS: qué parte de las evidencias traen los fragmentos.

    RAGAS compara con un parecido de texto. Acá la evidencia tiene que estar entera. None si no hay evidencias.
    """
    if not evidencias:
        return None
    return sum(esta(evidencia, textos) for evidencia in evidencias) / len(evidencias)


def revisar_evidencias(preguntas: list[dict], fragmentos: list[str]) -> pd.DataFrame:
    """Qué frases de evidencia se pueden medir: las que están, tal cual, en algún fragmento del manual.

    Las que no, no se encontrarían nunca (por ejemplo, si la lectura del PDF mezcló el texto) y quedan afuera.
    """
    return pd.DataFrame([{"id": pregunta["id"], "evidencia": evidencia, "buscable": esta(partes(evidencia), fragmentos)}
                         for pregunta in preguntas for evidencia in pregunta.get("evidencia", [])])


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


def corpus(buscador) -> dict[str, str]:
    """El texto de cada fragmento del manual, listo para buscar frases con comparable."""
    return {id_: comparable(chunk["texto"]) for id_, chunk in buscador.chunks.items()}


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
    ahí se pasan a páginas. El context recall usa solo las evidencias que se pueden medir.
    """
    if not preguntas or not ks or min(ks) <= 0:
        raise ValueError("Se necesitan preguntas y valores de k mayores que 0.")
    textos = corpus(buscador)
    filas = []
    for pregunta in preguntas:
        relevantes = set(pregunta["paginas"])
        evidencias = [partes(e) for e in pregunta.get("evidencia", [])]
        evidencias = [e for e in evidencias if esta(e, list(textos.values()))]
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
                    "context_recall": context_recall(evidencias, [textos[id_] for id_ in ids[:k]]),
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


def probar_tamanos(buscador, preguntas: list[dict], candidatos: list[int], fragmentos: list[int]) -> pd.DataFrame:
    """Acierto y tiempo de la búsqueda completa con distintos tamaños, para elegir los de config.yaml.

    candidatos son los que ordena el re-ranker (k_candidatos) y fragmentos los que recibe el
    tutor en cada búsqueda (k_fragmentos). Para cada cantidad de candidatos se busca una vez
    cada pregunta y se mide el acierto con cada cantidad de fragmentos: los primeros k de la
    lista son los mismos que daría buscar con k. Al terminar, el buscador vuelve a su valor.
    """
    if min(candidatos) < max(fragmentos):
        raise ValueError("Cada cantidad de candidatos tiene que alcanzar para la mayor cantidad de fragmentos.")
    original = buscador.k_candidatos
    filas = []
    try:
        for cantidad in candidatos:
            buscador.k_candidatos = cantidad
            for pregunta in preguntas:
                relevantes = set(pregunta["paginas"])
                inicio = time.perf_counter()
                metadatos = [r["metadata"] for r in buscador.buscar(pregunta["pregunta"], max(fragmentos))]
                segundos = time.perf_counter() - inicio
                for k in fragmentos:
                    paginas = a_paginas(metadatos[:k], relevantes)
                    filas.append({"candidatos": cantidad, "fragmentos": k,
                                  "recall": recall_at_k(paginas, relevantes, k), "segundos": segundos})
    finally:
        buscador.k_candidatos = original
    return (pd.DataFrame(filas).groupby(["candidatos", "fragmentos"])
            .agg(recall=("recall", "mean"),
                 segundos_p50=("segundos", lambda s: s.quantile(0.5)),
                 segundos_p95=("segundos", lambda s: s.quantile(0.95)))
            .reset_index())
