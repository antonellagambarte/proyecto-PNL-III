"""Extracción de las preguntas del cuestionario oficial del examen teórico.

El cuestionario marca la respuesta correcta en verde. Las opciones aparecen en cuatro
formatos: «A. B. C.», «a) b) c)», «• Verdadero / • Falso» y una línea «V F» con la letra
correcta en verde. Algunas preguntas dependen de una imagen, que en el PDF está entre
el enunciado y las opciones.
"""

import logging
import re
from collections import Counter
from pathlib import Path

import pdfplumber

log = logging.getLogger(__name__)

# Texto que se repite en todas las páginas. Se saca para que no se mezcle con las preguntas.
# El número de página va en la última línea, debajo del pie.
ENCABEZADO = ("Dirección Provincial", "de Política y Seguridad Vial")
PIE = "BATERÍA DE PREGUNTAS Y RESPUESTAS"

# Los valores fijos de este bloque se midieron en todo el cuestionario con
# scripts/explorar_cuestionario.py.

# Color de las letras de la respuesta correcta, en CMYK, como lo da pdfplumber. Las
# opciones correctas tienen todas este color, que en el PDF se ve verde.
VERDE = (0.48, 0.0, 0.89, 0.0)
# Casi todas las líneas arrancan a 0 a 3 puntos del margen, y las que continúan una opción,
# a 13 o 14. Entre 4 y 12 no hay ninguna.
SANGRIA = 8
# Las líneas de un mismo enunciado u opción están a 13 puntos, de una opción a la siguiente
# a 19, y entre el enunciado y las opciones o entre preguntas, a 26 o más. Entre 15 y 17 no
# hay ninguna.
INTERLINEADO = 16

# Línea que abre una sección del cuestionario, como "5) Preguntas para todas las clases: Semáforo".
# También reconoce "6) Peguntas para..." (sin la «r», como está escrito en el PDF) y el título en mayúsculas
# "PREGUNTAS ESPECÍFICAS SEGÚN CLASE", que separa las preguntas generales de las de cada clase.
TITULO = re.compile(r"^(?:\d+\)\s*)?(?:Pr?eguntas para|PREGUNTAS)")
# En negrita, un número con paréntesis también abre una sección. Ejemplo: "14) Seguridad Activa y Pasiva".
TITULO_NUMERADO = re.compile(r"^\d+\)\s")
# Opción. Ejemplos: "A. Al humano.", "c)Si, en forma irrestricta..." y "• Verdadero.".
# Algunas preguntas llegan hasta la opción g.
OPCION = re.compile(r"^(?:[A-Ha-h][.)]|•)\s*(.+)$")
# Opción sin punto después de la letra. Ejemplo: "C Por la esquina...".
OPCION_SIN_PUNTO = re.compile(r"^([A-H])\s+([A-ZÁÉÍÓÚÑ¿¡].*)$")
LETRAS = "ABCDEFGH"
# Número al principio de una pregunta. Ejemplo: "45) Excepcionalmente...".
NUMERO = re.compile(r"^\d+\)\s*")


def color_de(letras: list[dict]) -> tuple:
    """El color que tiene la mayoría de las letras, redondeado a dos decimales."""
    colores = Counter(tuple(round(c, 2) for c in (letra["non_stroking_color"] or ())) for letra in letras)
    return colores.most_common(1)[0][0] if colores else ()


def _es_verde(letras: list[dict]) -> bool:
    """Si la mayoría de las letras están en verde."""
    return color_de(letras) == VERDE


def _renglones_de_linea(linea: dict, pagina: int, continua: bool) -> list[dict]:
    """Convierte una línea del PDF en uno o dos renglones con lo que hace falta para armar las preguntas."""
    letras = linea["chars"]
    texto = linea["text"].strip()
    negrita = "Bold" in Counter(letra["fontname"] for letra in letras).most_common(1)[0][0]
    if texto == "V F":
        # La letra correcta está en verde. Se convierte en las dos opciones de siempre.
        return [
            {"pagina": pagina, "texto": f"• {opcion}", "verde": _es_verde([c for c in letras if c["text"] == letra]),
             "negrita": negrita, "continua": False}
            for letra, opcion in (("V", "Verdadero."), ("F", "Falso."))
        ]
    return [{"pagina": pagina, "texto": texto, "verde": _es_verde(letras), "negrita": negrita, "continua": continua}]


def lineas_de_contenido(pagina, numero: int) -> list[dict]:
    """Las líneas de una página sin el encabezado, el pie y el número de página."""
    lineas = pagina.extract_text_lines()
    if lineas and lineas[-1]["text"].strip() == str(numero):
        lineas = lineas[:-1]
    return [linea for linea in lineas if linea["text"].strip() not in (*ENCABEZADO, PIE)]


