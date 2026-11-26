"""Evaluación de la búsqueda: métricas de las cuatro variantes sobre el dataset de evaluación.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.evaluar_busqueda

Adaptado del script de evaluación de la búsqueda del código de la cátedra. Usa las
preguntas de data/processed/preguntas_eval.jsonl que tienen páginas relevantes (las que
el manual no menciona no tienen contra qué medirse) y guarda las tablas en reports/.

También prueba la búsqueda completa con las cantidades de candidatos y de fragmentos de la
sección evaluacion de config.yaml, para elegir k_candidatos y k_fragmentos
(reports/busqueda_tamanos.csv). No usa el LLM.
"""

import logging

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import leer_jsonl
from src.common.logs import configurar_logging
from src.rag.evaluators.busqueda import evaluar, probar_tamanos, tiempos
from src.rag.retrievers.hibrida import crear_buscador

log = logging.getLogger("evaluar_busqueda")


def main() -> None:
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    preguntas = [p for p in leer_jsonl(resolver_ruta(rutas["procesados"]) / "preguntas_eval.jsonl") if p["paginas"]]
    buscador = crear_buscador(config)
    # La primera búsqueda tarda más porque los modelos terminan de prepararse. No se mide.
    buscador.buscar("¿Cuál es la velocidad máxima en avenidas?", 5)

    por_pregunta, promedios = evaluar(buscador, preguntas, tuple(config["evaluacion"]["ks"]))
    segundos = tiempos(por_pregunta)

    reportes = resolver_ruta(rutas["reportes"])
    reportes.mkdir(parents=True, exist_ok=True)
    por_pregunta.to_csv(reportes / "busqueda_por_pregunta.csv", index=False)
    promedios.to_csv(reportes / "busqueda_promedios.csv", index=False)
    segundos.to_csv(reportes / "busqueda_tiempos.csv", index=False)
    evaluacion = config["evaluacion"]
    tamanos = probar_tamanos(buscador, preguntas, evaluacion["candidatos"], evaluacion["fragmentos"])
    tamanos.to_csv(reportes / "busqueda_tamanos.csv", index=False)

    print(f"\n=== Promedios por variante y k ({len(preguntas)} preguntas) ===")
    print(promedios.round(3).to_string(index=False))
    print("\n=== Segundos por búsqueda ===")
    print(segundos.round(3).to_string(index=False))
    print("\n=== Búsqueda completa con distintos tamaños ===")
    print(tamanos.round(3).to_string(index=False))
    log.info("Listo: tablas en %s", reportes)


if __name__ == "__main__":
    main()
