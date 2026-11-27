# Evaluación: cuatro_fragmentos

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_cuatro_fragmentos.csv`.

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
| Aciertos con opciones | 3 de 5 |
| Aciertos libres (dato clave) | 24 de 25 |
| Aciertos del tutor solo | 29 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 3 |
| La 2.ª vuelta arregló / arruinó | 0 / 2 |
| Parecido p50 | 0.92 |
| Segundos p50 | 8.3 |
| Segundos p95 | 23.6 |
| Tutor p50 (s) | 5.5 |
| Verificador p50 (s) | 2.3 |
| Tokens de entrada p50 | 4928 |
| Tokens de salida p50 | 288 |
| Costo p50 (US$) | 0.00065 |
| Costo total (US$) | 0.0257 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 29 de 30 |
| Sistema completo | 27 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.878 | 14.87 | 9186 | 589 | 0.001213 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.899 | 8.88 | 4835 | 493 | 0.00073 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.962 | 7.26 | 4713 | 200 | 0.000571 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 8.28 | 5122 | 276 | 0.00065 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 7.58 | 5312 | 249 | 0.000656 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 7.07 | 4925 | 180 | 0.000583 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.964 | 6.86 | 4974 | 175 | 0.000585 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 11.16 | 4913 | 320 | 0.000651 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 24.26 | 17999 | 1247 | 0.002423 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 8.27 | 5010 | 415 | 0.000709 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 11.79 | 5012 | 280 | 0.000641 |
| eval-12 | opciones | Sí | Sí | Sí | 2 | igual | aprobada | 0.854 | 30.31 | 19046 | 1456 | 0.002633 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.961 | 7.57 | 4900 | 286 | 0.000633 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 6.26 | 4892 | 209 | 0.000594 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 8.69 | 4963 | 463 | 0.000728 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 5.93 | 4924 | 133 | 0.000559 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 6.35 | 4930 | 156 | 0.000571 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.919 | 12.86 | 9239 | 545 | 0.001196 |
| eval-19 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.874 | 22.78 | 14245 | 1170 | 0.00201 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 10.23 | 9593 | 389 | 0.001154 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.977 | 8.92 | 5083 | 464 | 0.00074 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.961 | 6.74 | 4380 | 199 | 0.000538 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.947 | 8.5 | 4739 | 433 | 0.00069 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.92 | 7.88 | 4890 | 258 | 0.000618 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.908 | 7.37 | 4725 | 289 | 0.000617 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 7.16 | 4337 | 147 | 0.000507 |
| eval-27 | libre | **No** | **No** | Sí | 1 | — | aprobada | 0.876 | 7.47 | 4591 | 258 | 0.000588 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 7.78 | 4789 | 258 | 0.000608 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.89 | 8.81 | 4744 | 330 | 0.000639 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 9.22 | 5060 | 399 | 0.000705 |