def leer_renglones(ruta_pdf: Path) -> list[dict]:
    """Lee el PDF y devuelve sus líneas y sus imágenes en el orden en que aparecen.

    Cada línea dice su página, su texto, si está en verde, si está en negrita y si continúa
    la línea de arriba. De las imágenes solo importa dónde aparecen, no qué muestran.
    """
    renglones = []
    with pdfplumber.open(str(ruta_pdf)) as pdf:
        for numero, pagina in enumerate(pdf.pages, start=1):
            lineas = lineas_de_contenido(pagina, numero)
            # El margen izquierdo cambia un poco de una página a otra.
            margen = min((linea["x0"] for linea in lineas), default=0)
            elementos = []
            for i, linea in enumerate(lineas):
                # Continúa la de arriba si está pegada, si está corrida a la derecha o si empieza
                # en minúscula (una opción que sigue en la página siguiente).
                pegada = i > 0 and linea["top"] - lineas[i - 1]["top"] < INTERLINEADO
                continua = pegada or linea["x0"] > margen + SANGRIA or linea["text"][:1].islower()
                elementos.append((linea["top"], _renglones_de_linea(linea, numero, continua)))
            elementos += [(imagen["top"], [{"pagina": numero, "imagen": True}]) for imagen in pagina.images]
            for _, grupo in sorted(elementos, key=lambda par: par[0]):
                renglones.extend(grupo)
    return renglones


def _opcion(texto: str, actual: dict | None) -> str | None:
    """Devuelve el texto de la opción, o None si el renglón no es una opción."""
    coincidencia = OPCION.match(texto)
    if coincidencia:
        return coincidencia.group(1)
    # Sin el punto, «A Sí...» podría ser el comienzo de una pregunta. Solo se toma como
    # opción si es la letra que sigue en la pregunta que se está armando.
    coincidencia = OPCION_SIN_PUNTO.match(texto)
    if coincidencia and actual is not None and len(actual["opciones"]) < len(LETRAS):
        if coincidencia.group(1) == LETRAS[len(actual["opciones"])]:
            return coincidencia.group(2)
    return None


def armar_preguntas(renglones: list[dict]) -> list[dict]:
    """Agrupa los renglones en preguntas con su sección, sus opciones y la respuesta correcta.

    Las preguntas con menos de dos opciones se descartan: son textos que no son preguntas,
    como la portada o la hoja de firmas, o tablas para completar.
    """
    preguntas = []
    parte = seccion = None
    actual = None  # La pregunta que se está armando.
    despues_de_titulo = False
    for renglon in renglones:
        if renglon.get("imagen"):
            if actual is not None and not actual["opciones"]:
                actual["imagen"] = True
            continue
        texto = renglon["texto"]
        if TITULO.match(texto) or (renglon["negrita"] and TITULO_NUMERADO.match(texto)):
            if texto.startswith("PREGUNTAS"):
                parte = "especifica" if "ESPEC" in texto else "general"
            else:
                seccion = NUMERO.sub("", texto)
            actual = None
            despues_de_titulo = True
            continue
        opcion = _opcion(texto, actual)
        if opcion is not None:
            if actual is not None:
                actual["opciones"].append({"texto": opcion, "verde": renglon["verde"]})
        elif renglon["continua"] and actual is not None and actual["opciones"]:
            # Sigue la opción anterior. A veces la marca verde está solo en esta línea.
            ultima = actual["opciones"][-1]
            ultima["texto"] += " " + texto
            ultima["verde"] = ultima["verde"] or renglon["verde"]
        elif renglon["negrita"]:
            # Un título que sigue en la línea de abajo, o un subtítulo como «USUARIOS DE BICICLETA».
            if despues_de_titulo and texto[:1].islower():
                seccion += " " + texto
            actual = None
        elif actual is None or actual["opciones"] or NUMERO.match(texto):
            # Empieza una pregunta nueva. Una línea con número siempre abre una, aunque la
            # anterior no tenga opciones (por ejemplo, una tabla para completar).
            actual = {
                "parte": parte,
                "seccion": seccion,
                "pagina": renglon["pagina"],
                "pregunta": NUMERO.sub("", texto),
                "opciones": [],
                "imagen": False,
            }
            preguntas.append(actual)
        else:
            actual["pregunta"] += " " + texto
        despues_de_titulo = False

    completas = []
    for numero, pregunta in enumerate((p for p in preguntas if len(p["opciones"]) >= 2), start=1):
        opciones = pregunta.pop("opciones")
        completas.append({
            "id": f"cuestionario-{numero:03d}",
            **pregunta,
            "opciones": [o["texto"] for o in opciones],
            "correctas": [o["texto"] for o in opciones if o["verde"]],
        })
    return completas


def extraer_preguntas(ruta_pdf: Path) -> list[dict]:
    """Lee el cuestionario y devuelve todas sus preguntas."""
    preguntas = armar_preguntas(leer_renglones(ruta_pdf))
    log.info("Cuestionario: %d preguntas", len(preguntas))
    return preguntas


def es_candidata(pregunta: dict) -> bool:
    """Si la pregunta sirve para el dataset: de auto particular, sin imagen y con una sola respuesta correcta.

    Sirven las preguntas generales (salvo las de tracción a sangre) y las de la sección
    de auto y camioneta. Las de motos, camiones, taxis y otras clases quedan afuera.
    """
    seccion = (pregunta["seccion"] or "").lower()
    de_auto = (pregunta["parte"] == "general" and "sangre" not in seccion) or "auto y camioneta" in seccion
    return de_auto and not pregunta["imagen"] and len(pregunta["correctas"]) == 1
