# Evaluación: veinte_candidatos

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_veinte_candidatos.csv`.

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
| Aciertos | 27 de 30 |
| Aciertos con opciones | 4 de 5 |
| Aciertos libres (dato clave) | 23 de 25 |
| Aciertos del tutor solo | 28 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 1 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Parecido p50 | 0.92 |
| Segundos p50 | 6.3 |
| Segundos p95 | 11.1 |
| Tutor p50 (s) | 4.1 |
| Verificador p50 (s) | 2.0 |
| Tokens de entrada p50 | 5656 |
| Tokens de salida p50 | 294 |
| Costo p50 (US$) | 0.00072 |
| Costo total (US$) | 0.0246 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 28 de 30 |
| Sistema completo | 27 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.874 | 10.13 | 6214 | 730 | 0.000986 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.891 | 8.21 | 5579 | 552 | 0.000834 |
| eval-03 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.913 | 6.19 | 5782 | 303 | 0.00073 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 5.95 | 5836 | 271 | 0.000719 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.897 | 5.85 | 5797 | 250 | 0.000705 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.32 | 5616 | 161 | 0.000642 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 5.43 | 5704 | 165 | 0.000653 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.902 | 5.83 | 5398 | 260 | 0.00067 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.818 | 22.76 | 11159 | 1224 | 0.001728 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.896 | 9.4 | 11188 | 480 | 0.001359 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 7.5 | 5713 | 292 | 0.000717 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.855 | 10.82 | 10194 | 646 | 0.001342 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 6.05 | 5615 | 295 | 0.000709 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.967 | 5.53 | 5253 | 227 | 0.000639 |
| eval-15 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.952 | 7.17 | 5677 | 380 | 0.000758 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.898 | 4.82 | 4217 | 138 | 0.000491 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.932 | 5.22 | 5621 | 160 | 0.000642 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.93 | 7.9 | 5809 | 449 | 0.000805 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.921 | 6.95 | 5658 | 379 | 0.000755 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.843 | 6.99 | 5720 | 379 | 0.000762 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.971 | 11.24 | 10823 | 683 | 0.001424 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 5.11 | 4805 | 160 | 0.000561 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.928 | 6.79 | 5481 | 391 | 0.000744 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.906 | 8.58 | 10984 | 248 | 0.001222 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 6.02 | 5238 | 340 | 0.000694 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 5.22 | 5017 | 146 | 0.000575 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.901 | 5.04 | 5250 | 200 | 0.000625 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.47 | 5470 | 250 | 0.000672 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.891 | 5.67 | 5653 | 276 | 0.000703 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.74 | 5470 | 430 | 0.000762 |
