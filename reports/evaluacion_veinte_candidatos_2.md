# Evaluación: veinte_candidatos_2

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_veinte_candidatos_2.csv`.

- **p50** es la mediana: la mitad de las preguntas tarda (o gasta) eso o menos. **p95**: solo 5 de cada 100 tardan más.
- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).
- **Tutor solo** es el borrador del tutor en la primera vuelta, antes de que lo revise el verificador.
- **Parecido** es la similitud de significado (coseno entre embeddings, como Semantic Similarity de RAGAS) entre la respuesta y la esperada, con el modelo de la búsqueda. Con este modelo los valores quedan entre 0,7 y 1: sirve para comparar, no como porcentaje de acierto.
- El costo usa los precios de `configs/config.yaml` y no descuenta la caché de OpenAI: es un techo.

## Totales

| Medida | Valor |
|---|---|
| Preguntas de | practica |
| Candidatos | 20 |
| Fragmentos | 5 |
| Preguntas | 30 |
| Aciertos | 28 de 30 |
| Aciertos con opciones | 3 de 5 |
| Aciertos libres (dato clave) | 25 de 25 |
| Aciertos del tutor solo | 30 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 1 |
| Con 2 vueltas | 2 |
| La 2.ª vuelta arregló / arruinó | 0 / 2 |
| Parecido p50 | 0.93 |
| Segundos p50 | 5.9 |
| Segundos p95 | 14.1 |
| Tutor p50 (s) | 4.0 |
| Verificador p50 (s) | 2.1 |
| Tokens de entrada p50 | 5612 |
| Tokens de salida p50 | 282 |
| Costo p50 (US$) | 0.00071 |
| Costo total (US$) | 0.0252 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 30 de 30 |
| Sistema completo | 28 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.886 | 10.66 | 6137 | 663 | 0.000945 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 6.42 | 5531 | 346 | 0.000726 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 6.14 | 5373 | 263 | 0.000669 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.947 | 6.26 | 5812 | 254 | 0.000708 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 5.72 | 5984 | 279 | 0.000738 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.857 | 4.82 | 5619 | 162 | 0.000643 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 5.33 | 5704 | 165 | 0.000653 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.92 | 5.92 | 5383 | 275 | 0.000676 |
| eval-09 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.831 | 16.79 | 11582 | 1000 | 0.001658 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 5.82 | 5552 | 302 | 0.000706 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 5.95 | 5504 | 255 | 0.000678 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 10.86 | 9873 | 582 | 0.001278 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 7.9 | 5597 | 521 | 0.00082 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 5.89 | 5702 | 194 | 0.000667 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 5.93 | 5708 | 375 | 0.000758 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 4.9 | 5612 | 134 | 0.000628 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 5.26 | 5613 | 151 | 0.000637 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.938 | 5.94 | 5518 | 315 | 0.000709 |
| eval-19 | opciones | **No** | Sí | **No** | 2 | arruino | corregir | 0.854 | 22.09 | 15896 | 1859 | 0.002519 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.857 | 9.58 | 11529 | 489 | 0.001397 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.961 | 8.01 | 5837 | 489 | 0.000828 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.962 | 5.32 | 5139 | 204 | 0.000616 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.917 | 7.74 | 5604 | 476 | 0.000798 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 6.32 | 5564 | 271 | 0.000692 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.973 | 6.21 | 5522 | 293 | 0.000699 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 4.94 | 5034 | 158 | 0.000582 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.904 | 5.23 | 5052 | 187 | 0.000599 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.955 | 5.59 | 5363 | 286 | 0.000679 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 5.87 | 5755 | 279 | 0.000715 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 7.34 | 5733 | 422 | 0.000784 |
