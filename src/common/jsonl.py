"""Lectura y escritura de archivos JSONL: un objeto JSON por línea."""

import json
from pathlib import Path


def escribir_jsonl(registros: list[dict], ruta: Path) -> None:
    """Guarda cada registro en una línea. Crea la carpeta si no existe."""
    ruta = Path(ruta)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with ruta.open("w", encoding="utf-8") as archivo:
        for registro in registros:
            archivo.write(json.dumps(registro, ensure_ascii=False) + "\n")


def leer_jsonl(ruta: Path) -> list[dict]:
    """Lee un archivo JSONL y devuelve la lista de registros."""
    with Path(ruta).open(encoding="utf-8") as archivo:
        return [json.loads(linea) for linea in archivo if linea.strip()]
