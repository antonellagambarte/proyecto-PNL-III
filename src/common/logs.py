"""Configura el registro de eventos (logging) del sistema.

Los mensajes salen por consola y quedan guardados en logs/app.log, con niveles
(DEBUG, INFO, WARNING, ERROR). El archivo rota al llegar a 1 MB.
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

    raiz = logging.getLogger()
    raiz.setLevel(nivel)
    # Si se llama más de una vez, se reemplazan los manejadores para no duplicar mensajes.
    for manejador in list(raiz.handlers):
        raiz.removeHandler(manejador)
        manejador.close()

    formato = logging.Formatter(FORMATO)
    consola = logging.StreamHandler()
    consola.setFormatter(formato)
    archivo = RotatingFileHandler(ruta_archivo, maxBytes=1_000_000, backupCount=3, encoding="utf-8")
    archivo.setFormatter(formato)
    raiz.addHandler(consola)
    raiz.addHandler(archivo)
    return ruta_archivo
