"""Tests de la evaluación del sistema completo, del costo y del modelo solo. No usan el LLM."""

import pandas as pd

from src.rag.evaluators.costo import costo, segundos_por_agente, tokens
from src.rag.evaluators.juez import markdown_juez
from src.rag.evaluators.modelo_solo import Eleccion, responder_sin_manual
from src.rag.evaluators.sistema import (acierta, cita_pagina, markdown_corrida, markdown_corridas, medir,
                                        resumir, segunda_vuelta)
from tests.unit.test_auditoria import sistema_falso

PRECIOS = {"precio_entrada": 0.10, "precio_salida": 0.50}
CON_OPCIONES = {"id": "eval-02", "pregunta": "¿Cuánto tiempo hay para renovar?", "paginas": [13],
                "opciones": ["30 días.", "90 días corridos desde su vencimiento."],
                "correcta": "90 días corridos desde su vencimiento."}
LIBRE = {"id": "eval-37", "pregunta": "¿Velocidad máxima en avenidas?", "paginas": [57], "opciones": [],
         "correcta": "60 km/h."}


def test_costo():
    """Un millón de tokens de entrada y uno de salida cuestan la suma de los dos precios."""
    assert costo(1_000_000, 1_000_000, PRECIOS) == 0.60
    assert round(costo(5_800, 300, PRECIOS), 5) == 0.00073


def test_tokens():
    """Suma los tokens de todos los modelos, y anota aparte los que OpenAI tenía en su caché."""
    usos = {"a": {"input_tokens": 100, "output_tokens": 10, "input_token_details": {"cache_read": 64}},
            "b": {"input_tokens": 50, "output_tokens": 5}}
    assert tokens(usos) == {"tokens_entrada": 150, "tokens_salida": 15, "tokens_en_cache": 64}
    assert tokens({}) == {"tokens_entrada": 0, "tokens_salida": 0, "tokens_en_cache": 0}


def test_segundos_por_agente():
    """Suma las vueltas de cada agente y solo cuenta las líneas de esa sesión."""
    lineas = [{"sesion": "s1", "evento": "tutor", "segundos": 4.0},
              {"sesion": "s1", "evento": "verificador", "segundos": 2.0},
              {"sesion": "s1", "evento": "tutor", "segundos": 3.5},
              {"sesion": "s2", "evento": "tutor", "segundos": 9.0}]
    assert segundos_por_agente(lineas, "s1") == {"segundos_tutor": 7.5, "segundos_verificador": 2.0}


def test_acierta():
    """Compara la opción sin mayúsculas ni punto final. Sin opción elegida, falla. Sin opciones, no se sabe."""
    assert acierta(CON_OPCIONES, "90 días corridos desde su vencimiento")
    assert not acierta(CON_OPCIONES, "30 días.")
    assert not acierta(CON_OPCIONES, None)
    assert acierta(LIBRE, "lo que sea") is None


def test_cita_pagina():
    """Acierta si alguna cita nombra una página esperada, también dentro de un rango como «p. 56–57»."""
    assert cita_pagina(LIBRE, ["cap. 4 (Velocidades), p. 56–57"])
    assert not cita_pagina(LIBRE, ["cap. 4 (Velocidades), p. 103"])
    assert not cita_pagina(LIBRE, [])
    assert cita_pagina({**LIBRE, "paginas": []}, ["p. 57"]) is None


def test_segunda_vuelta():
    """Compara la opción del tutor en la primera vuelta con la final: arregló, arruinó o igual."""
    def respuesta(primera, final, vueltas=2):
        return {"vueltas": vueltas, "opcion_elegida": final,
                "registro": [{"agente": "tutor", "vuelta": 1, "opcion_elegida": primera}]}
    bien, mal = CON_OPCIONES["correcta"], "30 días."
    assert segunda_vuelta(CON_OPCIONES, respuesta(mal, bien)) == "arreglo"
    assert segunda_vuelta(CON_OPCIONES, respuesta(bien, mal)) == "arruino"
    assert segunda_vuelta(CON_OPCIONES, respuesta(bien, bien)) == "igual"
    assert segunda_vuelta(CON_OPCIONES, respuesta(bien, bien, vueltas=1)) is None


