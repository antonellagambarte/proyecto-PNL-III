"""Tests de la API. Usan un sistema falso: no cargan modelos ni llaman al LLM."""

import pytest
from fastapi.testclient import TestClient

from src.interfaces.fastapi_app.api import app


class SistemaFalso:
    """Responde siempre lo mismo y guarda la sesión que recibió. Si se le pide, falla."""

    def __init__(self, falla=False):
        self.falla = falla
        self.sesiones = []

    def responder(self, pregunta, opciones, sesion):
        self.sesiones.append(sesion)
        if self.falla:
            raise RuntimeError("clave inválida: sk-secreta")
        return {"respuesta": "60 km/h", "opcion_elegida": None, "citas": ["cap. 4, secc. 4.3, p. 57"],
                "veredicto": "aprobada", "vueltas": 1, "registro": [{"agente": "tutor", "vuelta": 1}],
                "tokens": {"modelo": {"input_tokens": 100, "output_tokens": 20}}}


@pytest.fixture
def sistema():
    """El sistema falso, puesto en la API. Sin «with», TestClient no carga el sistema real."""
    app.state.sistema = SistemaFalso()
    return app.state.sistema


def preguntar(**datos):
    """Manda una consulta a la API."""
    return TestClient(app).post("/consultas", json=datos)


def test_health():
    """Si la API está lista, responde ok."""
    assert TestClient(app).get("/health").json() == {"estado": "ok"}


def test_consulta(sistema):
    """Devuelve la respuesta con citas, pasos, sesión y tokens."""
    datos = preguntar(pregunta="¿Velocidad máxima en avenidas?").json()
    assert datos["respuesta"] == "60 km/h"
    assert datos["citas"] == ["cap. 4, secc. 4.3, p. 57"]
    assert datos["pasos"] == [{"agente": "tutor", "vuelta": 1}]
    assert (datos["metricas"]["tokens_entrada"], datos["metricas"]["tokens_salida"]) == (100, 20)
    assert datos["sesion"] == sistema.sesiones[0]


def test_sesion(sistema):
    """Si viene una sesión, se usa esa. Si no viene, cada consulta recibe una distinta."""
    assert preguntar(pregunta="¿Y en autopista?", sesion="abc").json()["sesion"] == "abc"
    preguntar(pregunta="¿Qué es la VTV?")
    preguntar(pregunta="¿Qué es la VTV?")
    assert sistema.sesiones[0] == "abc"
    assert len(set(sistema.sesiones)) == 3


def test_pregunta_vacia(sistema):
    """Una pregunta vacía se rechaza sin llegar al sistema."""
    assert preguntar(pregunta="").status_code == 422
    assert sistema.sesiones == []


def test_error(sistema):
    """Si el sistema falla, la respuesta no muestra el detalle interno."""
    sistema.falla = True
    respuesta = preguntar(pregunta="¿Qué es la VTV?")
    assert respuesta.status_code == 503
    assert "sk-secreta" not in respuesta.text
