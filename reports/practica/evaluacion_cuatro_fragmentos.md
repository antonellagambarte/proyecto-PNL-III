# Evaluación: cuatro_fragmentos

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_cuatro_fragmentos.csv`.

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
| Aciertos | 29 de 30 |
| Aciertos con opciones | 5 de 5 |
| Aciertos libres (dato clave) | 24 de 25 |
| Aciertos del tutor solo | 29 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 1 |
| La 2.ª vuelta arregló / arruinó | 0 / 0 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 6.8 |
| Segundos p95 | 12.0 |
| Tutor p50 (s) | 4.5 |
| Verificador p50 (s) | 2.2 |
| Tokens de entrada (promedio) | 5318 |
| Tokens de salida (promedio) | 358 |
| Costo por pregunta (promedio, US$) | 0.00071 |
| Costo total (US$) | 0.0213 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.852 | 7.87 | 4745 | 292 | 0.00062 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 12.6 | 4811 | 1018 | 0.00099 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 6.08 | 4725 | 264 | 0.000605 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.947 | 6.24 | 5117 | 251 | 0.000637 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.917 | 6.71 | 5165 | 301 | 0.000667 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.58 | 4920 | 208 | 0.000596 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 5.91 | 4986 | 176 | 0.000587 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.9 | 6.45 | 4631 | 261 | 0.000594 |
| eval-09 | opciones | Sí | Sí | **No** | 1 | — | aprobada | 0.855 | 8.4 | 3855 | 504 | 0.000638 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.878 | 6.55 | 4864 | 313 | 0.000643 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.929 | 8.49 | 5026 | 561 | 0.000783 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 10.24 | 8427 | 468 | 0.001077 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 5.95 | 4902 | 211 | 0.000596 |
| eval-14 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.956 | 15.76 | 11535 | 833 | 0.00157 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 11.35 | 9239 | 731 | 0.001289 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.896 | 5.98 | 4947 | 144 | 0.000567 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 5.89 | 4938 | 156 | 0.000572 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.923 | 7.01 | 5090 | 322 | 0.00067 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.892 | 6.42 | 4920 | 277 | 0.00063 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.85 | 8.38 | 4913 | 514 | 0.000748 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.971 | 7.53 | 5099 | 454 | 0.000737 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.962 | 6.8 | 4392 | 202 | 0.00054 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.934 | 7.15 | 4806 | 387 | 0.000674 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 6.24 | 4897 | 251 | 0.000615 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.966 | 7.25 | 5029 | 305 | 0.000655 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 5.93 | 4343 | 169 | 0.000519 |
| eval-27 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.883 | 7.04 | 4580 | 274 | 0.000595 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.44 | 4802 | 251 | 0.000606 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.887 | 6.45 | 4753 | 261 | 0.000606 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.947 | 7.16 | 5069 | 369 | 0.000691 |