def test_medir(tmp_path):
    """Con el sistema falso: una fila por pregunta con lo medido, los segundos de cada agente y los fragmentos."""
    config = {"llm": {"modelo": "falso", **PRECIOS}, "busqueda": {"k_candidatos": 30, "k_fragmentos": 5}}
    filas, textos = medir(sistema_falso(tmp_path, "corregir", "aprobada"), [LIBRE], config, "practica")
    assert filas[0]["vueltas"] == 2
    assert filas[0]["cita_pagina"]  # el tutor falso cita la p. 57
    assert filas[0]["costo"] == 0  # el sistema falso no llama al LLM
    assert {"segundos", "segundos_tutor", "segundos_verificador"} <= filas[0].keys()
    assert "sesion" not in filas[0]
    assert textos[0]["respuesta"] == "60 km/h"
    assert textos[0]["fragmentos"] == ["Avenidas: máxima 60 km/h."]


def test_reportes():
    """El resumen cuenta aciertos y medianas, y los reportes muestran las tres variantes y una fila por corrida."""
    tabla = pd.DataFrame([
        {"id": "eval-01", "forma": "opciones", "veredicto": "aprobada", "vueltas": 1, "acierta": True,
         "acierta_tutor_solo": True, "cita_pagina": True, "segunda_vuelta": None, "parecido": 0.9, "segundos": 5.0,
         "segundos_tutor": 3.0, "segundos_verificador": 2.0, "tokens_entrada": 5000, "tokens_salida": 300,
         "costo": 0.00065, "conjunto": "practica", "k_candidatos": 30, "k_fragmentos": 5},
        {"id": "eval-02", "forma": "opciones", "veredicto": "aprobada", "vueltas": 2, "acierta": True,
         "acierta_tutor_solo": False, "cita_pagina": False, "segunda_vuelta": "arreglo", "parecido": 0.8,
         "segundos": 11.0, "segundos_tutor": 7.0, "segundos_verificador": 4.0, "tokens_entrada": 9000,
         "tokens_salida": 600, "costo": 0.0012, "conjunto": "practica", "k_candidatos": 30, "k_fragmentos": 5},
    ])
    resumen = resumir("antes", tabla)
    assert resumen["aciertos"] == "2 de 2"
    assert resumen["aciertos_tutor_solo"] == "1 de 2"
    assert resumen["arreglo_arruino"] == "1 / 0"
    assert resumen["segundos_p50"] == 8.0
    texto = markdown_corrida("antes", tabla, "33 de 35")
    assert "| Modelo solo, sin el manual | 33 de 35 |" in texto
    assert "| eval-02 | opciones | Sí | **No** |" in texto
    assert "| antes | practica | 30 | 5 |" in markdown_corridas([resumen])


def test_modelo_solo():
    """Solo se preguntan las de opciones. Si una llamada falla, cuenta como error y no como acierto."""
    class LLMFalso:
        def with_structured_output(self, esquema):
            return self

        def batch(self, mensajes, config=None, return_exceptions=False):
            self.mensajes = mensajes
            return [Eleccion(opcion="90 días corridos desde su vencimiento."), TimeoutError()]

    llm = LLMFalso()
    filas = responder_sin_manual(llm, [CON_OPCIONES, LIBRE, {**CON_OPCIONES, "id": "eval-03"}])
    assert [(f["id"], f["acierta"], f["error"]) for f in filas] == [
        ("eval-02", True, None), ("eval-03", False, "TimeoutError")]
    assert "Opciones:\n- 30 días." in llm.mensajes[0][1].content


def test_juez():
    """El reporte del juez muestra la mediana de cada métrica y las respuestas con menos puntaje."""
    tabla = pd.DataFrame([
        {"id": "eval-01", "relevancia": 1.0, "motivo_relevancia": "ok", "fidelidad": 0.5, "motivo_fidelidad": "inventa un dato"},
        {"id": "eval-02", "relevancia": 1.0, "motivo_relevancia": "ok", "fidelidad": None, "motivo_fidelidad": None},
    ])
    texto = markdown_juez("antes", tabla)
    assert "Mediana 1.00, promedio 1.00, con 1: 2 de 2." in texto
    assert "| eval-01 | 0.50 | inventa un dato |" in texto
