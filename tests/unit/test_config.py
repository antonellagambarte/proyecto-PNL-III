"""Tests de la carga de configuración."""

import pytest

from src.common.config import ErrorConfiguracion, cargar_config, obtener_api_key, resolver_ruta


def test_la_configuracion_del_proyecto_se_lee():
    config = cargar_config()
    assert {"llm", "agentes", "busqueda", "chunks", "rutas", "logging"} <= config.keys()


def test_las_rutas_relativas_se_toman_desde_la_raiz():
    assert resolver_ruta("logs").is_absolute()


def test_falla_con_un_mensaje_claro_si_no_existe_el_archivo(tmp_path):
    with pytest.raises(ErrorConfiguracion, match="No se encontró"):
        cargar_config(tmp_path / "no_existe.yaml")


def test_falla_si_falta_la_api_key(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with pytest.raises(ErrorConfiguracion, match="OPENAI_API_KEY"):
        obtener_api_key(tmp_path / ".env_inexistente")
