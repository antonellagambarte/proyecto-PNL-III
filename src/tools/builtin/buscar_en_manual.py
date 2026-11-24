"""Herramienta del tutor: buscar en el manual.

Es de solo lectura y usa la búsqueda híbrida del sistema (src/rag/retrievers/hibrida.py).
Devuelve los fragmentos entre marcas, para que el modelo los lea como datos del manual y
no como instrucciones.
"""

from langchain_core.tools import tool
from pydantic import BaseModel, Field

from src.agents.esquemas import Fragmento


def formatear(fragmentos: list[Fragmento]) -> str:
    """Arma el texto que recibe el tutor: cada fragmento entre marcas, con su id y su cita."""
    if not fragmentos:
        return "No se encontraron fragmentos del manual para esta consulta."
    bloques = []
    for fragmento in fragmentos:
        bloques.append(f'<fragmento id="{fragmento.id}" cita="{fragmento.cita}">\n{fragmento.texto}\n</fragmento>')
    return "\n\n".join(bloques)


def crear_buscar_en_manual(buscador, k_max: int):
    """Crea la herramienta del tutor a partir del buscador.

    El buscador llega ya creado, con los modelos en memoria, porque cargarlos tarda
    varios segundos y se hace una sola vez al arrancar el sistema. La herramienta lo usa
    por dentro: el modelo solo le pasa la consulta y cuántos fragmentos quiere, entre 1 y k_max.
    """

    class Entrada(BaseModel):
        consulta: str = Field(description="Qué buscar, escrito con las palabras que usaría el manual.")
        k: int = Field(default=k_max, ge=1, le=k_max, description=f"Cuántos fragmentos traer, entre 1 y {k_max}.")

    @tool("buscar_en_manual", args_schema=Entrada, response_format="content_and_artifact")
    def buscar_en_manual(consulta: str, k: int = k_max) -> tuple[str, list[Fragmento]]:
        """Busca en el manual del conductor de la Provincia de Buenos Aires (edición 2019).

        Devuelve los fragmentos más relevantes, cada uno con su id y su cita.
        """
        fragmentos = [
            Fragmento(id=r["id"], cita=r["cita"], texto=r["texto"]) for r in buscador.buscar(consulta, k)
        ]
        # El texto va al modelo. La lista de fragmentos queda aparte, para el verificador.
        return formatear(fragmentos), fragmentos

    return buscar_en_manual
