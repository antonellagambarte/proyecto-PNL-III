"""Exploración del cuestionario.

Uso, desde la raíz del proyecto:
    uv run python -m scripts.explorar_cuestionario

Recorre todo el PDF y muestra tres medidas que se usan en src/rag/evaluators/cuestionario.py:
1. Los colores de las letras: el de las respuestas correctas es VERDE.
2. La distancia entre una línea y la siguiente, y qué tipo de líneas son: INTERLINEADO.
3. Cuánto se corre cada línea respecto del margen izquierdo, con ejemplos: SANGRIA.

En la medida 2, «opción» es una línea que empieza como opción («A.», «b)», «•») y «texto»
es cualquier otra: un enunciado, la segunda línea de una opción o un título.
"""

from collections import Counter, defaultdict

import pdfplumber

from src.common.config import cargar_config, resolver_ruta
from src.rag.evaluators.cuestionario import OPCION, color_de, lineas_de_contenido

# Desde cuántas apariciones una distancia se muestra con su detalle. Las demás se listan juntas.
FRECUENTE = 5


def tipo(linea: dict) -> str:
    """«opción» si la línea empieza como una opción, «texto» si no."""
    return "opción" if OPCION.match(linea["text"].strip()) else "texto"


def main() -> None:
    ruta = resolver_ruta(cargar_config()["rutas"]["cuestionario"])
    colores, ejemplos_de_color = Counter(), {}
    # Para cada distancia, cuántos pares de líneas hay de cada tipo y un ejemplo de cada tipo.
    distancias, ejemplos_de_distancia = defaultdict(Counter), {}
    # Para cada corrimiento, cuántas líneas hay y dos de ejemplo.
    corrimientos, ejemplos_de_corrimiento = Counter(), defaultdict(list)

    with pdfplumber.open(str(ruta)) as pdf:
        # La primera página es la portada y la última, la hoja de firmas.
        for numero, pagina in enumerate(pdf.pages[1:-1], start=2):
            for letra in pagina.chars:
                colores[(letra["ncs"], color_de([letra]))] += 1
            lineas = lineas_de_contenido(pagina, numero)
            for linea in lineas:
                color = (linea["chars"][0]["ncs"], color_de(linea["chars"]))
                if len(ejemplos_de_color.setdefault(color, [])) < 3:
                    ejemplos_de_color[color].append(f"p. {numero}: {linea['text'].strip()[:80]}")
            if not lineas:
                continue
            for arriba, abajo in zip(lineas, lineas[1:]):
                distancia = round(abajo["top"] - arriba["top"])
                par = f"{tipo(arriba)} → {tipo(abajo)}"
                distancias[distancia][par] += 1
                ejemplos_de_distancia.setdefault(
                    (distancia, par),
                    f"p. {numero}: «{arriba['text'].strip()[:35]}» → «{abajo['text'].strip()[:35]}»",
                )
            margen = min(linea["x0"] for linea in lineas)
            for linea in lineas:
                corrimiento = round(linea["x0"] - margen)
                corrimientos[corrimiento] += 1
                if len(ejemplos_de_corrimiento[corrimiento]) < 2:
                    ejemplos_de_corrimiento[corrimiento].append(f"p. {numero}: {linea['text'].strip()[:50]}")

    print("1. Colores de las letras (espacio de color y valor)")
    for color, cantidad in colores.most_common():
        print(f"   {color[0]} {color[1]}: {cantidad} letras")
        for ejemplo in ejemplos_de_color.get(color, ["(solo en el encabezado, el pie o partes de una línea)"]):
            print(f"      {ejemplo}")

    print("\n2. Distancia entre una línea y la siguiente, en puntos")
    poco_frecuentes, mas_de_60 = [], 0
    for distancia in sorted(distancias):
        pares = distancias[distancia]
        total = sum(pares.values())
        if total < FRECUENTE:
            if distancia > 60:
                mas_de_60 += total
            else:
                poco_frecuentes.append(f"{distancia}: {total}")
            continue
        detalle = ", ".join(f"{par}: {veces}" for par, veces in pares.most_common())
        print(f"   {distancia}: {total} veces ({detalle})")
        print(f"      {ejemplos_de_distancia[(distancia, pares.most_common(1)[0][0])]}")
    print(f"   Menos de {FRECUENTE} veces, hasta 60 puntos: {' | '.join(poco_frecuentes)}")
    print(f"   Menos de {FRECUENTE} veces, más de 60 puntos: {mas_de_60} en total")

    print("\n3. Corrimiento de cada línea respecto del margen izquierdo, en puntos")
    for corrimiento in sorted(corrimientos):
        print(f"   {corrimiento}: {corrimientos[corrimiento]} líneas")
        for ejemplo in ejemplos_de_corrimiento[corrimiento]:
            print(f"      {ejemplo}")


if __name__ == "__main__":
    main()
