# Asistente de estudio para el examen teórico de conducir

Asistente para estudiar el examen teórico de la licencia de conducir de la Provincia de Buenos Aires. Responde con el *Manual del conductor* (edición 2019) y cita la sección y la página de donde sale cada respuesta. Si el manual no trae la información, lo dice en lugar de responder de memoria.

## Qué hace

- **Búsqueda híbrida en el manual:** por palabras (BM25) y por significado (embeddings de `intfloat/multilingual-e5-small` en Chroma), combinadas con RRF y reordenadas con un re-ranker (`cross-encoder/mmarco-mMiniLMv2-L12-H384-v1`).
- **Dos agentes en LangGraph:** el **tutor** busca en el manual y redacta la respuesta con citas. El **verificador** no busca: lee la respuesta junto con los mismos fragmentos que encontró el tutor y comprueba que todo lo que afirma esté en ellos, que las citas correspondan y, si hay opciones, que la elegida sea la que mejor coincide. Decide entre tres veredictos: *aprobada*, *corregir* (el tutor arregla la respuesta) o *buscar más* (el tutor vuelve a buscar, con una consulta que le sugiere el verificador). Hay como máximo dos vueltas: si en la segunda tampoco la aprueba, el sistema responde que no encontró respaldo suficiente, en lugar de dar una respuesta sin respaldo.
- **Preguntas libres o de opción múltiple**, como las del cuestionario oficial.
- **Memoria de la charla:** recuerda las preguntas anteriores de la misma sesión, así se puede repreguntar sin repetir todo. Por ejemplo, después de «¿Cuál es la velocidad máxima en avenidas?» alcanza con preguntar «¿y en autopista?». Cuando la charla se alarga, la resume.
- **Seguridad:**
  - **Entrada:** largo máximo, limpieza de caracteres invisibles y detección de intentos de inyección. Una pregunta rechazada no llega a los agentes ni a la memoria.
  - **Agentes:** los fragmentos del manual y la charla se tratan como datos, nunca como instrucciones. El tutor tiene una sola herramienta, de solo lectura, y el verificador ninguna. El camino lo decide el código, con tope de vueltas y de búsquedas.
  - **Salida:** formato fijo, citas armadas por el código (si ninguna corresponde a un fragmento encontrado, la respuesta no se muestra) y sin enlaces ni imágenes. Aviso de que el manual es de 2019.
  - **Registro:** auditoría de cada paso en `logs/auditoria.jsonl`, sin guardar el texto de preguntas ni respuestas.
  - **Pruebas:** 10 preguntas de ataque y fuera de tema (`scripts.probar_ataques`), que cumplen 10 de 10.
- **API** con FastAPI y **pantalla** de chat con Streamlit.

```
Pantalla (Streamlit) → API (FastAPI) → control de entrada
  → tutor: búsqueda híbrida y re-ranking → respuesta con citas
  → verificador: ¿la respaldan los fragmentos? → aprobada, corregir o buscar más (hasta 2 vueltas)
  → control de salida → respuesta con citas, o aviso de que no encontró respaldo
```

## Requisitos

