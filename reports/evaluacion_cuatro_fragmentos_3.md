# Evaluación: cuatro_fragmentos_3

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_cuatro_fragmentos_3.csv`.

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
| Aciertos | 27 de 30 |
| Aciertos con opciones | 4 de 5 |
| Aciertos libres (dato clave) | 23 de 25 |
| Aciertos del tutor solo | 28 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 2 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Parecido p50 | 0.91 |
| Segundos p50 | 7.0 |
| Segundos p95 | 16.5 |
| Tutor p50 (s) | 5.1 |
| Verificador p50 (s) | 2.1 |
| Tokens de entrada p50 | 4938 |
| Tokens de salida p50 | 306 |
| Costo p50 (US$) | 0.00064 |
| Costo total (US$) | 0.0238 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 28 de 30 |
| Sistema completo | 27 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.896 | 13.15 | 10240 | 624 | 0.001336 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.91 | 10.34 | 8992 | 424 | 0.001111 |
| eval-03 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.912 | 6.8 | 4988 | 325 | 0.000661 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.945 | 6.31 | 5095 | 185 | 0.000602 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 6.44 | 5328 | 244 | 0.000655 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 6.07 | 4923 | 180 | 0.000582 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 5.42 | 4976 | 169 | 0.000582 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.891 | 6.78 | 4967 | 278 | 0.000636 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 18.05 | 12828 | 1245 | 0.001905 |
| eval-10 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.873 | 27.32 | 13399 | 1036 | 0.001858 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 7.27 | 4805 | 292 | 0.000626 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 11.77 | 8400 | 408 | 0.001044 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 7.57 | 4887 | 355 | 0.000666 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 6.44 | 4875 | 190 | 0.000583 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 9.63 | 5009 | 488 | 0.000745 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 6.57 | 4930 | 140 | 0.000563 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 6.33 | 4934 | 154 | 0.00057 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.938 | 10.14 | 5100 | 434 | 0.000727 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.9 | 8.18 | 4921 | 389 | 0.000687 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.84 | 14.55 | 9729 | 979 | 0.001462 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.971 | 9.11 | 5095 | 493 | 0.000756 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.961 | 6.59 | 4382 | 205 | 0.000541 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.926 | 7.13 | 4751 | 351 | 0.000651 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.913 | 6.36 | 4883 | 245 | 0.000611 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 7.15 | 4492 | 319 | 0.000609 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 6.96 | 4339 | 152 | 0.00051 |
| eval-27 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.862 | 6.86 | 4594 | 251 | 0.000585 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.25 | 4792 | 206 | 0.000582 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 6.65 | 4744 | 259 | 0.000604 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.937 | 8.22 | 4942 | 434 | 0.000711 |
