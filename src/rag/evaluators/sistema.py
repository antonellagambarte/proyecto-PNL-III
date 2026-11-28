"""Evaluación del sistema completo.

Mide cada respuesta con reglas, sin otro LLM: si acertó (la respuesta final y el borrador del
tutor), si citó la página esperada, qué hizo la segunda vuelta, cuánto tardó y cuánto costó.
Después arma el resumen y los reportes.
"""

import json
import logging
import re
import time
import unicodedata
from uuid import uuid4

import pandas as pd

from src.policies.salida import igual
from src.rag.evaluators.costo import costo, segundos_por_agente, tokens

log = logging.getLogger(__name__)

# Los conjuntos de preguntas, en data/processed: las de práctica (para ajustar) y las del test final.
CONJUNTOS = {"practica": "preguntas_eval.jsonl", "test": "preguntas_test.jsonl"}

# Las páginas de una cita: «p. 57» o «p. 56–57».
PAGINAS = re.compile(r"p\. (\d+)(?:–(\d+))?")


def normalizar(texto: str) -> str:
    """Sin mayúsculas ni tildes, para buscar el dato clave sin que falle por eso."""
    sin_tildes = unicodedata.normalize("NFKD", texto.lower())
    return "".join(c for c in sin_tildes if not unicodedata.combining(c))


def trae_clave(clave: list[list[str]], texto: str) -> bool:
    """Si el texto trae todos los datos clave. De cada dato alcanza con una de sus variantes."""
    texto = normalizar(texto)
    return all(any(normalizar(variante) in texto for variante in dato) for dato in clave)


def acierta(pregunta: dict, opcion: str | None, texto: str = "") -> bool | None:
    """Si respondió bien: la opción correcta en las de opciones, o el dato clave en las libres.

    None si es libre y no tiene dato clave: no se puede saber sin leerla.
    """
    if pregunta["opciones"]:
        return bool(opcion) and igual(opcion, pregunta["correcta"])
    if pregunta.get("clave"):
        return trae_clave(pregunta["clave"], texto or "")
    return None


def paginas_citadas(citas: list[str]) -> set[int]:
    """Todas las páginas que nombran las citas."""
    paginas = set()
    for cita in citas:
        for inicio, fin in PAGINAS.findall(cita):
            paginas.update(range(int(inicio), int(fin or inicio) + 1))
    return paginas


def cita_pagina(pregunta: dict, citas: list[str]) -> bool | None:
    """Si citó alguna página donde está la respuesta. Si el manual no lo dice, no hay página esperada: None."""
    if not pregunta["paginas"]:
        return None
    return bool(paginas_citadas(citas) & set(pregunta["paginas"]))


def borrador_del_tutor(registro: list[dict]) -> tuple[str | None, str]:
    """La opción y el texto del tutor en la primera vuelta, antes de que el verificador los revise."""
    primero = next((paso for paso in registro if paso.get("agente") == "tutor"), {})
    return primero.get("opcion_elegida"), primero.get("respuesta", "")


def segunda_vuelta(pregunta: dict, respuesta: dict) -> str | None:
    """Qué hizo la segunda vuelta con la respuesta: la arregló, la arruinó o la dejó igual.

    None si hubo una sola vuelta o si no se puede saber si acertó (libre sin dato clave).
    """
    if respuesta["vueltas"] < 2:
        return None
    antes = acierta(pregunta, *borrador_del_tutor(respuesta["registro"]))
    despues = acierta(pregunta, respuesta["opcion_elegida"], respuesta["respuesta"])
    if antes is None or despues is None:
        return None
    if antes == despues:
        return "igual"
    return "arreglo" if despues else "arruino"


def evaluar(pregunta: dict, respuesta: dict) -> dict:
    """Lo que se mide de una respuesta con reglas."""
    return {
        "id": pregunta["id"],
        "forma": "opciones" if pregunta["opciones"] else "libre",
        "veredicto": respuesta["veredicto"],
        "vueltas": respuesta["vueltas"],
        "acierta": acierta(pregunta, respuesta["opcion_elegida"], respuesta["respuesta"]),
        "acierta_tutor_solo": acierta(pregunta, *borrador_del_tutor(respuesta["registro"])),
        "cita_pagina": cita_pagina(pregunta, respuesta["citas"]),
        "segunda_vuelta": segunda_vuelta(pregunta, respuesta),
        # Solo las preguntas del test tienen tipo (dato, combinar, premisa falsa, no lo dice, cuestionario).
        **({"tipo": pregunta["tipo"]} if "tipo" in pregunta else {}),
    }


