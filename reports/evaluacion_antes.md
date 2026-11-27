# Evaluación: antes

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_antes.csv`.

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
| Parecido p50 | 0.92 |
| Segundos p50 | 6.8 |
| Segundos p95 | 13.0 |
| Tutor p50 (s) | 4.8 |
| Verificador p50 (s) | 1.9 |
| Tokens de entrada p50 | 5658 |
| Tokens de salida p50 | 288 |
| Costo p50 (US$) | 0.0007 |
| Costo total (US$) | 0.0248 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 30 de 30 |
| Sistema completo | 28 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.894 | 10.19 | 5934 | 507 | 0.000847 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.906 | 6.69 | 5542 | 307 | 0.000708 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 7.06 | 5380 | 273 | 0.000674 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.952 | 6.55 | 5822 | 240 | 0.000702 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.917 | 10.65 | 5778 | 241 | 0.000698 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.84 | 5616 | 166 | 0.000645 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 5.85 | 5643 | 170 | 0.000649 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.909 | 6.02 | 5394 | 262 | 0.00067 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | buscar_mas | 0.824 | 15.32 | 11703 | 981 | 0.001661 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.888 | 8.03 | 5554 | 507 | 0.000809 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.95 | 6.14 | 5725 | 254 | 0.0007 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.855 | 11.36 | 10579 | 775 | 0.001445 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.958 | 6.87 | 5616 | 215 | 0.000669 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 9.72 | 5673 | 608 | 0.000871 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.937 | 7.27 | 5711 | 493 | 0.000818 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.898 | 5.11 | 5615 | 138 | 0.00063 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.94 | 5.23 | 5614 | 151 | 0.000637 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.923 | 6.86 | 5711 | 352 | 0.000747 |
| eval-19 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.875 | 14.43 | 10009 | 1096 | 0.001549 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.843 | 10.46 | 11400 | 370 | 0.001325 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.972 | 7.47 | 5826 | 447 | 0.000806 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.963 | 6.64 | 5186 | 212 | 0.000625 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.955 | 6.71 | 5404 | 333 | 0.000707 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.919 | 6.19 | 5565 | 207 | 0.00066 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.932 | 9.12 | 8939 | 365 | 0.001076 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.906 | 5.73 | 5031 | 157 | 0.000582 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.902 | 6.06 | 5241 | 238 | 0.000643 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.12 | 5469 | 274 | 0.000684 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 6.35 | 5757 | 303 | 0.000727 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 7.42 | 5741 | 469 | 0.000809 |
