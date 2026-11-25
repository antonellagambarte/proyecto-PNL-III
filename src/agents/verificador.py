"""El verificador: revisa la respuesta del tutor contra los fragmentos y decide el veredicto.

No tiene herramientas. Responde con un Veredicto de formato fijo (salida estructurada).
"""

from langchain_core.messages import HumanMessage, SystemMessage

from src.agents.esquemas import Estado, Veredicto
from src.agents.memoria import formatear_conversacion
from src.agents.prompts import VERIFICADOR
from src.tools.builtin.buscar_en_manual import formatear


def mensaje_para_verificador(estado: Estado) -> str:
    """Arma lo que recibe el verificador, cada parte entre marcas.

    La charla anterior (si hay), la pregunta, las consultas que hizo el tutor, el borrador y
    los fragmentos. Con las consultas sabe si ya se buscó más de una vez.
    """
    borrador = estado["borrador"]
    opciones = "\n".join(f"- {opcion}" for opcion in estado["opciones"] or [])
    charla = ""
    if estado["conversacion_resumida"]:
        charla = f"Charla anterior:\n{formatear_conversacion(estado['conversacion_resumida'])}\n\n"
    consultas = [c for paso in estado["registro"] if paso["agente"] == "tutor" for c in paso["consultas"] if c]
    buscado = "\n".join(f"- {consulta}" for consulta in consultas) or "-"
    return (
        f"{charla}<pregunta>\n{estado['pregunta']}\n{opciones}\n</pregunta>\n\n"
        f"<consultas>\n{buscado}\n</consultas>\n\n"
        f"<borrador>\nRespuesta: {borrador.respuesta}\n"
        f"Opción elegida: {borrador.opcion_elegida or '-'}\n"
        f"Citas: {', '.join(borrador.citas) or '-'}\n</borrador>\n\n"
        f"Fragmentos del manual:\n{formatear(estado['fragmentos'])}"
    )


class Verificador:
    """Nodo del grafo que corre el verificador."""

    def __init__(self, llm):
        self.llm = llm.with_structured_output(Veredicto)

    def __call__(self, estado: Estado) -> dict:
        mensajes = [SystemMessage(VERIFICADOR), HumanMessage(mensaje_para_verificador(estado))]
        veredicto = self.llm.invoke(mensajes)
        return {
            "veredicto": veredicto,
            "registro": estado["registro"] + [{
                "agente": "verificador", "vuelta": estado["vueltas"], "veredicto": veredicto.veredicto,
                "motivo": veredicto.motivo, "consulta_sugerida": veredicto.consulta_sugerida,
            }],
        }
