"""Tests de la extracción del cuestionario. Usan renglones inventados, no el PDF real."""

from src.rag.evaluators.cuestionario import armar_preguntas, es_candidata


def renglon(texto, verde=False, negrita=False, continua=False, pagina=3):
    """Arma un renglón de prueba como los que devuelve leer_renglones."""
    return {"pagina": pagina, "texto": texto, "verde": verde, "negrita": negrita, "continua": continua}


TITULO = renglon("1) Preguntas para todas las clases: Seguridad", negrita=True)


def test_opciones_y_correcta():
    """Arma la pregunta con sus opciones, une la línea que continúa una opción y toma la verde como correcta."""
    preguntas = armar_preguntas([
        TITULO,
        renglon("¿A qué factor se deben la mayoría"),
        renglon("de los siniestros viales?", continua=True),
        renglon("A. Al humano,"),
        renglon("en especial.", verde=True, continua=True),
        renglon("B. Al vehicular."),
        renglon("C Al ambiental."),
    ])
    assert len(preguntas) == 1
    pregunta = preguntas[0]
    assert pregunta["pregunta"] == "¿A qué factor se deben la mayoría de los siniestros viales?"
    assert pregunta["opciones"] == ["Al humano, en especial.", "Al vehicular.", "Al ambiental."]
    assert pregunta["correctas"] == ["Al humano, en especial."]
    assert pregunta["seccion"] == "Preguntas para todas las clases: Seguridad"


def test_verdadero_falso_y_numero():
    """Las preguntas numeradas pierden el número, y una línea con número abre una pregunta nueva."""
    preguntas = armar_preguntas([
        TITULO,
        renglon("45) Complete la tabla de velocidades:"),
        renglon("46) Es recomendable frenar sobre zona resbaladiza."),
        renglon("• Verdadero."),
        renglon("• Falso.", verde=True),
    ])
    # La 45 no tiene opciones, así que se descarta y no se mezcla con la 46. Imita la
    # pregunta 137 del cuestionario (páginas 61 y 62), que es una tabla para completar.
    assert [p["pregunta"] for p in preguntas] == ["Es recomendable frenar sobre zona resbaladiza."]
    assert preguntas[0]["correctas"] == ["Falso."]


def test_imagen():
    """Una imagen entre el enunciado y las opciones marca la pregunta, que deja de ser candidata."""
    preguntas = armar_preguntas([
        renglon("PREGUNTAS GENERALES: CONVIVENCIA SEGURA", negrita=True),
        TITULO,
        renglon("¿Es correcta la detención del vehículo en este sector?"),
        {"pagina": 3, "imagen": True},
        renglon("A. Sí.", verde=True),
        renglon("B. No."),
    ])
    assert preguntas[0]["imagen"] is True
    assert preguntas[0]["parte"] == "general"
    assert not es_candidata(preguntas[0])