def medir(sistema, preguntas: list[dict], config: dict, conjunto: str) -> tuple[list[dict], list[dict]]:
    """Responde cada pregunta y devuelve una fila con lo medido, y los textos para el juez y para leer qué pasó."""
    filas, textos = [], []
    for pregunta in preguntas:
        # Una sesión nueva por pregunta: no arrastra charla y permite encontrar sus pasos en la auditoría.
        sesion = f"eval-{uuid4().hex[:12]}"
        inicio = time.perf_counter()
        respuesta = sistema.responder(pregunta["pregunta"], pregunta["opciones"] or None, sesion)
        segundos = round(time.perf_counter() - inicio, 2)
        usados = tokens(respuesta["tokens"])
        filas.append({
            **evaluar(pregunta, respuesta),
            "segundos": segundos,
            **usados,
            "costo": round(costo(usados["tokens_entrada"], usados["tokens_salida"], config["llm"]), 6),
            "sesion": sesion,
            "conjunto": conjunto,
            "modelo": config["llm"]["modelo"],
            "k_candidatos": config["busqueda"]["k_candidatos"],
            "k_fragmentos": config["busqueda"]["k_fragmentos"],
        })
        # Los fragmentos que encontró quedan en el estado de la sesión. El juez los necesita para medir fidelidad.
        estado = sistema.grafo.get_state({"configurable": {"thread_id": sesion}}).values
        textos.append({
            "id": pregunta["id"], "pregunta": pregunta["pregunta"], "esperada": pregunta["correcta"],
            "respuesta": respuesta["respuesta"], "fragmentos": [f.texto for f in estado.get("fragmentos", [])],
            # Lo que hizo cada agente en cada vuelta, con el veredicto y el motivo del verificador.
            "registro": respuesta["registro"],
        })
        log.info("%s: %.1f s", pregunta["id"], segundos)

    # Cuánto tardó cada agente sale de la auditoría, que anota los segundos de cada paso.
    lineas = [json.loads(linea) for linea in sistema.auditoria.ruta.read_text(encoding="utf-8").splitlines()]
    for fila in filas:
        fila.update(segundos_por_agente(lineas, fila.pop("sesion")))
    return filas, textos


def similitud(modelo, respuestas: list[str], esperadas: list[str]) -> list[float]:
    """Semantic similarity entre cada respuesta y la esperada: el coseno entre sus embeddings."""
    from sentence_transformers import util

    # El modelo e5 pide el prefijo «query: » cuando se comparan dos textos del mismo tipo.
    vectores = lambda textos: modelo.encode([f"query: {t}" for t in textos], convert_to_tensor=True)
    return [round(float(valor), 3) for valor in util.pairwise_cos_sim(vectores(respuestas), vectores(esperadas))]


def de(columna: pd.Series) -> str:
    """Cuántos dieron sí entre los que se pueden medir: «33 de 35»."""
    medibles = columna.dropna().astype(bool)
    return f"{int(medibles.sum())} de {len(medibles)}"


def resumir(nombre: str, tabla: pd.DataFrame) -> dict:
    """Lo principal de una corrida: aciertos, promedios, medianas (p50), percentil 95 (p95) y totales.

    Lo que se suma (tokens y costo) y la calidad (semantic similarity) van en promedio por pregunta.
    Los tiempos van en p50 y p95, porque una pregunta lenta distorsiona el promedio.
    """
    p50 = lambda columna: tabla[columna].quantile(0.5)
    vueltas = tabla["segunda_vuelta"].dropna()
    return {
        "corrida": nombre,
        "conjunto": tabla["conjunto"].iloc[0],
        "candidatos": int(tabla["k_candidatos"].iloc[0]),
        "fragmentos": int(tabla["k_fragmentos"].iloc[0]),
        "preguntas": len(tabla),
        "aciertos": de(tabla["acierta"]),
        "aciertos_opciones": de(tabla.loc[tabla["forma"] == "opciones", "acierta"]),
        "aciertos_libres": de(tabla.loc[tabla["forma"] == "libre", "acierta"]),
        "aciertos_tutor_solo": de(tabla["acierta_tutor_solo"]),
        "cita_pagina": de(tabla["cita_pagina"]),
        "sin_respaldo": int((tabla["veredicto"] != "aprobada").sum()),
        "dos_vueltas": int((tabla["vueltas"] == 2).sum()),
        "arreglo_arruino": f"{int((vueltas == 'arreglo').sum())} / {int((vueltas == 'arruino').sum())}",
        "parecido_promedio": round(tabla["parecido"].mean(), 2),
        "segundos_p50": round(p50("segundos"), 1),
        "segundos_p95": round(tabla["segundos"].quantile(0.95), 1),
        "tutor_p50": round(p50("segundos_tutor"), 1),
        "verificador_p50": round(p50("segundos_verificador"), 1),
        "entrada_promedio": round(tabla["tokens_entrada"].mean()),
        "salida_promedio": round(tabla["tokens_salida"].mean()),
        "costo_promedio": round(tabla["costo"].mean(), 5),
        "costo_total": round(tabla["costo"].sum(), 4),
    }


