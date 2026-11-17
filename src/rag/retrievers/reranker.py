"""Re-ranking con un cross-encoder.

Adaptado del re-ranking del código de la cátedra, con un modelo multilingüe.
"""

from sentence_transformers import CrossEncoder


class Reranker:
    """Reordena candidatos leyendo la pregunta junto con el texto de cada uno."""

    def __init__(self, nombre_modelo: str):
        self.modelo = CrossEncoder(nombre_modelo)

    def reordenar(self, consulta: str, candidatos: list[tuple[str, str]]) -> list[tuple[str, float]]:
        """Recibe pares (id, texto) y los devuelve como (id, puntaje), del más al menos relevante."""
        if not candidatos:
            return []
        pares = [(consulta, texto) for _, texto in candidatos]
        puntajes = self.modelo.predict(pares)
        salida = [(id_, float(puntaje)) for (id_, _), puntaje in zip(candidatos, puntajes)]
        salida.sort(key=lambda par: par[1], reverse=True)
        return salida
