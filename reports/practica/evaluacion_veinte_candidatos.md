# Evaluación: veinte_candidatos

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_veinte_candidatos.csv`.

- **p50 y p95:** mediana y percentil 95.
- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).
- **Tutor solo:** el borrador de la primera vuelta, antes del verificador. Muestra cuántas habría acertado el sistema sin verificador.
- **Semantic similarity:** coseno entre los embeddings de la respuesta y de la esperada, con el modelo de la búsqueda.
- **Costo:** con los precios de `configs/config.yaml`, sin el descuento de OpenAI por caché. El costo real puede ser algo menor.

## Totales

| Medida | Valor |
|---|---|
| Preguntas de | practica |
| Candidatos | 20 |
| Fragmentos | 5 |
| Preguntas | 30 |
| Aciertos | 29 de 30 |
| Aciertos con opciones | 4 de 5 |
| Aciertos libres (dato clave) | 25 de 25 |
| Aciertos del tutor solo | 30 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 2 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 6.7 |
| Segundos p95 | 15.6 |
| Tutor p50 (s) | 4.5 |
| Verificador p50 (s) | 2.1 |
| Tokens de entrada (promedio) | 6552 |
| Tokens de salida (promedio) | 376 |
| Costo por pregunta (promedio, US$) | 0.00084 |
| Costo total (US$) | 0.0253 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.892 | 7.74 | 5494 | 351 | 0.000725 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.907 | 10.61 | 5592 | 852 | 0.000985 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.952 | 6.57 | 5510 | 307 | 0.000705 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.5 | 5826 | 294 | 0.00073 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 5.48 | 6001 | 227 | 0.000714 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.45 | 5631 | 170 | 0.000648 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.966 | 5.31 | 5753 | 198 | 0.000674 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.899 | 6.0 | 5355 | 274 | 0.000673 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.829 | 17.69 | 14483 | 1221 | 0.002059 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 5.73 | 5592 | 224 | 0.000671 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 6.75 | 5512 | 340 | 0.000721 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 9.47 | 10215 | 526 | 0.001285 |
| eval-13 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.925 | 17.26 | 15784 | 1243 | 0.0022 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 6.11 | 5743 | 257 | 0.000703 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 6.27 | 5711 | 336 | 0.000739 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.896 | 9.8 | 5627 | 143 | 0.000634 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.93 | 7.07 | 5630 | 155 | 0.000641 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.933 | 7.14 | 5815 | 428 | 0.000795 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.902 | 6.49 | 5673 | 312 | 0.000723 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.846 | 9.12 | 11419 | 430 | 0.001357 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.968 | 13.57 | 5563 | 460 | 0.000786 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.964 | 7.31 | 5196 | 234 | 0.000637 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.919 | 7.13 | 5481 | 372 | 0.000734 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.93 | 6.06 | 5566 | 237 | 0.000675 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 7.63 | 5460 | 345 | 0.000718 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.898 | 5.43 | 5023 | 139 | 0.000572 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.9 | 6.05 | 5071 | 262 | 0.000638 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.23 | 5371 | 263 | 0.000669 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.89 | 6.56 | 5728 | 267 | 0.000706 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 7.5 | 5744 | 422 | 0.000785 |
