"""Parseo del manual del conductor: del PDF a secciones con su texto y sus páginas.

Adaptado del lector de PDF del código de la cátedra. Además de leer el PDF página
por página, saca el encabezado y el pie del manual, detecta capítulos y secciones,
y deja afuera los capítulos que no son de auto particular.
"""

import json
import logging
import re
from pathlib import Path

import pdfplumber

log = logging.getLogger(__name__)

# Texto que se repite en todas las páginas. Se saca para que no ensucie los chunks.
# El número de página no se pierde: queda en los metadatos.
ENCABEZADO = ["Dirección Provincial", "de Política y Seguridad Vial"]
PIE = "MANUAL DEL CONDUCTOR"
# Motocicleta (8) y triciclos y cuatriciclos (9). El proyecto es para auto particular.
CAPITULOS_EXCLUIDOS = {8, 9}

# Línea del índice de la página 2. Ejemplo: "CAPITULO 3 SEÑALAMIENTO VIAL 39".
CAPITULO_EN_INDICE = re.compile(r"^CAP[IÍ]TULO (\d+) (.+) (\d+)$")
# Línea del índice final. Ejemplo: "3.2 SEÑALES VERTICALES 42". A veces falta la página.
SECCION_EN_INDICE = re.compile(r"^(\d{1,2}\.\d{1,2}) (.+?)(?: (\d+))?$")
# En el texto, el número de sección va solo en una línea. Ejemplo: "3.2".
NUMERO_DE_SECCION = re.compile(r"^(\d{1,2})\.(\d{1,2})$")
# Palabra cortada con guion al final de una línea. Ejemplo: "des-\ntrezas".
GUION_AL_FINAL = re.compile(r"(\w)-\n(\w)")


def leer_paginas(ruta_pdf: Path) -> list[list[str]]:
    """Devuelve las líneas de texto de cada página. La posición 0 es la página 1."""
    with pdfplumber.open(str(ruta_pdf)) as pdf:
        return [
            [linea.strip() for linea in (pagina.extract_text() or "").splitlines() if linea.strip()]
            for pagina in pdf.pages
        ]


def limpiar_pagina(lineas: list[str], numero: int) -> list[str]:
    """Saca el encabezado y el pie que se repiten en todas las páginas del manual."""
    if lineas[:2] == ENCABEZADO:
        lineas = lineas[2:]
    limpias = []
    saltear_numero = False
    for linea in lineas:
        if linea == PIE:
            # El número de página viene justo después del pie.
            saltear_numero = True
            continue
        if saltear_numero and linea == str(numero):
            saltear_numero = False
            continue
        saltear_numero = False
        limpias.append(linea)
    return limpias


def leer_transcripciones(ruta: Path) -> dict[int, list[str]]:
    """Lee las tablas transcriptas a mano. Devuelve las líneas de cada página corregida."""
    with Path(ruta).open(encoding="utf-8") as archivo:
        datos = json.load(archivo)
    return {int(pagina): entrada["texto"] for pagina, entrada in datos["paginas"].items()}


def aplicar_transcripcion(lineas: list[str], transcripcion: list[str]) -> list[str]:
    """Reemplaza el texto mal extraído de una página por su transcripción manual.

    Si en la página empieza una sección, se conservan su número y su título.
    """
    for i, linea in enumerate(lineas):
        if NUMERO_DE_SECCION.match(linea):
            return lineas[i:i + 2] + transcripcion
    return list(transcripcion)


def leer_capitulos(lineas_indice: list[str]) -> dict[int, dict]:
    """Lee el índice de la página 2: título y página de inicio de cada capítulo."""
    capitulos = {}
    for linea in lineas_indice:
        coincidencia = CAPITULO_EN_INDICE.match(linea)
        if coincidencia:
            numero, titulo, pagina = coincidencia.groups()
            capitulos[int(numero)] = {"titulo": titulo, "pagina": int(pagina)}
    return capitulos


def leer_titulos_de_secciones(lineas_indice: list[str]) -> dict[str, str]:
    """Lee los títulos de las secciones del índice final. Ese índice está incompleto."""
    titulos = {}
    for linea in lineas_indice:
        coincidencia = SECCION_EN_INDICE.match(linea)
        if coincidencia:
            titulos[coincidencia.group(1)] = coincidencia.group(2)
    return titulos


def unir_lineas(lineas: list[str]) -> str:
    """Une las líneas en un texto y junta las palabras cortadas con guion."""
    return GUION_AL_FINAL.sub(r"\1\2", "\n".join(lineas))


