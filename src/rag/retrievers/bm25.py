"""Búsqueda por palabras (BM25) sobre los chunks del manual.

Adaptado del índice BM25 del código de la cátedra. Lo que cambia: las palabras se
comparan sin tildes, los códigos como «A.1.1» quedan enteros, cada chunk se indexa
con el título de su sección y el índice se guarda en disco.
"""

import json
import logging
import re
import unicodedata
from pathlib import Path

from rank_bm25 import BM25Okapi

from src.rag.retrievers.texto import texto_para_indexar

log = logging.getLogger(__name__)

# Una palabra o un número. Los puntos internos se conservan, para que códigos como
# «A.1.1» o números de ley como «24.449» queden en una sola pieza.
TOKEN = re.compile(r"[a-z0-9]+(?:\.[a-z0-9]+)*")


def sin_tildes(texto: str) -> str:
    """Pasa a minúsculas y saca las tildes. «Máxima» queda «maxima»."""
    separado = unicodedata.normalize("NFD", texto.lower())
    return "".join(letra for letra in separado if not unicodedata.combining(letra))


def tokenizar(texto: str) -> list[str]:
    """Parte un texto en palabras, en minúsculas y sin tildes."""
    return TOKEN.findall(sin_tildes(texto))


class IndiceBM25:
    """Índice BM25 sobre los chunks. Guarda el id de cada chunk y sus palabras."""

    def __init__(self, ids: list[str], tokens: list[list[str]]):
        if not ids or len(ids) != len(tokens):
            raise ValueError("Se necesita un id por cada lista de palabras, y al menos un chunk.")
        self.ids = ids
        self.tokens = tokens
        self.bm25 = BM25Okapi(tokens)

    @classmethod
    def desde_chunks(cls, chunks: list[dict]) -> "IndiceBM25":
        """Arma el índice a partir de los chunks, con el título de la sección incluido."""
        indice = cls([c["id"] for c in chunks], [tokenizar(texto_para_indexar(c)) for c in chunks])
        log.info("Índice BM25 armado con %d chunks", len(chunks))
        return indice

    def guardar(self, ruta: Path) -> None:
        """Guarda los ids y las palabras en JSON. El índice se rearma al cargarlo."""
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with ruta.open("w", encoding="utf-8") as archivo:
            json.dump({"ids": self.ids, "tokens": self.tokens}, archivo, ensure_ascii=False)

    @classmethod
    def cargar(cls, ruta: Path) -> "IndiceBM25":
        """Lee el índice guardado. Con unos cientos de chunks, rearmarlo es instantáneo."""
        with Path(ruta).open(encoding="utf-8") as archivo:
            datos = json.load(archivo)
        return cls(datos["ids"], datos["tokens"])

    def buscar(self, consulta: str, k: int) -> list[tuple[str, float]]:
        """Devuelve hasta k chunks con su puntaje, del más al menos relevante.

        Solo devuelve chunks que comparten alguna palabra con la consulta (puntaje mayor a 0).
        """
        palabras = tokenizar(consulta)
        if not palabras:
            return []
        puntajes = self.bm25.get_scores(palabras)
        orden = sorted(range(len(self.ids)), key=lambda i: puntajes[i], reverse=True)
        return [(self.ids[i], float(puntajes[i])) for i in orden[:k] if puntajes[i] > 0]
