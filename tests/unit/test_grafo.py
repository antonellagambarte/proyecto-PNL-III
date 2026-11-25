"""Tests del grafo tutor → verificador. Usan agentes falsos: no llaman al LLM ni gastan crédito."""

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from src.agents.esquemas import Fragmento, RespuestaTutor, Veredicto
from src.agents.memoria import crear_memoria
from src.agents.tutor import mensajes_para_tutor
from src.agents.verificador import mensaje_para_verificador
from src.graphs.workflows.tutor_verificador import SIN_RESPALDO, armar_respuesta, crear_grafo, entrada

FRAGMENTO = Fragmento(id="f1", cita="cap. 4, secc. 4.3, p. 57", texto="Avenidas: máxima 60 km/h.")


class TutorFalso:
    """Responde siempre lo mismo y guarda el veredicto y la charla anterior que recibió en cada vuelta."""

    def __init__(self):
        self.recibido = []
        self.charlas = []

    def __call__(self, estado):
        self.recibido.append(estado["veredicto"])
        self.charlas.append(estado["conversacion_resumida"])
        borrador = RespuestaTutor(respuesta="60 km/h", citas=["f1"])
        vuelta = estado["vueltas"] + 1
        return {"borrador": borrador, "fragmentos": [FRAGMENTO], "vueltas": vuelta,
                "registro": estado["registro"] + [{"agente": "tutor", "vuelta": vuelta}]}


class VerificadorFalso:
    """Devuelve los veredictos de la lista, uno por vuelta."""

    def __init__(self, *veredictos):
        self.veredictos = list(veredictos)

    def __call__(self, estado):
        return {"veredicto": Veredicto(veredicto=self.veredictos.pop(0), motivo="prueba"),
                "registro": estado["registro"] + [{"agente": "verificador", "vuelta": estado["vueltas"]}]}


