"""Carga la configuración del sistema.

Los parámetros vienen de configs/config.yaml y las credenciales del .env
(o de variables de entorno del sistema). Nada de esto queda fijo en el código.
"""

import os
from pathlib import Path

import yaml
from dotenv import load_dotenv

RAIZ = Path(__file__).resolve().parents[2]
RUTA_CONFIG = RAIZ / "configs" / "config.yaml"
RUTA_ENV = RAIZ / ".env"


class ErrorConfiguracion(RuntimeError):
    """La configuración falta o está mal escrita."""


def cargar_config(ruta: Path = RUTA_CONFIG) -> dict:
    """Lee el archivo YAML y devuelve la configuración como diccionario."""
    try:
        return yaml.safe_load(Path(ruta).read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ErrorConfiguracion(f"No se encontró el archivo de configuración: {ruta}") from error
    except yaml.YAMLError as error:
        raise ErrorConfiguracion(f"El archivo de configuración no es YAML válido: {ruta}") from error


def resolver_ruta(valor: str) -> Path:
    """Devuelve la ruta absoluta; las relativas se toman desde la raíz del proyecto."""
    ruta = Path(valor)
    return ruta if ruta.is_absolute() else RAIZ / ruta


def obtener_api_key(ruta_env: Path = RUTA_ENV) -> str:
    """Devuelve la API key de OpenAI, desde el entorno o desde el .env."""
    load_dotenv(ruta_env)
    clave = os.getenv("OPENAI_API_KEY", "").strip()
    if not clave:
        raise ErrorConfiguracion(
            "Falta OPENAI_API_KEY: copiá .env.example como .env y pegá la key."
        )
    return clave
