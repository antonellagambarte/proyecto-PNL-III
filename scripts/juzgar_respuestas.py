"""El juez: mide las respuestas guardadas con Answer Relevancy y Faithfulness de DeepEval.

Uso, desde la raíz del proyecto (--with instala DeepEval solo para esta corrida):
    uv run --with deepeval==4.3.6 python -m scripts.juzgar_respuestas <nombre> [practica|test]

Lee reports/<conjunto>/respuestas_<nombre>.jsonl y guarda ahí juez_<nombre>.csv y .md.
"""

import os

# Sin telemetría: tiene que estar antes de importar DeepEval.
os.environ["DEEPEVAL_TELEMETRY_OPT_OUT"] = "YES"

import logging
import sys
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric
from deepeval.models.base_model import DeepEvalBaseLLM
from deepeval.test_case import LLMTestCase
from langchain_core.callbacks import get_usage_metadata_callback

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import leer_jsonl
from src.common.logs import configurar_logging
from src.rag.evaluators.costo import costo, tokens
from src.rag.evaluators.juez import markdown_juez
from src.rag.evaluators.sistema import CONJUNTOS
from src.runtime.providers.llm import crear_llm

log = logging.getLogger("juzgar_respuestas")


def config_del_juez(config: dict) -> dict:
    """La configuración del LLM con el modelo y los precios del juez (sección evaluacion de config.yaml)."""
    evaluacion = config["evaluacion"]
    return {**config, "llm": {**config["llm"], "modelo": evaluacion["modelo_juez"],
                              "precio_entrada": evaluacion["precio_juez_entrada"],
                              "precio_salida": evaluacion["precio_juez_salida"]}}


class Juez(DeepEvalBaseLLM):
    """El LLM del juez, con la forma que pide DeepEval para usarlo."""

    def __init__(self, config: dict):
        self.llm = crear_llm(config)
        self.nombre = config["llm"]["modelo"]
        super().__init__(self.nombre)

    def load_model(self, *args, **kwargs):
        return self.llm

    def get_model_name(self, *args, **kwargs) -> str:
        return self.nombre

    def generate(self, prompt: str, schema=None):
        if schema:
            return self.llm.with_structured_output(schema).invoke(prompt)
        return self.llm.invoke(prompt).text

    async def a_generate(self, prompt: str, schema=None):
        return self.generate(prompt, schema)


def juzgar(juez: Juez, texto: dict) -> dict:
    """Las dos métricas de una respuesta. Sin fragmentos (pregunta rechazada) no hay fidelidad que medir."""
    caso = LLMTestCase(input=texto["pregunta"], actual_output=texto["respuesta"],
                       retrieval_context=texto["fragmentos"])
    metricas = {"relevancia": (AnswerRelevancyMetric, {})}
    if texto["fragmentos"]:
        # Una afirmación que los fragmentos no confirman ni contradicen cuenta como no fiel. Por defecto
        # DeepEval la cuenta como fiel, y entonces solo bajarían el puntaje las contradicciones.
        metricas["fidelidad"] = (FaithfulnessMetric, {"penalize_ambiguous_claims": True})
    fila = {"id": texto["id"], "fidelidad": None, "motivo_fidelidad": None}
    with get_usage_metadata_callback() as uso:
        for nombre, (Metrica, opciones) in metricas.items():
            metrica = Metrica(model=juez, include_reason=True, async_mode=False, verbose_mode=False, **opciones)
            metrica.measure(caso, _show_indicator=False)
            fila[nombre], fila[f"motivo_{nombre}"] = round(metrica.score, 3), metrica.reason
    return {**fila, **tokens(uso.usage_metadata)}


def main() -> None:
    conjunto = sys.argv[2] if len(sys.argv) > 2 else "practica"
    if len(sys.argv) < 2 or conjunto not in CONJUNTOS:
        sys.exit("Uso: uv run --with deepeval==4.3.6 python -m scripts.juzgar_respuestas <nombre> [practica|test]")
    nombre = sys.argv[1]
    config = config_del_juez(cargar_config())
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    reportes = resolver_ruta(rutas["reportes"]) / conjunto
    textos = leer_jsonl(reportes / f"respuestas_{nombre}.jsonl")
    juez = Juez(config)
    # De a cuatro a la vez: cada respuesta lleva varias llamadas al juez.
    with ThreadPoolExecutor(4) as hilos:
        filas = list(hilos.map(lambda texto: juzgar(juez, texto), textos))

    tabla = pd.DataFrame(filas)
    tabla.to_csv(reportes / f"juez_{nombre}.csv", index=False)
    (reportes / f"juez_{nombre}.md").write_text(markdown_juez(nombre, tabla, juez.nombre, conjunto), encoding="utf-8")
    gasto = costo(tabla["tokens_entrada"].sum(), tabla["tokens_salida"].sum(), config["llm"])
    print(tabla[["id", "relevancia", "fidelidad"]].to_string(index=False))
    print(f"\nRelevancia p50 {tabla['relevancia'].median():.2f} | Fidelidad p50 {tabla['fidelidad'].median():.2f} | US$ {gasto:.4f}")
    log.info("Listo: %s", reportes / f"juez_{nombre}.md")


if __name__ == "__main__":
    main()
