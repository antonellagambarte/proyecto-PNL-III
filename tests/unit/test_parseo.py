"""Tests del parseo del manual. Usan textos chicos inventados, no el PDF real."""

from src.rag.ingestion.parseo import (
    aplicar_transcripcion,
    leer_capitulos,
    limpiar_pagina,
    separar_secciones,
    unir_lineas,
)

ENCABEZADO = ["Dirección Provincial", "de Política y Seguridad Vial"]

# Índice inventado: el capítulo 1 empieza en la página 3, el 8 en la 6 y el 10 en la 8.
CAPITULOS = {
    1: {"titulo": "EL CONDUCTOR", "pagina": 3},
    8: {"titulo": "FUNCIONAMIENTO DE LA MOTOCICLETA", "pagina": 6},
    10: {"titulo": "LAS INFRACCIONES DE TRANSITO", "pagina": 8},
}


def test_encabezado_y_pie():
    """Se sacan el encabezado, el pie y el número de página que lo sigue."""
    lineas = ENCABEZADO + ["Texto de la página.", "MANUAL DEL CONDUCTOR", "12"]
    assert limpiar_pagina(lineas, 12) == ["Texto de la página."]


def test_numero_de_lista():
    """Un número suelto que es parte del texto no se borra, aunque coincida con la página."""
    lineas = ENCABEZADO + ["5", "Abonar los aranceles.", "MANUAL DEL CONDUCTOR", "5"]
    assert limpiar_pagina(lineas, 5) == ["5", "Abonar los aranceles."]


def test_palabra_cortada():
    """Una palabra cortada con guion al final de una línea se une."""
    assert unir_lineas(["Conocimientos y des-", "trezas necesarias."]) == "Conocimientos y destrezas necesarias."


def test_capitulos_del_indice():
    """Del índice salen el número, el título y la página de inicio de cada capítulo."""
    indice = ["INDICE GENERAL", "CAPÍTULO 1 EL CONDUCTOR 3", "CAPITULO 2 LA VÍA PÚBLICA 25"]
    assert leer_capitulos(indice) == {
        1: {"titulo": "EL CONDUCTOR", "pagina": 3},
        2: {"titulo": "LA VÍA PÚBLICA", "pagina": 25},
    }


def test_secciones():
    """Las secciones se cortan en cada número de sección y guardan el texto por página."""
    paginas = {
        3: ["1", "CAPITULO EL CONDUCTOR"],  # portada del capítulo: se saltea
        4: ["1.1", "RESPONSABILIDAD SOCIAL", "Texto de 1.1."],
        5: ["Sigue 1.1.", "1.2", "CLASES DE LICENCIA", "Texto de 1.2."],
    }
    titulos = {"1.1": "RESPONSABILIDAD SOCIAL DEL CONDUCTOR"}
    secciones = separar_secciones(paginas, CAPITULOS, titulos)

    assert [s["seccion"] for s in secciones] == ["1.1", "1.2"]
    # El título sale del índice final si está ahí, y si no, de la línea que sigue al número.
    assert secciones[0]["titulo_seccion"] == "RESPONSABILIDAD SOCIAL DEL CONDUCTOR"
    assert secciones[1]["titulo_seccion"] == "CLASES DE LICENCIA"
    assert [p["pagina"] for p in secciones[0]["paginas"]] == [4, 5]
    assert secciones[0]["paginas"][1]["texto"] == "Sigue 1.1."


def test_capitulos_excluidos():
    """Las páginas de los capítulos 8 y 9 quedan afuera."""
    paginas = {
        4: ["1.1", "RESPONSABILIDAD SOCIAL", "Texto de auto."],
        7: ["8.1", "LA MOTOCICLETA", "Texto de moto."],
        9: ["10.1", "LAS PROHIBICIONES", "Texto de infracciones."],
    }
    secciones = separar_secciones(paginas, CAPITULOS, {})
    assert [s["capitulo"] for s in secciones] == [1, 10]


def test_titulo_antes_del_numero():
    """Una línea en mayúsculas justo antes del número de sección pasa a la sección nueva."""
    paginas = {
        4: ["1.1", "TÍTULO", "Final de 1.1.", "EN ZONA URBANA", "1.2", "Texto de 1.2."],
    }
    secciones = separar_secciones(paginas, CAPITULOS, {})
    assert secciones[0]["paginas"][0]["texto"] == "TÍTULO\nFinal de 1.1."
    assert secciones[1]["paginas"][0]["texto"].startswith("EN ZONA URBANA")


def test_transcripcion():
    """La transcripción reemplaza el texto de la página y conserva el número y el título de la sección."""
    transcripcion = ["Luz 1, frontal, baja."]
    con_seccion = aplicar_transcripcion(["4.4", "USO DE LAS LUCES", "al l c a a rg"], transcripcion)
    assert con_seccion == ["4.4", "USO DE LAS LUCES", "Luz 1, frontal, baja."]
    assert aplicar_transcripcion(["ANABRU LARUR"], transcripcion) == transcripcion