def por_tipo(tabla: pd.DataFrame) -> list[dict]:
    """Los aciertos de cada tipo de pregunta, para ver en qué clase de pregunta falla."""
    return [{"tipo": tipo, "preguntas": len(grupo), "aciertos": de(grupo["acierta"]),
             "tutor_solo": de(grupo["acierta_tutor_solo"])}
            for tipo, grupo in tabla.groupby("tipo", sort=False)]


NOMBRES = {
    "corrida": "Corrida", "conjunto": "Preguntas de", "candidatos": "Candidatos", "fragmentos": "Fragmentos", "preguntas": "Preguntas",
    "aciertos": "Aciertos", "aciertos_opciones": "Aciertos con opciones", "aciertos_libres": "Aciertos libres (dato clave)",
    "aciertos_tutor_solo": "Aciertos del tutor solo",
    "cita_pagina": "Cita la página esperada", "sin_respaldo": "Sin respaldo", "dos_vueltas": "Con 2 vueltas",
    "arreglo_arruino": "La 2.ª vuelta arregló / arruinó", "parecido_promedio": "Semantic similarity (promedio)",
    "segundos_p50": "Segundos p50", "segundos_p95": "Segundos p95",
    "tutor_p50": "Tutor p50 (s)", "verificador_p50": "Verificador p50 (s)",
    "entrada_promedio": "Tokens de entrada (promedio)", "salida_promedio": "Tokens de salida (promedio)",
    "costo_promedio": "Costo por pregunta (promedio, US$)", "costo_total": "Costo total (US$)",
}

EXPLICACION = [
    "- **p50 y p95:** mediana y percentil 95.",
    "- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).",
    "- **Tutor solo:** el borrador de la primera vuelta, antes del verificador. Muestra cuántas habría acertado el sistema sin verificador.",
    "- **Semantic similarity:** coseno entre los embeddings de la respuesta y de la esperada, con el modelo de la búsqueda.",
    "- **Costo:** con los precios de `configs/config.yaml`, sin el descuento de OpenAI por caché. El costo real puede ser algo menor.",
]


def tabla_md(filas: list[dict], columnas: dict) -> list[str]:
    """Una tabla en markdown con las columnas dadas, en ese orden."""
    renglones = ["| " + " | ".join(columnas.values()) + " |", "|" + "---|" * len(columnas)]
    for fila in filas:
        renglones.append("| " + " | ".join("—" if pd.isna(fila[c]) else str(fila[c]) for c in columnas) + " |")
    return renglones


def markdown_corrida(nombre: str, tabla: pd.DataFrame) -> str:
    """El reporte de una corrida: los totales arriba y una fila por pregunta abajo."""
    resumen = resumir(nombre, tabla)
    por_pregunta = {
        "id": "Id", "forma": "Forma", "acierta": "¿Acertó?", "acierta_tutor_solo": "Tutor solo",
        "cita_pagina": "¿Citó la página?", "vueltas": "Vueltas", "segunda_vuelta": "2.ª vuelta",
        "veredicto": "Veredicto", "parecido": "Semantic similarity", "segundos": "Segundos",
        "tokens_entrada": "Tokens de entrada", "tokens_salida": "Tokens de salida", "costo": "Costo (US$)",
    }
    tipos = []
    if "tipo" in tabla:
        por_pregunta = {"id": "Id", "tipo": "Tipo", **por_pregunta}
        tipos = ["## Por tipo de pregunta", "",
                 *tabla_md(por_tipo(tabla), {"tipo": "Tipo", "preguntas": "Preguntas", "aciertos": "Aciertos",
                                             "tutor_solo": "Tutor solo"}), ""]
    filas = tabla.replace({True: "Sí", False: "**No**"}).to_dict("records")
    return "\n".join([
        f"# Evaluación: {nombre}",
        "",
        "Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_" + nombre + ".csv`.",
        "",
        *EXPLICACION,
        "",
        "## Totales",
        "",
        *tabla_md([{"medida": NOMBRES[c], "valor": v} for c, v in resumen.items() if c != "corrida"],
                  {"medida": "Medida", "valor": "Valor"}),
        "",
        *tipos,
        "## Por pregunta",
        "",
        *tabla_md(filas, por_pregunta),
        "",
    ])


def markdown_corridas(resumenes: list[dict]) -> str:
    """Una fila por corrida, para comparar antes y después de un cambio en la configuración."""
    return "\n".join([
        "# Corridas del sistema completo",
        "",
        "Cada corrida de `scripts.evaluar_sistema` suma una fila. Sirve para comparar antes y después de un cambio en `configs/config.yaml`.",
        "",
        *EXPLICACION,
        "",
        *tabla_md(resumenes, NOMBRES),
        "",
    ])
