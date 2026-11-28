# Evaluación: cuatro_fragmentos_2

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_cuatro_fragmentos_2.csv`.

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
| Aciertos con opciones | 4 de 5 |
| Aciertos libres (dato clave) | 24 de 25 |
| Aciertos del tutor solo | 29 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 1 |
| Con 2 vueltas | 1 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 6.7 |
| Segundos p95 | 11.7 |
| Tutor p50 (s) | 4.5 |
| Verificador p50 (s) | 2.3 |
| Tokens de entrada (promedio) | 5571 |
| Tokens de salida (promedio) | 373 |
| Costo por pregunta (promedio, US$) | 0.00074 |
| Costo total (US$) | 0.0223 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.88 | 7.86 | 4753 | 337 | 0.000644 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.904 | 7.89 | 4845 | 492 | 0.000731 |
| eval-03 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.917 | 6.75 | 5022 | 318 | 0.000661 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 6.41 | 5114 | 259 | 0.000641 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.914 | 6.19 | 5171 | 242 | 0.000638 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.6 | 4931 | 176 | 0.000581 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 5.3 | 4745 | 166 | 0.000558 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 6.41 | 4660 | 274 | 0.000603 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | buscar_mas | 0.824 | 19.85 | 18294 | 1177 | 0.002418 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.886 | 6.53 | 4875 | 309 | 0.000642 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.926 | 7.57 | 4803 | 287 | 0.000624 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.853 | 12.0 | 8478 | 806 | 0.001251 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.961 | 6.68 | 4939 | 288 | 0.000638 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 8.82 | 4958 | 643 | 0.000817 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.941 | 7.04 | 4987 | 423 | 0.00071 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 6.35 | 4955 | 197 | 0.000594 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 5.74 | 4938 | 161 | 0.000574 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.931 | 7.29 | 4788 | 339 | 0.000648 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.909 | 11.44 | 4933 | 802 | 0.000894 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.845 | 9.48 | 9801 | 411 | 0.001186 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.967 | 8.25 | 4846 | 530 | 0.00075 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 6.23 | 4405 | 248 | 0.000565 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.925 | 6.93 | 4767 | 358 | 0.000656 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 6.05 | 4893 | 242 | 0.00061 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 7.01 | 4756 | 345 | 0.000648 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 5.53 | 4347 | 147 | 0.000508 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 5.88 | 4560 | 232 | 0.000572 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.95 | 6.67 | 4797 | 242 | 0.000601 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.888 | 6.68 | 4705 | 287 | 0.000614 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 7.82 | 5058 | 454 | 0.000733 |
