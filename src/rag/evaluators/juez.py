"""El reporte del juez: Answer Relevancy y Faithfulness de DeepEval, que usan un LLM como juez.

Las métricas se calculan en scripts.juzgar_respuestas, que es el único lugar que importa
DeepEval (no es dependencia del proyecto). Acá solo se resume lo que guardó.
"""

import pandas as pd

METRICAS = {
    "relevancia": "Answer Relevancy: si la respuesta contesta lo que se preguntó, sin irse por las ramas",
    "fidelidad": "Faithfulness: si lo que afirma la respuesta está en los fragmentos que encontró el sistema",
}


def markdown_juez(nombre: str, tabla: pd.DataFrame, peores: int = 5) -> str:
    """Para cada métrica: mediana, promedio, cuántas sacaron 1 y las de puntaje más bajo con el motivo del juez."""
    renglones = [
        f"# Juez: {nombre}",
        "",
        "Se genera con `uv run --with deepeval python -m scripts.juzgar_respuestas " + nombre + "`. "
        "El juez es el mismo modelo del sistema, así que puede ser indulgente con sus propias respuestas.",
        "",
    ]
    for metrica, explicacion in METRICAS.items():
        notas = tabla[metrica].dropna()
        renglones += [
            f"## {explicacion.split(':')[0]}",
            "",
            explicacion.split(": ", 1)[1].capitalize() + ".",
            "",
            f"- Mediana {notas.median():.2f}, promedio {notas.mean():.2f}, con 1: {int((notas == 1).sum())} de {len(notas)}.",
            "",
            "| Id | Puntaje | Motivo del juez |",
            "|---|---|---|",
        ]
        for _, fila in tabla.dropna(subset=[metrica]).nsmallest(peores, metrica).iterrows():
            motivo = str(fila[f"motivo_{metrica}"]).replace("|", "\\|").replace("\n", " ")
            renglones.append(f"| {fila['id']} | {fila[metrica]:.2f} | {motivo} |")
        renglones.append("")
    return "\n".join(renglones)
