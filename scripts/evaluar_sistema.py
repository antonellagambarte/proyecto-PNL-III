"""Evaluación del sistema completo: pasa un conjunto de preguntas y mide cada respuesta.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.evaluar_sistema <nombre> [practica|test]

El nombre identifica la corrida. Guarda en reports/<conjunto>/:
- evaluacion_<nombre>.csv y .md: una fila por pregunta y los totales.
- respuestas_<nombre>.jsonl: lo que respondió y lo que hizo cada agente, para el juez y para leer por qué falló.
- corridas.md: una fila por corrida, para comparar.
"""

import json
import logging
import sys

import pandas as pd
from sentence_transformers import SentenceTransformer

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import leer_jsonl
from src.common.logs import configurar_logging
from src.graphs.workflows.tutor_verificador import TutorVerificador
from src.rag.evaluators.sistema import CONJUNTOS, markdown_corrida, markdown_corridas, medir, resumir, similitud

log = logging.getLogger("evaluar_sistema")


def main() -> None:
    nombre = sys.argv[1] if len(sys.argv) > 1 else "actual"
    conjunto = sys.argv[2] if len(sys.argv) > 2 else "practica"
    if not nombre.replace("_", "").isalnum() or conjunto not in CONJUNTOS:
        sys.exit("Uso: python -m scripts.evaluar_sistema <nombre> [practica|test]. El nombre, sin espacios ni símbolos.")
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    preguntas = leer_jsonl(resolver_ruta(rutas["procesados"]) / CONJUNTOS[conjunto])
    filas, textos = medir(TutorVerificador(config), preguntas, config, conjunto)

    # La semantic similarity con la respuesta esperada se calcula al final, con el mismo modelo de embeddings de la búsqueda.
    modelo = SentenceTransformer(config["busqueda"]["modelo_embeddings"])
    parecidos = similitud(modelo, [t["respuesta"] for t in textos], [t["esperada"] for t in textos])
    for fila, parecido in zip(filas, parecidos):
        fila["parecido"] = parecido

    # Cada conjunto en su carpeta: reports/practica o reports/test.
    reportes = resolver_ruta(rutas["reportes"]) / conjunto
    reportes.mkdir(parents=True, exist_ok=True)
    tabla = pd.DataFrame(filas)
    tabla.to_csv(reportes / f"evaluacion_{nombre}.csv", index=False)
    with open(reportes / f"respuestas_{nombre}.jsonl", "w", encoding="utf-8") as archivo:
        archivo.writelines(json.dumps(t, ensure_ascii=False) + "\n" for t in textos)

    (reportes / f"evaluacion_{nombre}.md").write_text(markdown_corrida(nombre, tabla), encoding="utf-8")

    # La comparación junta todas las corridas guardadas del conjunto, de la más vieja a la más nueva.
    corridas = sorted(reportes.glob("evaluacion_*.csv"), key=lambda ruta: ruta.stat().st_mtime)
    resumenes = [resumir(ruta.stem.removeprefix("evaluacion_"), pd.read_csv(ruta)) for ruta in corridas]
    (reportes / "corridas.md").write_text(markdown_corridas(resumenes), encoding="utf-8")
    print(pd.Series(resumir(nombre, tabla)).to_string())
    log.info("Listo: %s", reportes / f"evaluacion_{nombre}.md")


if __name__ == "__main__":
    main()
