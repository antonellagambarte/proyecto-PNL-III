"""Configura el registro de eventos (logging) del sistema.

Los mensajes salen por consola y quedan guardados en logs/app.log, con niveles
(DEBUG, INFO, WARNING, ERROR). Para que el archivo no crezca sin límite, cuando
llega a 1 MB se guarda como app.log.1 y se empieza uno nuevo. Se conservan los
3 archivos anteriores.
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

FORMATO = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
NOMBRE_ARCHIVO = "app.log"


def configurar_logging(carpeta: Path, nivel: str = "INFO") -> Path:
    """Prepara la consola y el archivo de logs. Devuelve la ruta del archivo."""
    carpeta = Path(carpeta)
    carpeta.mkdir(parents=True, exist_ok=True)
    ruta_archivo = carpeta / NOMBRE_ARCHIVO

    consola = logging.StreamHandler()
    archivo = RotatingFileHandler(ruta_archivo, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    # force=True saca los handlers de una llamada anterior. Si no, se sumarían
    # a los nuevos y cada mensaje saldría repetido.
    logging.basicConfig(level=nivel, format=FORMATO, handlers=[consola, archivo], force=True)
    return ruta_archivo
