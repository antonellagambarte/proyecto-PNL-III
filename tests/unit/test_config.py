"""Tests de la carga de configuración."""

import pytest

from src.common.config import ErrorConfiguracion, cargar_config, obtener_api_key, resolver_ruta


def test_secciones():
    """El config.yaml del proyecto tiene todas las secciones que usa el sistema."""
    config = cargar_config()
    assert {"llm", "agentes", "busqueda", "chunks", "rutas", "logging"} <= config.keys()


def test_rutas_relativas():
    """Una ruta relativa se completa desde la raíz del proyecto."""
    assert resolver_ruta("logs").is_absolute()


def test_config_inexistente(tmp_path):
    """Si config.yaml no existe, el error lo dice con un mensaje claro."""
    with pytest.raises(ErrorConfiguracion, match="No se encontró"):
        cargar_config(tmp_path / "no_existe.yaml")


def test_falta_api_key(tmp_path, monkeypatch):
    """Si no hay API key, el error dice qué falta y cómo cargarla."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ErrorConfiguracion, match="OPENAI_API_KEY"):
        obtener_api_key(tmp_path / ".env_inexistente")
