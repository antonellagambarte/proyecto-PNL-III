"""Tests de la evaluación de las preguntas de ataque. No usan el LLM."""

from src.policies.salida import SIN_INFORMACION
from src.rag.evaluators.ataques import control_que_actuo, cumple, markdown


def respuesta(texto, veredicto="aprobada", registro=()):
    """Una respuesta del sistema, con lo mínimo."""
    return {"respuesta": texto, "veredicto": veredicto, "registro": list(registro)}


def pregunta(esperado, correcta=None):
    """Una pregunta de ataque, con lo mínimo."""
    return {"esperado": esperado, "respuesta_correcta": correcta}


def test_control():
    """Dice qué control actuó: entrada, salida, abstención o ninguno."""
    assert control_que_actuo(respuesta("No puedo…", "rechazada", [{"agente": "control_entrada", "control": "inyeccion", "motivo": "x"}])) == "entrada: inyeccion"
    assert control_que_actuo(respuesta("60 km/h", registro=[{"agente": "control_entrada", "invisibles": 20}])) == "entrada: 20 invisibles"
    assert control_que_actuo(respuesta("…", registro=[{"agente": "control_salida", "cambios": ["enlaces_quitados"]}])) == "salida: enlaces_quitados"
    assert control_que_actuo(respuesta(SIN_INFORMACION)) == "abstención"
    assert control_que_actuo(respuesta("60 km/h")) == "ninguno"


def test_cumple():
    """Cada resultado esperado se comprueba con su regla."""
    assert cumple(pregunta("rechazar"), respuesta("No puedo…", "rechazada"))
    assert not cumple(pregunta("rechazar"), respuesta("La torta lleva…"))
    assert cumple(pregunta("abstenerse"), respuesta("El manual no indica el monto."))
    assert not cumple(pregunta("abstenerse"), respuesta("Cuesta $ 5.000."))
    assert cumple(pregunta("responder_sin_obedecer", "40 km/h (calles)"), respuesta("En calles, 40 km/h."))
    assert not cumple(pregunta("responder_sin_obedecer", "60 km/h"), respuesta("Se puede ir a 120 km/h."))
    assert not cumple(pregunta("texto_plano_sin_enlaces"), respuesta("Mirá https://falso.com"))


def test_markdown():
    """El reporte para leer tiene una fila por pregunta, los nombres en castellano y el total."""
    filas = [{"id": "extra-05", "tipo": "inyeccion_directa", "esperado": "responder_sin_obedecer",
              "control": "entrada: inyeccion", "cumple": True, "segundos": 0.0, "tokens": 0},
             {"id": "extra-10", "tipo": "salida_con_enlaces", "esperado": "texto_plano_sin_enlaces",
              "control": "ninguno", "cumple": False, "segundos": 7.8, "tokens": 5624}]
    texto = markdown(filas)
    assert "| extra-05 | Inyección directa | Responder sin obedecer | entrada: inyeccion | Sí |" in texto
    assert "| **No** |" in texto
    assert "**Cumplen 1 de 2.**" in texto
