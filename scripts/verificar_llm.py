"""Verifica que la API key de OpenAI y el modelo elegido respondan.

Uso:
    uv run --no-project scripts/verificar_llm.py [modelo]

Lee OPENAI_API_KEY de las variables de entorno o, si no está, del archivo
.env de la raíz del proyecto. Usa solo la biblioteca estándar, así que no
necesita instalar dependencias.
"""

import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
MODELO_POR_DEFECTO = "gpt-6-luna"
URL_RESPONSES = "https://api.openai.com/v1/responses"


def leer_env(ruta: Path) -> dict[str, str]:
    """Lee pares CLAVE=valor de un archivo .env, ignorando comentarios."""
    valores: dict[str, str] = {}
    if not ruta.exists():
        return valores
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if not linea or linea.startswith("#") or "=" not in linea:
            continue
        clave, valor = linea.split("=", 1)
        valores[clave.strip()] = valor.strip().strip('"').strip("'")
    return valores


def extraer_texto(respuesta: dict) -> str:
    """Junta el texto de los mensajes que devuelve la API de Responses."""
    partes = [
        contenido.get("text", "")
        for item in respuesta.get("output", [])
        if item.get("type") == "message"
        for contenido in item.get("content", [])
        if contenido.get("type") == "output_text"
    ]
    return " ".join(p for p in partes if p).strip()


def main() -> int:
    modelo = sys.argv[1] if len(sys.argv) > 1 else MODELO_POR_DEFECTO
    clave = os.getenv("OPENAI_API_KEY") or leer_env(RAIZ / ".env").get("OPENAI_API_KEY", "")
    if not clave:
        print("Falta OPENAI_API_KEY: copiá .env.example como .env y pegá la key.")
        return 1

    cuerpo = {
        "model": modelo,
        "instructions": "Respondé en una sola oración, en castellano.",
        "input": "¿Qué indica una luz amarilla intermitente en un semáforo?",
        "max_output_tokens": 800,
    }
    pedido = urllib.request.Request(
        URL_RESPONSES,
        data=json.dumps(cuerpo).encode("utf-8"),
        headers={"Authorization": f"Bearer {clave}", "Content-Type": "application/json"},
    )

    try:
        with urllib.request.urlopen(pedido, timeout=60) as resp:
            datos = json.load(resp)
    except urllib.error.HTTPError as error:
        try:
            detalle = json.loads(error.read() or b"{}").get("error", {})
        except json.JSONDecodeError:
            detalle = {}
        print(f"La API respondió con error {error.code}: {detalle.get('message', 'sin detalle')}")
        if error.code == 401:
            print("Revisá que la key esté bien copiada y que no esté vencida.")
        elif error.code == 429:
            print("Puede faltar saldo en Billing o haberse alcanzado un límite de uso.")
        elif error.code == 404:
            print(f"El modelo '{modelo}' no está disponible para esta cuenta.")
        return 1
    except urllib.error.URLError as error:
        print(f"No se pudo conectar con OpenAI: {error.reason}")
        return 1

    texto = extraer_texto(datos)
    uso = datos.get("usage", {})
    print(f"Modelo: {datos.get('model', modelo)}")
    print(f"Respuesta: {texto or '(vacía)'}")
    print(f"Tokens: {uso.get('input_tokens')} de entrada y {uso.get('output_tokens')} de salida")
    if datos.get("status") == "incomplete":
        motivo = (datos.get("incomplete_details") or {}).get("reason", "desconocido")
        print(f"Aviso: la respuesta quedó incompleta (motivo: {motivo}).")
    return 0 if texto else 1


if __name__ == "__main__":
    sys.exit(main())
