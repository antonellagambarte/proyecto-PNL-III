"""Búsqueda por significado: los vectores de los chunks guardados en Chroma.

Reemplaza la búsqueda vectorial en Pinecone del código de la cátedra. Chroma corre
local, sin cuenta ni key. Los vectores los calcula multilingual-e5-small, que pide
marcar cada texto como pregunta («query: ») o como fragmento («passage: »).
"""

import logging
from pathlib import Path

import chromadb
from chromadb.config import Settings
from chromadb.errors import NotFoundError
from sentence_transformers import SentenceTransformer

from src.rag.retrievers.texto import texto_para_indexar

log = logging.getLogger(__name__)

COLECCION = "manual"


def cargar_modelo(nombre: str) -> SentenceTransformer:
    """Carga el modelo de embeddings. La primera vez lo descarga de Hugging Face."""
    return SentenceTransformer(nombre)


class IndiceDenso:
    """Índice de vectores en Chroma, guardado en disco."""

    def __init__(self, ruta: Path, modelo):
        self.modelo = modelo
        # Sin telemetría: Chroma no manda estadísticas de uso afuera.
        self.cliente = chromadb.PersistentClient(path=str(ruta), settings=Settings(anonymized_telemetry=False))

    def _vectores(self, textos: list[str]) -> list[list[float]]:
        # Normalizados, para que la distancia coseno compare solo la dirección de los vectores.
        return self.modelo.encode(textos, normalize_embeddings=True).tolist()

    def indexar(self, chunks: list[dict]) -> None:
        """Arma el índice desde cero: calcula el vector de cada chunk y lo guarda con sus metadatos."""
        try:
            self.cliente.delete_collection(COLECCION)
        except NotFoundError:
            pass  # La primera vez todavía no existe.
        coleccion = self.cliente.create_collection(COLECCION, configuration={"hnsw": {"space": "cosine"}})
        coleccion.add(
            ids=[c["id"] for c in chunks],
            embeddings=self._vectores([f"passage: {texto_para_indexar(c)}" for c in chunks]),
            documents=[c["texto"] for c in chunks],
            # Chroma no acepta valores vacíos en los metadatos (la introducción no tiene sección).
            metadatas=[{k: v for k, v in c["metadata"].items() if v is not None} for c in chunks],
        )
        log.info("Índice de vectores armado con %d chunks", len(chunks))

    def buscar(self, consulta: str, k: int) -> list[tuple[str, float]]:
        """Devuelve los k chunks más parecidos a la consulta, con su similitud (de -1 a 1)."""
        coleccion = self.cliente.get_collection(COLECCION)
        resultado = coleccion.query(query_embeddings=self._vectores([f"query: {consulta}"]), n_results=k)
        # Chroma devuelve la distancia coseno. La similitud es 1 menos la distancia.
        return [(id_, 1 - distancia) for id_, distancia in zip(resultado["ids"][0], resultado["distances"][0])]
