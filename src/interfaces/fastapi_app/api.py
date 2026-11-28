"""La API del asistente, con FastAPI.

El sistema (modelos, índices y agentes) se carga una sola vez, al arrancar, porque tarda
varios segundos. Si falta la API key o todavía no se corrió la ingesta, la API no arranca.
"""

import logging
import time
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request

from src.common.config import cargar_config, resolver_ruta
from src.common.logs import configurar_logging
from src.graphs.workflows.tutor_verificador import TutorVerificador
from src.interfaces.fastapi_app.esquemas import Consulta, Metricas, Respuesta
from src.policies.salida import sin_enlaces

log = logging.getLogger(__name__)


@asynccontextmanager
async def arrancar(app: FastAPI):
    """Carga la configuración y el sistema antes de recibir la primera consulta."""
    config = cargar_config()
    configurar_logging(resolver_ruta(config["rutas"]["logs"]), config["logging"]["nivel"])
    app.state.sistema = TutorVerificador(config)
    yield


app = FastAPI(title="Asistente de estudio para el examen teórico de conducir", lifespan=arrancar)


@app.get("/health")
def health() -> dict:
    """Avisa que la API está lista. Si responde, el sistema ya se cargó."""
    return {"estado": "ok"}


@app.post("/consultas")
def consultar(consulta: Consulta, request: Request) -> Respuesta:
    """Responde una pregunta con el tutor y el verificador."""
    sesion = consulta.sesion or str(uuid4())
    inicio = time.perf_counter()
    try:
        resultado = request.app.state.sistema.responder(consulta.pregunta, consulta.opciones, sesion)
    except Exception as error:
        # El detalle queda en el log. A quien consulta no se le muestran errores internos.
        log.exception("Falló una consulta")
        raise HTTPException(503, "No se pudo responder en este momento. Probá de nuevo en unos minutos.") from error
    tokens = resultado.pop("tokens").values()
    return Respuesta(
        respuesta=resultado["respuesta"],
        opcion_elegida=resultado["opcion_elegida"],
        citas=resultado["citas"],
        veredicto=resultado["veredicto"],
        vueltas=resultado["vueltas"],
        pasos=[{**paso, "respuesta": sin_enlaces(paso["respuesta"])} if "respuesta" in paso else paso
               for paso in resultado["registro"]],
        sesion=sesion,
        metricas=Metricas(
            segundos=round(time.perf_counter() - inicio, 2),
            tokens_entrada=sum(uso["input_tokens"] for uso in tokens),
            tokens_salida=sum(uso["output_tokens"] for uso in tokens),
        ),
    )
