"""Extracción del cuestionario oficial: del PDF a un JSONL con todas las preguntas.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.extraer_cuestionario

Cada pregunta sale con su sección, sus opciones, la respuesta correcta (la marcada en
verde) y si sirve para el dataset de evaluación (campo "candidata"). El resultado queda
en data/interim/cuestionario.jsonl.
"""

import logging
from collections import Counter

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import escribir_jsonl
from src.common.logs import configurar_logging
from src.rag.evaluators.cuestionario import es_candidata, extraer_preguntas

log = logging.getLogger("extraer_cuestionario")


def main() -> None:
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    preguntas = extraer_preguntas(resolver_ruta(rutas["cuestionario"]))
    for pregunta in preguntas:
        pregunta["candidata"] = es_candidata(pregunta)
    ruta = resolver_ruta(rutas["intermedios"]) / "cuestionario.jsonl"
    escribir_jsonl(preguntas, ruta)

    respuestas = Counter(len(p["correctas"]) for p in preguntas)
    log.info(
        "Listo: %d preguntas (%d con imagen, %d sin respuesta marcada, %d con más de una) "
        "y %d candidatas para el dataset, en %s",
        len(preguntas), sum(p["imagen"] for p in preguntas), respuestas[0],
        sum(n for cantidad, n in respuestas.items() if cantidad > 1),
        sum(p["candidata"] for p in preguntas), ruta,
    )


if __name__ == "__main__":
    main()
