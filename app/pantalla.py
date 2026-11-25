"""La pantalla del asistente: un chat en Streamlit que le habla a la API.

Uso, desde la raíz del proyecto y con la API ya levantada:
    uv run python -m streamlit run app/pantalla.py
"""

import httpx
import streamlit as st

from src.common.config import cargar_config

URL_API = cargar_config()["pantalla"]["url_api"]
VEREDICTOS = {"aprobada": "aprobó la respuesta", "corregir": "pidió corregirla", "buscar_mas": "pidió buscar más"}


def preguntar(pregunta: str, sesion: str | None) -> dict:
    """Le manda la pregunta a la API. Si algo sale mal, devuelve el error con un mensaje para mostrar."""
    try:
        # Sin tiempo máximo: la API ya tiene el suyo para cada llamada al LLM.
        respuesta = httpx.post(f"{URL_API}/consultas", json={"pregunta": pregunta, "sesion": sesion}, timeout=None)
    except httpx.ConnectError:
        return {"error": "La API no está encendida. Levantala con: uv run uvicorn app.main:app"}
    if respuesta.status_code != 200:
        return {"error": "No se pudo responder en este momento. Probá de nuevo en unos minutos."}
    return respuesta.json()


def mostrar_pasos(datos: dict) -> None:
    """El desplegable con lo que hizo cada agente en cada vuelta."""
    with st.expander("Cómo se llegó a la respuesta"):
        for paso in datos["pasos"]:
            if paso["agente"] == "tutor":
                st.markdown(f"**Tutor, vuelta {paso['vuelta']}**")
                for consulta in paso["consultas"]:
                    st.markdown(f"- Buscó en el manual: «{consulta}»")
                st.markdown(f"- Escribió: {paso['respuesta']}")
            else:
                st.markdown(f"**Verificador, vuelta {paso['vuelta']}**: {VEREDICTOS[paso['veredicto']]}")
                st.markdown(f"- {paso['motivo']}")
        m = datos["metricas"]
        st.caption(f"{m['segundos']:.0f} segundos · {m['tokens_entrada']} tokens de entrada y {m['tokens_salida']} de salida")


def mostrar_respuesta(datos: dict) -> None:
    """La respuesta con la opción elegida, si hay, las citas y los pasos."""
    if "error" in datos:
        st.error(datos["error"])
        return
    st.markdown(datos["respuesta"])
    if datos["opcion_elegida"]:
        st.markdown(f"**Opción elegida:** {datos['opcion_elegida']}")
    for cita in datos["citas"]:
        st.caption(f"📖 {cita}")
    mostrar_pasos(datos)


def empezar_charla() -> None:
    """Borra la charla de la pantalla. La próxima pregunta abre una sesión nueva."""
    st.session_state.charla = []
    st.session_state.sesion = None


st.set_page_config(page_title="Asistente de manejo PBA", page_icon="🚗")
st.title("Asistente para el examen de conducir")
st.caption("Responde según el manual del conductor de la Provincia de Buenos Aires, edición 2019. Las normas pueden haber cambiado desde entonces.")

# Streamlit vuelve a correr todo el archivo en cada interacción: la charla se guarda entre una y otra.
if "charla" not in st.session_state:
    empezar_charla()
st.sidebar.button("Nueva charla", on_click=empezar_charla)

for turno in st.session_state.charla:
    st.chat_message("user").markdown(turno["pregunta"])
    with st.chat_message("assistant"):
        mostrar_respuesta(turno["datos"])

pregunta = st.chat_input("Escribí tu pregunta, con o sin opciones")
if pregunta:
    st.chat_message("user").markdown(pregunta)
    with st.chat_message("assistant"):
        with st.spinner("Buscando en el manual…"):
            datos = preguntar(pregunta, st.session_state.sesion)
        mostrar_respuesta(datos)
    st.session_state.charla.append({"pregunta": pregunta, "datos": datos})
    st.session_state.sesion = datos.get("sesion", st.session_state.sesion)
