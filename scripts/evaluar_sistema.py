"""Evaluación del sistema completo: pasa un conjunto de preguntas y mide cada respuesta.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.evaluar_sistema <nombre> [practica|test]

El nombre identifica la corrida (por ejemplo antes y despues de un cambio en config.yaml).
El conjunto es practica (las de ajuste) o test (el test final). Usa el LLM: con las 30 de
práctica cuesta unos tres centavos. Guarda en reports/:
- evaluacion_<nombre>.csv y .md: una fila por pregunta, con aciertos, citas, vueltas,
  tiempos, tokens y costo, y los totales.
- respuestas_<nombre>.jsonl: pregunta, respuesta, fragmentos y lo que hizo cada agente en cada
  vuelta (con el motivo del verificador), para juzgarlas con scripts.juzgar_respuestas y para
  leer por qué falló una pregunta.
- corridas.md: una fila por corrida, para comparar antes y después.
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

    # El parecido con la respuesta esperada se calcula al final, con el mismo modelo de embeddings de la búsqueda.
    modelo = SentenceTransformer(config["busqueda"]["modelo_embeddings"])
    parecidos = similitud(modelo, [t["respuesta"] for t in textos], [t["esperada"] for t in textos])
    for fila, parecido in zip(filas, parecidos):
        fila["parecido"] = parecido

    reportes = resolver_ruta(rutas["reportes"])
    reportes.mkdir(parents=True, exist_ok=True)
    tabla = pd.DataFrame(filas)
    tabla.to_csv(reportes / f"evaluacion_{nombre}.csv", index=False)
    with open(reportes / f"respuestas_{nombre}.jsonl", "w", encoding="utf-8") as archivo:
        archivo.writelines(json.dumps(t, ensure_ascii=False) + "\n" for t in textos)

    # El modelo solo se corre aparte, con scripts.evaluar_modelo_solo. Si ya está, entra en la tabla de variantes.
    solo = reportes / f"modelo_solo_{conjunto}.csv"
    modelo_solo = None
    if solo.exists():
        aciertos = pd.read_csv(solo)["acierta"].dropna().astype(bool)
        modelo_solo = f"{int(aciertos.sum())} de {len(aciertos)}"
    (reportes / f"evaluacion_{nombre}.md").write_text(markdown_corrida(nombre, tabla, modelo_solo), encoding="utf-8")

    # La comparación junta todas las corridas guardadas, de la más vieja a la más nueva.
    corridas = sorted(reportes.glob("evaluacion_*.csv"), key=lambda ruta: ruta.stat().st_mtime)
    resumenes = [resumir(ruta.stem.removeprefix("evaluacion_"), pd.read_csv(ruta)) for ruta in corridas]
    (reportes / "corridas.md").write_text(markdown_corridas(resumenes), encoding="utf-8")
    print(pd.DataFrame(resumenes).T.to_string(header=False))
    log.info("Listo: %s", reportes / f"evaluacion_{nombre}.md")


if __name__ == "__main__":
    main()
