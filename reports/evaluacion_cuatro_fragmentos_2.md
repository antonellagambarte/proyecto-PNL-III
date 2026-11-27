# Evaluación: cuatro_fragmentos_2

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_cuatro_fragmentos_2.csv`.

- **p50** es la mediana: la mitad de las preguntas tarda (o gasta) eso o menos. **p95**: solo 5 de cada 100 tardan más.
- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).
- **Tutor solo** es el borrador del tutor en la primera vuelta, antes de que lo revise el verificador.
- **Parecido** es la similitud de significado (coseno entre embeddings, como Semantic Similarity de RAGAS) entre la respuesta y la esperada, con el modelo de la búsqueda. Con este modelo los valores quedan entre 0,7 y 1: sirve para comparar, no como porcentaje de acierto.
- El costo usa los precios de `configs/config.yaml` y no descuenta la caché de OpenAI: es un techo.

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
| Sin respaldo | 0 |
| Con 2 vueltas | 2 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Parecido p50 | 0.91 |
| Segundos p50 | 7.5 |
| Segundos p95 | 15.2 |
| Tutor p50 (s) | 5.1 |
| Verificador p50 (s) | 2.0 |
| Tokens de entrada p50 | 5014 |
| Tokens de salida p50 | 290 |
| Costo p50 (US$) | 0.00064 |
| Costo total (US$) | 0.0248 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 29 de 30 |
| Sistema completo | 28 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.877 | 14.11 | 9308 | 702 | 0.001282 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.908 | 8.08 | 4833 | 473 | 0.00072 |
| eval-03 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.916 | 7.09 | 5011 | 263 | 0.000633 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 6.84 | 5120 | 276 | 0.00065 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.904 | 6.65 | 5328 | 182 | 0.000624 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.65 | 4910 | 160 | 0.000571 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 6.06 | 4978 | 171 | 0.000583 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 7.05 | 4961 | 303 | 0.000648 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 18.92 | 12336 | 1190 | 0.001829 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 6.45 | 5010 | 246 | 0.000624 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.966 | 6.69 | 5015 | 244 | 0.000624 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.851 | 12.15 | 8490 | 602 | 0.00115 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 6.06 | 4884 | 189 | 0.000583 |
| eval-14 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.96 | 16.07 | 12369 | 896 | 0.001685 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.943 | 7.97 | 5012 | 470 | 0.000736 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 5.53 | 4924 | 136 | 0.00056 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 6.08 | 4930 | 154 | 0.00057 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.925 | 8.66 | 5081 | 442 | 0.000729 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.912 | 7.28 | 5099 | 310 | 0.000665 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.846 | 12.29 | 9629 | 439 | 0.001182 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 12.6 | 9779 | 492 | 0.001224 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.964 | 7.46 | 4721 | 232 | 0.000588 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.943 | 7.68 | 4734 | 332 | 0.000639 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.91 | 9.93 | 9180 | 320 | 0.001078 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.943 | 11.06 | 9332 | 417 | 0.001142 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 5.82 | 4339 | 154 | 0.000511 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.902 | 7.49 | 4578 | 203 | 0.000559 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.78 | 4796 | 257 | 0.000608 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 7.86 | 5019 | 257 | 0.00063 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 10.97 | 9197 | 464 | 0.001152 |
