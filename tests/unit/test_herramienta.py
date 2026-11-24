"""Tests de los esquemas y de la herramienta del tutor. Usan un buscador falso, sin modelos."""

import pytest
from pydantic import ValidationError

from src.agents.esquemas import Fragmento, Veredicto
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