- [uv](https://docs.astral.sh/uv/), que instala Python 3.12 si hace falta.
- Una API key de OpenAI. El modelo se elige en `configs/config.yaml` (`gpt-6-luna`).
- Unos 2 GB de disco: el entorno ocupa alrededor de 1,2 GB, sobre todo por PyTorch, y los dos modelos de búsqueda se descargan solos de Hugging Face la primera vez que se usan.

## Instalación

Desde la raíz del proyecto:

```bash
uv sync                               # crea .venv con las versiones exactas de uv.lock
cp .env.example .env                  # y completar OPENAI_API_KEY
uv run python -m scripts.ingestar     # arma los índices de búsqueda en data/indices/
```

Para comprobar que todo funciona:

```bash
uv run pytest                                 # tests unitarios, sin LLM y sin costo
uv run --no-project scripts/verificar_llm.py  # que la API key y el modelo respondan
```

## Uso

En dos terminales, primero la API y después la pantalla:

```bash
uv run uvicorn app.main:app
uv run python -m streamlit run app/pantalla.py
```

La API también se puede usar directo. La documentación interactiva queda en http://127.0.0.1:8000/docs.

- `GET /health`: si la API está lista.
- `POST /consultas`: recibe la pregunta y, si tiene, las opciones y la sesión de la charla. Devuelve la respuesta, la opción elegida, las citas, el veredicto del verificador, las vueltas, lo que hizo cada agente en cada paso, la sesión y cuánto tardó y gastó.

```bash
curl -X POST http://127.0.0.1:8000/consultas -H "Content-Type: application/json" \
     -d '{"pregunta": "¿Cuál es la velocidad máxima en avenidas?"}'
```

## Evaluación

Las preguntas están en `data/processed/`:

- `preguntas_eval.jsonl`: 30 de práctica, para ajustar el sistema.
- `preguntas_test.jsonl`: 30 de test, que se corren una sola vez, con el sistema ya ajustado.
- `preguntas_extra.jsonl`: 10 de ataque y fuera de tema.

Cada pregunta trae las páginas del manual que la responden. En las de opción múltiple, acertar es elegir la correcta. En las libres, que la respuesta traiga el dato clave (campo `clave`).

| Qué mide | Comando |
|---|---|
| La búsqueda sola: si encuentra las páginas correctas y cuánto tarda | `uv run python -m scripts.evaluar_busqueda [practica\|test]` |
| El sistema completo: aciertos, citas, tiempos, tokens y costo | `uv run python -m scripts.evaluar_sistema <nombre> [practica\|test]` |
| El modelo solo, sin el manual | `uv run python -m scripts.evaluar_modelo_solo [practica\|test]` |
| Un LLM como juez (DeepEval): si la respuesta contesta lo preguntado y si se apoya en lo que encontró | `uv run --with deepeval python -m scripts.juzgar_respuestas <nombre>` |
| Las preguntas de ataque y fuera de tema | `uv run python -m scripts.probar_ataques` |

Todas menos la primera usan el LLM: cada corrida cuesta entre 1 y 3 centavos de dólar. Los resultados quedan en `reports/`, en CSV y en markdown. `reports/corridas.md` junta una fila por corrida del sistema completo, para comparar configuraciones.

## Configuración

Todo lo que se puede ajustar está en `configs/config.yaml`, con comentarios:

- `llm`: modelo, tiempo máximo de espera, reintentos y precios por millón de tokens.
- `agentes`: vueltas entre tutor y verificador, y búsquedas del tutor en cada vuelta.
- `busqueda`: modelos de embeddings y de re-ranking, candidatos antes del re-ranking, fragmentos que recibe el tutor y tope por sección.
- `chunks`, `memoria`, `entrada` y `pantalla`.

La API key va solo en `.env`, que no se sube al repositorio.

## Estructura

```
app/                      API (main.py) y pantalla (pantalla.py)
configs/config.yaml       configuración
data/raw/                 manual, cuestionario oficial y tablas transcriptas a mano
data/processed/           secciones, chunks y preguntas de evaluación
scripts/                  ingesta, extracción del cuestionario, evaluaciones y ataques
src/agents/               tutor, verificador, prompts y memoria de la charla
src/graphs/workflows/     el grafo que une los dos agentes y los controles
src/interfaces/           la API
src/policies/             controles de entrada y de salida
src/rag/ingestion/        lectura del PDF y armado de chunks
src/rag/retrievers/       BM25, embeddings, búsqueda híbrida, re-ranking y citas
src/rag/evaluators/       métricas y evaluaciones
src/tools/builtin/        la herramienta de búsqueda del tutor
src/common/               configuración, logs y auditoría
tests/unit/               tests unitarios
reports/                  resultados de las evaluaciones
```

## Limitaciones

- El manual es de 2019: las normas pueden haber cambiado, y la pantalla lo avisa.
- Responde solo con lo que encuentra en el manual. Si la búsqueda no trae el fragmento justo, puede decir que no encontró la información aunque esté.
- Depende de la API de OpenAI: sin conexión o sin crédito no responde.
