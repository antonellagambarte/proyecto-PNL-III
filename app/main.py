"""Punto de entrada de la API.

Uso, desde la raíz del proyecto:
    uv run uvicorn app.main:app
"""

from src.interfaces.fastapi_app.api import app

__all__ = ["app"]
