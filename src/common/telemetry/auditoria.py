"""Auditoría: una línea en logs/auditoria.jsonl por cada paso de una pregunta, en el momento en que pasa.

Registra decisiones, tiempos y tokens, nunca textos: ni la pregunta, ni las búsquedas del
tutor, ni la respuesta, ni el motivo del verificador. Así el archivo sirve para revisar
qué hizo el sistema sin guardar lo que escribió quien estudia.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Literal

NOMBRE_ARCHIVO = "auditoria.jsonl"

# Gravedad de cada línea: info es lo normal, warning lo que conviene mirar (un ataque frenado,
# algo escondido que se sacó) y error lo que falló.
Gravedad = Literal["info", "warning", "error"]


class Auditoria:
    """Escribe los eventos de una pregunta. Cada línea lleva la hora, el id de la pregunta y los segundos del paso."""

    def __init__(self, carpeta: Path):
        self.ruta = Path(carpeta) / NOMBRE_ARCHIVO
        self.ruta.parent.mkdir(parents=True, exist_ok=True)

    def empezar(self, id_pregunta: str, sesion: str) -> "Pregunta":
        """Abre el registro de una pregunta nueva. Recibe su id, no el texto."""
        return Pregunta(self.ruta, id_pregunta, sesion)


class Pregunta:
    """Los eventos de una pregunta. Mide cuánto tardó cada paso desde el anterior."""

    def __init__(self, ruta: Path, id_pregunta: str, sesion: str):
        self.ruta, self.id_pregunta, self.sesion = ruta, id_pregunta, sesion
        self.inicio = self.anterior = time.perf_counter()

    def registrar(self, evento: str, gravedad: Gravedad = "info", **datos) -> None:
        """Agrega una línea al archivo. Los datos tienen que ser números, listas cortas o palabras fijas."""
        ahora = time.perf_counter()
        linea = {
            "hora": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "id_pregunta": self.id_pregunta,
            "sesion": self.sesion,
            "evento": evento,
            "gravedad": gravedad,
            "segundos": round(ahora - self.anterior, 2),
            **datos,
        }
        self.anterior = ahora
        with self.ruta.open("a", encoding="utf-8") as archivo:
            archivo.write(json.dumps(linea, ensure_ascii=False) + "\n")

    def total(self) -> float:
        """Segundos desde que empezó la pregunta."""
        return round(time.perf_counter() - self.inicio, 2)
