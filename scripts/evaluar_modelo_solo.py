"""La variante «modelo solo»: le hace las preguntas con opciones al LLM, sin darle el manual.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.evaluar_modelo_solo [practica|test]

Usa el LLM: cuesta menos de un centavo. Guarda en reports/modelo_solo_<conjunto>.csv qué
eligió el modelo en cada pregunta y si acertó. scripts.evaluar_sistema lo suma a su tabla de
variantes, así que conviene correr este primero.
"""

import logging
import sys

import pandas as pd
from langchain_core.callbacks import get_usage_metadata_callback

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import leer_jsonl
from src.common.logs import configurar_logging
from src.rag.evaluators.costo import costo, tokens
from src.rag.evaluators.modelo_solo import responder_sin_manual
from src.rag.evaluators.sistema import CONJUNTOS
from src.runtime.providers.llm import crear_llm

log = logging.getLogger("evaluar_modelo_solo")


def main() -> None:
    conjunto = sys.argv[1] if len(sys.argv) > 1 else "practica"
    if conjunto not in CONJUNTOS:
        sys.exit("Uso: python -m scripts.evaluar_modelo_solo [practica|test]")
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    preguntas = leer_jsonl(resolver_ruta(rutas["procesados"]) / CONJUNTOS[conjunto])
    with get_usage_metadata_callback() as uso:
        filas = responder_sin_manual(crear_llm(config), preguntas)
    usados = tokens(uso.usage_metadata)

    reportes = resolver_ruta(rutas["reportes"])
    reportes.mkdir(parents=True, exist_ok=True)
    tabla = pd.DataFrame(filas)
    tabla.to_csv(reportes / f"modelo_solo_{conjunto}.csv", index=False)
    print(tabla.to_string(index=False))
    print(f"\nAciertos sin el manual: {int(tabla['acierta'].sum())} de {len(tabla)}"
          f" | US$ {costo(usados['tokens_entrada'], usados['tokens_salida'], config['llm']):.4f}")
    log.info("Listo: %s", reportes / f"modelo_solo_{conjunto}.csv")


if __name__ == "__main__":
    main()
