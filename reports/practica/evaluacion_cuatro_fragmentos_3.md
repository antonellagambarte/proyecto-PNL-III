# Evaluación: cuatro_fragmentos_3

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_cuatro_fragmentos_3.csv`.

- **p50 y p95:** mediana y percentil 95.
- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).
- **Tutor solo:** el borrador de la primera vuelta, antes del verificador. Muestra cuántas habría acertado el sistema sin verificador.
- **Semantic similarity:** coseno entre los embeddings de la respuesta y de la esperada, con el modelo de la búsqueda.
- **Costo:** con los precios de `configs/config.yaml`, sin el descuento de OpenAI por caché. El costo real puede ser algo menor.

## Totales

| Medida | Valor |
|---|---|
| Preguntas de | practica |
| Candidatos | 30 |
| Fragmentos | 4 |
| Preguntas | 30 |
| Aciertos | 28 de 30 |
| Aciertos con opciones | 3 de 5 |
| Aciertos libres (dato clave) | 25 de 25 |
| Aciertos del tutor solo | 30 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 3 |
| La 2.ª vuelta arregló / arruinó | 0 / 2 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 7.0 |
| Segundos p95 | 16.0 |
| Tutor p50 (s) | 4.4 |
| Verificador p50 (s) | 2.2 |
| Tokens de entrada (promedio) | 5949 |
| Tokens de salida (promedio) | 394 |
| Costo por pregunta (promedio, US$) | 0.00079 |
| Costo total (US$) | 0.0238 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.85 | 8.03 | 4751 | 341 | 0.000646 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.913 | 7.11 | 4831 | 333 | 0.00065 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.952 | 7.44 | 4743 | 422 | 0.000685 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 6.48 | 4707 | 255 | 0.000598 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.912 | 6.94 | 5151 | 325 | 0.000678 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 6.31 | 4933 | 177 | 0.000582 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 6.11 | 4975 | 218 | 0.000607 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 6.28 | 4967 | 271 | 0.000632 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 19.44 | 12756 | 1355 | 0.001953 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 7.12 | 4856 | 381 | 0.000676 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.948 | 7.15 | 5023 | 303 | 0.000654 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.851 | 11.9 | 8410 | 706 | 0.001194 |
| eval-13 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.922 | 15.31 | 13479 | 851 | 0.001773 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 6.96 | 4228 | 278 | 0.000562 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 8.45 | 5013 | 526 | 0.000764 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 5.83 | 4949 | 150 | 0.00057 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 5.3 | 4942 | 200 | 0.000594 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.929 | 7.61 | 5033 | 395 | 0.000701 |
| eval-19 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.886 | 16.64 | 13517 | 1102 | 0.001903 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.852 | 10.38 | 10144 | 402 | 0.001215 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 7.75 | 4836 | 409 | 0.000688 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 6.29 | 4402 | 245 | 0.000563 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.926 | 7.81 | 4748 | 397 | 0.000673 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 5.41 | 4897 | 193 | 0.000586 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.975 | 6.46 | 4485 | 264 | 0.00058 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.904 | 6.11 | 4364 | 225 | 0.000549 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.907 | 5.84 | 4645 | 236 | 0.000583 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.04 | 4806 | 244 | 0.000603 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.89 | 6.56 | 4949 | 244 | 0.000617 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 7.04 | 4939 | 358 | 0.000673 |
