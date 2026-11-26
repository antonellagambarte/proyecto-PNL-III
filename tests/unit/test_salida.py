"""Tests del control de salida. No usan el LLM."""

from src.agents.esquemas import RespuestaTutor
from src.graphs.workflows.tutor_verificador import crear_grafo, entrada
from src.policies.salida import ENLACE_QUITADO, SIN_INFORMACION, controlar_salida, sin_enlaces
from tests.unit.test_grafo import TutorFalso, VerificadorFalso, memoria_falsa, sesion

OPCIONES = ["60 km.", "80 km.", "90 km."]


def respuesta(texto="La máxima es 60 km/h.", opcion=None, citas=("f1",)):
    """Un borrador del tutor."""
    return RespuestaTutor(respuesta=texto, opcion_elegida=opcion, citas=list(citas))


def test_sin_cambios():
    """Una respuesta con citas válidas, sin enlaces y con una opción de la lista sale igual."""
    borrador = respuesta(opcion="60 km.")
    assert controlar_salida(borrador, OPCIONES, {"f1"}) == (borrador, [])


def test_enlaces():
    """Saca las imágenes, deja el texto de los enlaces y reemplaza las direcciones sueltas."""
    texto = "Mirá [el sitio](https://falso.com) y ![x](https://falso.com/a.png) o https://www.gba.gob.ar/seguridadvial/."
    assert sin_enlaces(texto) == f"Mirá el sitio y  o {ENLACE_QUITADO}."
    final, cambios = controlar_salida(respuesta(texto), None, {"f1"})
    assert "https" not in final.respuesta
    assert cambios == ["enlaces_quitados"]


def test_opcion():
    """Una opción de la lista queda con su texto oficial. Una que no está, se descarta."""
    final, cambios = controlar_salida(respuesta(opcion="60 KM"), OPCIONES, {"f1"})
    assert (final.opcion_elegida, cambios) == ("60 km.", [])
    final, cambios = controlar_salida(respuesta(opcion="70 km."), OPCIONES, {"f1"})
    assert (final.opcion_elegida, cambios) == (None, ["opcion_inexistente"])


def test_sin_citas_validas():
    """Sin citas, o con citas a fragmentos que no se encontraron, la respuesta se reemplaza por el aviso."""
    final, cambios = controlar_salida(respuesta(citas=[]), None, {"f1"})
    assert (final.respuesta, final.citas, cambios) == (SIN_INFORMACION, [], ["sin_citas"])
    final, cambios = controlar_salida(respuesta(opcion="60 km.", citas=["inventado"]), OPCIONES, {"f1"})
    assert (final.respuesta, final.opcion_elegida, cambios) == (SIN_INFORMACION, None, ["citas_inventadas"])


class TutorConEnlace(TutorFalso):
    """El tutor falso, pero con un enlace en la respuesta."""

    def __call__(self, estado):
        cambios = super().__call__(estado)
        cambios["borrador"] = respuesta("60 km/h. Más en https://falso.com")
        return cambios


def test_charla_controlada():
    """La respuesta que se muestra y la que queda en la charla ya pasaron por el control."""
    grafo = crear_grafo(TutorConEnlace(), VerificadorFalso("aprobada"), memoria_falsa(), 2)
    estado = grafo.invoke(entrada("¿Velocidad máxima en avenidas?", None), sesion("a"))
    assert "https" not in estado["borrador"].respuesta
    assert "https" not in estado["conversacion"][-1].content
