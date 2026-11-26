"""Pruebas de ataque: pasa las preguntas de ataque y fuera de tema por el sistema completo.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.probar_ataques

Usa el LLM: cuesta alrededor de un centavo. Guarda en reports/ataques.csv, para cada pregunta,
qué se esperaba, qué control actuó y si se cumplió, y la misma tabla para leer en ataques.md.
"""

import logging
import time

import pandas as pd

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import leer_jsonl
from src.common.logs import configurar_logging
from src.graphs.workflows.tutor_verificador import TutorVerificador
from src.rag.evaluators.ataques import evaluar, markdown

log = logging.getLogger("probar_ataques")


def main() -> None:
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    preguntas = leer_jsonl(resolver_ruta(rutas["procesados"]) / "preguntas_extra.jsonl")
    sistema = TutorVerificador(config)
    filas = []
    for pregunta in preguntas:
        inicio = time.perf_counter()
        respuesta = sistema.responder(pregunta["pregunta"])
        tokens = respuesta["tokens"].values()
        filas.append({
            **evaluar(pregunta, respuesta),
            "segundos": round(time.perf_counter() - inicio, 1),
            "tokens": sum(uso["input_tokens"] + uso["output_tokens"] for uso in tokens),
        })

    tabla = pd.DataFrame(filas)
    reportes = resolver_ruta(rutas["reportes"])
    reportes.mkdir(parents=True, exist_ok=True)
    tabla.to_csv(reportes / "ataques.csv", index=False)
    (reportes / "ataques.md").write_text(markdown(filas), encoding="utf-8")
    print(tabla.to_string(index=False))
    print(f"\nCumplen {tabla['cumple'].sum()} de {len(tabla)}")
    log.info("Listo: %s", reportes / "ataques.csv")


if __name__ == "__main__":
    main()
