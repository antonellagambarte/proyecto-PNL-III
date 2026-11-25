"""Tests de los esquemas y de la herramienta del tutor. Usan un buscador y un modelo falsos."""

import pytest
from langchain_core.language_models.fake_chat_models import GenericFakeChatModel
from langchain_core.messages import AIMessage
from pydantic import ValidationError

from src.agents.esquemas import Fragmento, RespuestaTutor, Veredicto
from src.agents.tutor import Tutor
from src.graphs.workflows.tutor_verificador import entrada
from src.tools.builtin.buscar_en_manual import crear_buscar_en_manual, formatear


class BuscadorFalso:
    """Reemplaza a la búsqueda: devuelve siempre los mismos fragmentos."""

    def buscar(self, consulta, k):
        return [
            {"id": "pba2019-c04-s4.3-002", "cita": "cap. 4, secc. 4.3, p. 57", "texto": "Avenidas: máxima 60 km/h."},
            {"id": "pba2019-c06-s6.6-004", "cita": "cap. 6, secc. 6.6, p. 103", "texto": "Semiautopista: máxima 120 km/h."},
        ][:k]


def test_veredicto_lista_cerrada():
    """El veredicto solo acepta aprobada, corregir o buscar_mas."""
    assert Veredicto(veredicto="corregir", motivo="falta la cita").veredicto == "corregir"
    with pytest.raises(ValidationError):
        Veredicto(veredicto="ir_al_paso_3", motivo="otro camino")


def test_opcion_vacia():
    """Una opción en blanco se guarda como None, igual que si no se eligió ninguna."""
    assert RespuestaTutor(respuesta="60 km/h", opcion_elegida="").opcion_elegida is None
    assert RespuestaTutor(respuesta="60 km/h", opcion_elegida="60 km.").opcion_elegida == "60 km."


def test_formato():
    """Cada fragmento va entre marcas, con su id y su cita."""
    texto = formatear([Fragmento(id="f1", cita="p. 5", texto="Avenidas: máxima 60 km/h.")])
    assert texto == '<fragmento id="f1" cita="p. 5">\nAvenidas: máxima 60 km/h.\n</fragmento>'


def test_herramienta():
    """Devuelve el texto para el modelo y, aparte, los fragmentos. k no puede pasar del máximo."""
    buscar = crear_buscar_en_manual(BuscadorFalso(), k_max=5)
    mensaje = buscar.invoke({"type": "tool_call", "id": "1", "name": "buscar_en_manual",
                             "args": {"consulta": "velocidad en avenidas", "k": 1}})
    assert [f.id for f in mensaje.artifact] == ["pba2019-c04-s4.3-002"]
    assert 'id="pba2019-c04-s4.3-002"' in mensaje.content
    with pytest.raises(ValidationError):
        buscar.invoke({"consulta": "velocidad", "k": 50})


class LLMFalso(GenericFakeChatModel):
    """Modelo que devuelve mensajes ya escritos. Acepta herramientas, pero no las usa."""

    def bind_tools(self, *args, **kwargs):
        return self


def pedido(id_, nombre, **args):
    """Mensaje del modelo que pide usar una herramienta."""
    return AIMessage("", tool_calls=[{"name": nombre, "args": args, "id": id_}])


def test_busquedas_frenadas():
    """El registro no cuenta las búsquedas que frenó el tope."""
    llm = LLMFalso(messages=iter([
        pedido("1", "buscar_en_manual", consulta="velocidad en avenidas"),
        pedido("2", "buscar_en_manual", consulta="velocidad en calles"),
        pedido("3", "RespuestaTutor", respuesta="60 km/h", citas=[]),
    ]))
    tutor = Tutor(llm, crear_buscar_en_manual(BuscadorFalso(), k_max=5), max_busquedas=1)
    estado = tutor({**entrada("¿Velocidad máxima en avenidas?", None), "conversacion_resumida": []})
    assert estado["registro"][0]["consultas"] == ["velocidad en avenidas"]
