# Evaluación: antes_2

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_antes_2.csv`.

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
| Fragmentos | 5 |
| Preguntas | 30 |
| Aciertos | 28 de 30 |
| Aciertos con opciones | 4 de 5 |
| Aciertos libres (dato clave) | 24 de 25 |
| Aciertos del tutor solo | 29 de 30 |
| Cita la página esperada | 28 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 1 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 7.0 |
| Segundos p95 | 9.8 |
| Tutor p50 (s) | 4.5 |
| Verificador p50 (s) | 2.2 |
| Tokens de entrada (promedio) | 6287 |
| Tokens de salida (promedio) | 367 |
| Costo por pregunta (promedio, US$) | 0.00081 |
| Costo total (US$) | 0.0244 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | **No** | **No** | **No** | 1 | — | aprobada | 0.832 | 8.25 | 5923 | 378 | 0.000781 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.908 | 8.6 | 5497 | 511 | 0.000805 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.962 | 6.25 | 5402 | 306 | 0.000693 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.99 | 5814 | 247 | 0.000705 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.898 | 6.87 | 5393 | 322 | 0.0007 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.82 | 5622 | 159 | 0.000642 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 6.19 | 5692 | 221 | 0.00068 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.9 | 6.6 | 5362 | 288 | 0.00068 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 22.14 | 22695 | 1406 | 0.002972 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 7.49 | 5549 | 341 | 0.000725 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 6.38 | 5454 | 249 | 0.00067 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 8.29 | 5408 | 540 | 0.000811 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 8.16 | 5241 | 542 | 0.000795 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 9.65 | 5669 | 770 | 0.000952 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.952 | 7.08 | 5712 | 339 | 0.000741 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 5.7 | 5635 | 151 | 0.000639 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 5.34 | 5624 | 155 | 0.00064 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.921 | 8.09 | 5785 | 364 | 0.00076 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 6.41 | 5275 | 310 | 0.000682 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.834 | 9.88 | 11535 | 402 | 0.001355 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 9.03 | 5564 | 467 | 0.00079 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 5.7 | 5194 | 207 | 0.000623 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.91 | 6.7 | 5438 | 381 | 0.000734 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 6.08 | 5562 | 236 | 0.000674 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.967 | 7.52 | 5535 | 346 | 0.000727 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 5.72 | 5062 | 189 | 0.000601 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 6.22 | 5247 | 232 | 0.000641 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 7.56 | 5475 | 212 | 0.000654 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 7.14 | 5516 | 299 | 0.000701 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 8.15 | 5740 | 436 | 0.000792 |
