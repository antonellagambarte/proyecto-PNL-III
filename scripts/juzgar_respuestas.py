"""El juez: mide las respuestas guardadas con dos métricas de DeepEval que usan un LLM como juez.

- Answer Relevancy: si la respuesta contesta lo que se preguntó, sin irse por las ramas.
- Faithfulness: si lo que afirma la respuesta está en los fragmentos que encontró el sistema.

El juez es el mismo modelo del sistema. DeepEval no es dependencia del proyecto: uv lo baja
aparte para esta corrida, sin tocar las versiones del proyecto. Uso, desde la raíz:
    uv run --with deepeval python -m scripts.juzgar_respuestas <nombre>

Lee reports/respuestas_<nombre>.jsonl, que deja scripts.evaluar_sistema. Usa el LLM: con las
40 de práctica cuesta unos tres centavos. Guarda reports/juez_<nombre>.csv y .md.
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
from src.runtime.providers.llm import crear_llm

log = logging.getLogger("juzgar_respuestas")


class Juez(DeepEvalBaseLLM):
    """El LLM del sistema, con la forma que pide DeepEval para usarlo como juez."""

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
    metricas = {"relevancia": AnswerRelevancyMetric}
    if texto["fragmentos"]:
        metricas["fidelidad"] = FaithfulnessMetric
    fila = {"id": texto["id"], "fidelidad": None, "motivo_fidelidad": None}
    with get_usage_metadata_callback() as uso:
        for nombre, Metrica in metricas.items():
            metrica = Metrica(model=juez, include_reason=True, async_mode=False, verbose_mode=False)
            metrica.measure(caso, _show_indicator=False)
            fila[nombre], fila[f"motivo_{nombre}"] = round(metrica.score, 3), metrica.reason
    return {**fila, **tokens(uso.usage_metadata)}


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit("Uso: uv run --with deepeval python -m scripts.juzgar_respuestas <nombre>")
    nombre = sys.argv[1]
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    reportes = resolver_ruta(rutas["reportes"])
    textos = leer_jsonl(reportes / f"respuestas_{nombre}.jsonl")
    juez = Juez(config)
    # De a cuatro a la vez: cada respuesta lleva varias llamadas al juez.
    with ThreadPoolExecutor(4) as hilos:
        filas = list(hilos.map(lambda texto: juzgar(juez, texto), textos))

    tabla = pd.DataFrame(filas)
    tabla.to_csv(reportes / f"juez_{nombre}.csv", index=False)
    (reportes / f"juez_{nombre}.md").write_text(markdown_juez(nombre, tabla), encoding="utf-8")
    gasto = costo(tabla["tokens_entrada"].sum(), tabla["tokens_salida"].sum(), config["llm"])
    print(tabla[["id", "relevancia", "fidelidad"]].to_string(index=False))
    print(f"\nRelevancia p50 {tabla['relevancia'].median():.2f} | Fidelidad p50 {tabla['fidelidad'].median():.2f} | US$ {gasto:.4f}")
    log.info("Listo: %s", reportes / f"juez_{nombre}.md")


if __name__ == "__main__":
    main()