def capitulo_de_pagina(pagina: int, capitulos: dict[int, dict]) -> int | None:
    """Devuelve el capítulo al que pertenece una página, según el índice."""
    actual = None
    for numero, datos in sorted(capitulos.items(), key=lambda item: item[1]["pagina"]):
        if datos["pagina"] <= pagina:
            actual = numero
    return actual


def separar_secciones(
    paginas: dict[int, list[str]],
    capitulos: dict[int, dict],
    titulos: dict[str, str],
) -> list[dict]:
    """Recorre las páginas ya limpias y arma una lista de secciones con su texto por página.

    El texto de un capítulo que aparece antes de su primera sección queda como una
    sección sin número.
    """
    secciones = []
    actual = None
    for numero_pagina in sorted(paginas):
        capitulo = capitulo_de_pagina(numero_pagina, capitulos)
        if capitulo is None or capitulo in CAPITULOS_EXCLUIDOS:
            actual = None
            continue
        if numero_pagina == capitulos[capitulo]["pagina"]:
            # Es la portada del capítulo: solo tiene el número y el título.
            actual = None
            continue
        lineas = paginas[numero_pagina]
        acumuladas = []
        for i, linea in enumerate(lineas):
            coincidencia = NUMERO_DE_SECCION.match(linea)
            if coincidencia and int(coincidencia.group(1)) == capitulo:
                # Un título en mayúsculas justo antes del número es de la sección nueva.
                arrastre = [acumuladas.pop()] if acumuladas and acumuladas[-1].isupper() else []
                # Empieza una sección nueva: lo acumulado es de la anterior.
                if actual is not None and acumuladas:
                    actual["paginas"].append({"pagina": numero_pagina, "texto": unir_lineas(acumuladas)})
                acumuladas = arrastre
                siguiente = lineas[i + 1] if i + 1 < len(lineas) else None
                actual = {
                    "capitulo": capitulo,
                    "titulo_capitulo": capitulos[capitulo]["titulo"],
                    "seccion": linea,
                    "titulo_seccion": titulos.get(linea, siguiente),
                    "paginas": [],
                }
                secciones.append(actual)
                continue
            if actual is None or actual["capitulo"] != capitulo:
                actual = {
                    "capitulo": capitulo,
                    "titulo_capitulo": capitulos[capitulo]["titulo"],
                    "seccion": None,
                    "titulo_seccion": None,
                    "paginas": [],
                }
                secciones.append(actual)
            acumuladas.append(linea)
        if actual is not None and acumuladas:
            actual["paginas"].append({"pagina": numero_pagina, "texto": unir_lineas(acumuladas)})
    return [s for s in secciones if s["paginas"]]


def parsear_manual(ruta_pdf: Path, ruta_transcripciones: Path | None = None) -> list[dict]:
    """Lee el manual y devuelve sus secciones, sin los capítulos excluidos.

    Si se indica un archivo de transcripciones, esas páginas usan el texto transcripto
    a mano y quedan marcadas con origen "transcripcion_manual".
    """
    todas = leer_paginas(ruta_pdf)
    log.info("Se leyeron %d páginas de %s", len(todas), Path(ruta_pdf).name)
    transcripciones = leer_transcripciones(ruta_transcripciones) if ruta_transcripciones else {}

    capitulos = leer_capitulos(todas[1])
    # El contenido termina donde empieza el índice final.
    inicio_indice_final = next(
        numero for numero, lineas in enumerate(todas, start=1) if numero > 2 and "INDICE" in lineas
    )
    lineas_indice_final = [linea for lineas in todas[inicio_indice_final - 1:] for linea in lineas]
    titulos = leer_titulos_de_secciones(lineas_indice_final)

    paginas = {
        numero: limpiar_pagina(lineas, numero)
        for numero, lineas in enumerate(todas, start=1)
        if numero < inicio_indice_final and lineas
    }
    for numero, transcripcion in transcripciones.items():
        paginas[numero] = aplicar_transcripcion(paginas.get(numero, []), transcripcion)
    log.info("Se usaron transcripciones manuales en las páginas %s", sorted(transcripciones))

    secciones = separar_secciones(paginas, capitulos, titulos)
    for seccion in secciones:
        for pagina in seccion["paginas"]:
            pagina["origen"] = "transcripcion_manual" if pagina["pagina"] in transcripciones else "pdf"
    log.info(
        "Se armaron %d secciones de %d capítulos (excluidos: %s)",
        len(secciones),
        len({s["capitulo"] for s in secciones}),
        sorted(CAPITULOS_EXCLUIDOS),
    )
    return secciones
