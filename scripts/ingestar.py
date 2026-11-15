"""Ingesta del manual: del PDF a los chunks con metadatos.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.ingestar

Lee el PDF, arma las secciones (con las tablas transcriptas a mano) y las corta
en chunks. Guarda los resultados en data/processed/.
"""

import logging

from src.common.config import cargar_config, resolver_ruta
from src.common.jsonl import escribir_jsonl
from src.common.logs import configurar_logging
from src.rag.ingestion.chunks import armar_chunks
from src.rag.ingestion.parseo import parsear_manual

log = logging.getLogger("ingestar")


def main() -> None:
    config = cargar_config()
    rutas = config["rutas"]
    configurar_logging(resolver_ruta(rutas["logs"]), config["logging"]["nivel"])

    ruta_pdf = resolver_ruta(rutas["manual_pdf"])
    procesados = resolver_ruta(rutas["procesados"])

    secciones = parsear_manual(ruta_pdf, resolver_ruta(rutas["transcripciones"]))
    escribir_jsonl(secciones, procesados / "secciones.jsonl")

    chunks = armar_chunks(
        secciones,
        config["chunks"]["max_tokens"],
        config["chunks"]["solapamiento"],
        ruta_pdf.name,
    )
    escribir_jsonl(chunks, procesados / "chunks.jsonl")

    transcriptos = sum(chunk["metadata"]["origen"] == "transcripcion_manual" for chunk in chunks)
    log.info(
        "Listo: %d secciones y %d chunks (%d con texto transcripto) en %s",
        len(secciones), len(chunks), transcriptos, procesados,
    )


if __name__ == "__main__":
    main()