def memoria_falsa(max_tokens=1000):
    """La memoria del sistema con un modelo falso: si tiene que resumir, el resumen es «RESUMEN»."""
    return crear_memoria(FakeListChatModel(responses=["RESUMEN"] * 10),
                         {"memoria": {"max_tokens": max_tokens, "max_tokens_resumen": max_tokens // 2}})


def sesion(id_):
    """La configuración que identifica una sesión para el checkpointer."""
    return {"configurable": {"thread_id": id_}}


def correr(tutor, verificador, max_vueltas=2):
    """Corre el grafo con una pregunta de prueba y devuelve el estado final."""
    grafo = crear_grafo(tutor, verificador, memoria_falsa(), max_vueltas)
    return grafo.invoke(entrada("¿Velocidad máxima en avenidas?", None), sesion("prueba"))


def test_aprobada():
    """Si el verificador aprueba, termina en la primera vuelta con la respuesta del tutor."""
    estado = correr(TutorFalso(), VerificadorFalso("aprobada"))
    assert estado["vueltas"] == 1
    assert estado["borrador"].respuesta == "60 km/h"


def test_corrige_y_aprueba():
    """Con corregir vuelve al tutor, que recibe el veredicto, y en la segunda vuelta se aprueba."""
    tutor = TutorFalso()
    estado = correr(tutor, VerificadorFalso("corregir", "aprobada"))
    assert estado["vueltas"] == 2
    assert tutor.recibido[0] is None
    assert tutor.recibido[1].veredicto == "corregir"


def test_registro():
    """El registro acumula, en orden, una entrada por agente y por vuelta."""
    estado = correr(TutorFalso(), VerificadorFalso("corregir", "aprobada"))
    pasos = [(r["agente"], r["vuelta"]) for r in estado["registro"]]
    assert pasos == [("tutor", 1), ("verificador", 1), ("tutor", 2), ("verificador", 2)]


def test_sin_vueltas():
    """Si se acaban las vueltas sin aprobación, la respuesta es el aviso de que no hay respaldo."""
    estado = correr(TutorFalso(), VerificadorFalso("buscar_mas", "corregir"))
    assert estado["vueltas"] == 2
    assert estado["borrador"].respuesta == SIN_RESPALDO
    assert estado["borrador"].citas == []


def test_segunda_vuelta():
    """En la segunda vuelta el tutor sigue su conversación y recibe como mensaje nuevo lo que observó el verificador."""
    anteriores = [HumanMessage("Pregunta: ¿Velocidad máxima en avenidas?"), AIMessage("80 km/h")]
    estado = {"pregunta": "¿Velocidad máxima en avenidas?", "opciones": None, "fragmentos": [FRAGMENTO], "vueltas": 1,
              "mensajes_tutor": anteriores, "borrador": RespuestaTutor(respuesta="80 km/h", citas=["f1"]),
              "veredicto": Veredicto(veredicto="buscar_mas", motivo="falta la mínima",
                                     consulta_sugerida="velocidad mínima en avenidas")}
    mensajes = mensajes_para_tutor(estado)
    assert mensajes[:2] == anteriores
    assert "Motivo: falta la mínima" in mensajes[2].content
    assert "Buscá con esta consulta: velocidad mínima en avenidas" in mensajes[2].content


def test_charla_en_el_mensaje():
    """Si hay charla anterior, el tutor la recibe entre marcas, antes de la pregunta."""
    estado = {"pregunta": "¿Y en autopista?", "opciones": None, "veredicto": None,
              "conversacion_resumida": [HumanMessage("¿Velocidad máxima en avenidas?"), AIMessage("60 km/h")]}
    texto = mensajes_para_tutor(estado)[0].content
    assert "<conversacion>\nEstudiante: ¿Velocidad máxima en avenidas?\nTutor: 60 km/h\n</conversacion>" in texto
    assert texto.endswith("Pregunta: ¿Y en autopista?")


def test_consultas_al_verificador():
    """El verificador recibe las consultas del tutor de todas las vueltas, para saber si ya se buscó más de una vez."""
    estado = {"pregunta": "¿Cuál es el objetivo de la VTV?", "opciones": None, "fragmentos": [FRAGMENTO],
              "conversacion_resumida": [], "borrador": RespuestaTutor(respuesta="El manual no lo dice."),
              "registro": [{"agente": "tutor", "vuelta": 1, "consultas": ["objetivo de la VTV"]},
                           {"agente": "verificador", "vuelta": 1},
                           {"agente": "tutor", "vuelta": 2, "consultas": ["para qué sirve la VTV"]}]}
    mensaje = mensaje_para_verificador(estado)
    assert "<consultas>\n- objetivo de la VTV\n- para qué sirve la VTV\n</consultas>" in mensaje


def test_memoria():
    """En la misma sesión, la pregunta siguiente recibe la charla anterior. En otra sesión, no."""
    tutor = TutorFalso()
    grafo = crear_grafo(tutor, VerificadorFalso("aprobada", "aprobada", "aprobada"), memoria_falsa(), 2)
    grafo.invoke(entrada("¿Velocidad máxima en avenidas?", None), sesion("a"))
    estado = grafo.invoke(entrada("¿Y en autopista?", None), sesion("a"))
    grafo.invoke(entrada("¿Qué es la VTV?", None), sesion("b"))
    assert tutor.charlas[0] == []
    assert [m.content for m in tutor.charlas[1]] == ["¿Velocidad máxima en avenidas?", "60 km/h"]
    assert tutor.charlas[2] == []
    assert len(estado["registro"]) == 2  # el registro empieza de cero en cada pregunta


def test_resumen():
    """Cuando la charla pasa del tamaño máximo, llega resumida."""
    tutor = TutorFalso()
    grafo = crear_grafo(tutor, VerificadorFalso(*["aprobada"] * 4), memoria_falsa(max_tokens=40), 2)
    for pregunta in ["¿Velocidad máxima en avenidas?", "¿Y en autopista?", "¿Y en calles?", "¿Y en rutas?"]:
        grafo.invoke(entrada(pregunta, None), sesion("a"))
    assert isinstance(tutor.charlas[-1][0], SystemMessage)
    assert "RESUMEN" in tutor.charlas[-1][0].content


def test_citas():
    """Las citas salen de los fragmentos recuperados y sin repetir. Un id que no está entre ellos no se cita."""
    otro = Fragmento(id="f2", cita=FRAGMENTO.cita, texto="Otro pedazo de la misma página.")
    estado = {"pregunta": "x", "opciones": None, "fragmentos": [FRAGMENTO, otro], "vueltas": 1, "registro": [],
              "borrador": RespuestaTutor(respuesta="60 km/h", citas=["f1", "f2", "inventado"]),
              "veredicto": Veredicto(veredicto="aprobada", motivo="ok")}
    assert armar_respuesta(estado)["citas"] == ["cap. 4, secc. 4.3, p. 57"]
