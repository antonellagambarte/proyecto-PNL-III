"""Tests de la pantalla. Reemplazan la llamada a la API: no la levantan ni llaman al LLM."""

import httpx
import pytest
from streamlit.testing.v1 import AppTest

from src.common.config import RAIZ

RESPUESTA = {
    "respuesta": "La máxima es 60 km/h.", "opcion_elegida": None, "citas": ["cap. 4, secc. 4.3, p. 57"],
    "veredicto": "aprobada", "vueltas": 1, "sesion": "abc",
    "pasos": [{"agente": "tutor", "vuelta": 1, "consultas": ["velocidad en avenidas"], "respuesta": "60 km/h"},
              {"agente": "verificador", "vuelta": 1, "veredicto": "aprobada", "motivo": "Está en la tabla."}],
    "metricas": {"segundos": 6.5, "tokens_entrada": 100, "tokens_salida": 20},
}


@pytest.fixture
def pedidos(monkeypatch):
    """Reemplaza la API por una que responde siempre lo mismo, y guarda lo que recibió."""
    recibidos = []

    def post(url, json, timeout):
        recibidos.append(json)
        return httpx.Response(200, json=RESPUESTA)

    monkeypatch.setattr(httpx, "post", post)
    return recibidos


def escribir(pantalla, texto):
    """Escribe en el chat y devuelve la pantalla como queda."""
    return pantalla.chat_input[0].set_value(texto).run()


def textos(pantalla):
    """Todo el texto que se ve en la pantalla."""
    return " ".join(e.value for e in [*pantalla.markdown, *pantalla.caption, *pantalla.error])


def abrir():
    """Abre la pantalla como la ve quien entra por primera vez."""
    return AppTest.from_file(str(RAIZ / "app" / "pantalla.py"), default_timeout=30).run()


def test_respuesta(pedidos):
    """Muestra la respuesta, la cita y los pasos. Sin opción elegida, esa línea no aparece."""
    texto = textos(escribir(abrir(), "¿Velocidad máxima en avenidas?"))
    assert "La máxima es 60 km/h." in texto
    assert "p. 57" in texto
    assert "velocidad en avenidas" in texto
    assert "Opción elegida" not in texto


def test_misma_sesion(pedidos):
    """La segunda pregunta manda la sesión de la primera. Con «Nueva charla», empieza otra."""
    pantalla = escribir(escribir(abrir(), "¿Velocidad máxima en avenidas?"), "¿Y en autopista?")
    assert [p["sesion"] for p in pedidos] == [None, "abc"]
    escribir(pantalla.sidebar.button[0].click().run(), "¿Qué es la VTV?")
    assert pedidos[2]["sesion"] is None


def test_api_apagada(monkeypatch):
    """Si la API no está encendida, avisa cómo levantarla."""
    def post(*args, **kwargs):
        raise httpx.ConnectError("sin conexión")

    monkeypatch.setattr(httpx, "post", post)
    assert "La API no está encendida" in textos(escribir(abrir(), "¿Qué es la VTV?"))
