"""Costo y latencia de cada pregunta: tokens, dólares y segundos de cada agente.

El costo es tokens por precio (los de config.yaml, de la página de OpenAI). No descuenta
la caché de OpenAI, así que el real puede ser algo menor.
"""


def costo(tokens_entrada: int, tokens_salida: int, precios: dict) -> float:
    """Dólares de una pregunta. Los precios son por millón de tokens, por lo que se divide por 1_000_000."""
    return (tokens_entrada * precios["precio_entrada"] + tokens_salida * precios["precio_salida"]) / 1_000_000


def tokens(usos: dict) -> dict:
    """Suma los tokens de todas las llamadas al LLM de una pregunta. El uso viene agrupado por modelo."""
    return {
        "tokens_entrada": sum(uso["input_tokens"] for uso in usos.values()),
        "tokens_salida": sum(uso["output_tokens"] for uso in usos.values()),
        "tokens_en_cache": sum(uso.get("input_token_details", {}).get("cache_read", 0) for uso in usos.values()),
    }


def segundos_por_agente(lineas: list[dict], sesion: str) -> dict:
    """Segundos del tutor y del verificador en una pregunta, sumando sus vueltas, según la auditoría.

    El tiempo del tutor incluye sus búsquedas en el manual.
    """
    de_la_sesion = [linea for linea in lineas if linea.get("sesion") == sesion]
    return {
        f"segundos_{agente}": round(sum(l["segundos"] for l in de_la_sesion if l["evento"] == agente), 2)
        for agente in ("tutor", "verificador")
    }
