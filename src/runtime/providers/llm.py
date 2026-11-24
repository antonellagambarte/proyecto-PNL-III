"""El modelo de lenguaje (LLM) del sistema.

Se crea en un solo lugar, con el modelo y sus parámetros de configs/config.yaml. Así se
puede cambiar de modelo o de proveedor sin tocar el resto del código.
"""

from langchain_openai import ChatOpenAI

from src.common.config import obtener_api_key


def crear_llm(config: dict) -> ChatOpenAI:
    """Crea el LLM con el modelo, el tiempo máximo de espera y los reintentos de la configuración."""
    llm = config["llm"]
    return ChatOpenAI(
        model=llm["modelo"],
        timeout=llm["timeout_segundos"],
        max_retries=llm["reintentos"],
        api_key=obtener_api_key(),
    )
