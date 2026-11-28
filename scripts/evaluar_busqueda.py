"""Evaluación de la búsqueda sola: las cuatro variantes con las preguntas de práctica o de test.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.evaluar_busqueda [practica|test]

Adaptado del script de la cátedra. Usa las preguntas con páginas esperadas, mide las páginas
encontradas, el context recall y los tiempos, y guarda las tablas en reports/<conjunto>/. Con la práctica,
además, prueba distintas cantidades de candidatos y fragmentos para elegir los de config.yaml.
"""

import logging
import sys

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import leer_jsonl
from src.common.logs import configurar_logging
from src.rag.evaluators.busqueda import corpus, evaluar, probar_tamanos, revisar_evidencias, tiempos
from src.rag.evaluators.sistema import CONJUNTOS
from src.rag.retrievers.hibrida import crear_buscador

log = logging.getLogger("evaluar_busqueda")


def main() -> None:
    conjunto = sys.argv[1] if len(sys.argv) > 1 else "practica"
    if conjunto not in CONJUNTOS:
        sys.exit("Uso: python -m scripts.evaluar_busqueda [practica|test]")
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    preguntas = [p for p in leer_jsonl(resolver_ruta(rutas["procesados"]) / CONJUNTOS[conjunto]) if p["paginas"]]
    buscador = crear_buscador(config)
    # La primera búsqueda tarda más porque los modelos terminan de prepararse. No se mide.
    buscador.buscar("¿Cuál es la velocidad máxima en avenidas?", 5)

    por_pregunta, promedios = evaluar(buscador, preguntas, tuple(config["evaluacion"]["ks"]))
    segundos = tiempos(por_pregunta)

    # Cada conjunto en su carpeta: reports/practica o reports/test.
    reportes = resolver_ruta(rutas["reportes"]) / conjunto
    reportes.mkdir(parents=True, exist_ok=True)
    evidencias = revisar_evidencias(preguntas, list(corpus(buscador).values()))
    por_pregunta.to_csv(reportes / "busqueda_por_pregunta.csv", index=False)
    promedios.to_csv(reportes / "busqueda_promedios.csv", index=False)
    segundos.to_csv(reportes / "busqueda_tiempos.csv", index=False)
    evidencias.to_csv(reportes / "busqueda_evidencias.csv", index=False)

    print(f"\n=== Promedios por variante y k ({len(preguntas)} preguntas de {conjunto}) ===")
    print(promedios.round(3).to_string(index=False))
    afuera = evidencias[~evidencias["buscable"]]
    print(f"\nContext recall: {len(evidencias) - len(afuera)} de {len(evidencias)} frases de evidencia se pueden medir.")
    for fila in afuera.itertuples():
        print(f"  Afuera, porque no está tal cual en ningún fragmento: {fila.id}, «{fila.evidencia[:70]}…»")
    print("\n=== Segundos por búsqueda ===")
    print(segundos.round(3).to_string(index=False))
    if conjunto == "practica":
        evaluacion = config["evaluacion"]
        tamanos = probar_tamanos(buscador, preguntas, evaluacion["candidatos"], evaluacion["fragmentos"])
        tamanos.to_csv(reportes / "busqueda_tamanos.csv", index=False)
        print("\n=== Búsqueda completa con distintos tamaños ===")
        print(tamanos.round(3).to_string(index=False))
    log.info("Listo: tablas en %s", reportes)


if __name__ == "__main__":
    main()
