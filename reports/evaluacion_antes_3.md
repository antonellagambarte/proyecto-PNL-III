# Evaluación: antes_3

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_antes_3.csv`.

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
| Sin respaldo | 0 |
| Con 2 vueltas | 3 |
| La 2.ª vuelta arregló / arruinó | 0 / 2 |
| Parecido p50 | 0.92 |
| Segundos p50 | 6.7 |
| Segundos p95 | 19.4 |
| Tutor p50 (s) | 4.8 |
| Verificador p50 (s) | 2.2 |
| Tokens de entrada p50 | 5678 |
| Tokens de salida p50 | 312 |
| Costo p50 (US$) | 0.00071 |
| Costo total (US$) | 0.0285 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 30 de 30 |
| Sistema completo | 28 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 12.89 | 11187 | 829 | 0.001533 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 7.26 | 5602 | 441 | 0.000781 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.46 | 5400 | 315 | 0.000697 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.941 | 6.24 | 5819 | 280 | 0.000722 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 6.24 | 6080 | 224 | 0.00072 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.54 | 5614 | 165 | 0.000644 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 5.62 | 5691 | 203 | 0.000671 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.9 | 6.34 | 5389 | 267 | 0.000672 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 28.91 | 20275 | 1940 | 0.002998 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 6.64 | 5542 | 308 | 0.000708 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.931 | 6.66 | 5719 | 270 | 0.000707 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.844 | 11.65 | 9933 | 715 | 0.001351 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.95 | 6.29 | 5670 | 257 | 0.000696 |
| eval-14 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.96 | 17.27 | 14354 | 1001 | 0.001936 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 7.59 | 5686 | 330 | 0.000734 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 6.73 | 5614 | 135 | 0.000629 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.945 | 5.96 | 5614 | 198 | 0.00066 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.919 | 7.85 | 5781 | 385 | 0.000771 |
| eval-19 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.872 | 21.13 | 14343 | 1355 | 0.002112 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 11.46 | 11386 | 464 | 0.001371 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 8.68 | 5815 | 511 | 0.000837 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.964 | 6.65 | 4808 | 217 | 0.000589 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.943 | 7.27 | 5388 | 354 | 0.000716 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.917 | 9.95 | 9861 | 358 | 0.001165 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.962 | 8.06 | 5239 | 340 | 0.000694 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 5.22 | 5015 | 142 | 0.000572 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.904 | 6.38 | 5246 | 243 | 0.000646 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.43 | 5469 | 255 | 0.000674 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.888 | 5.91 | 5656 | 253 | 0.000692 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 7.45 | 5717 | 463 | 0.000803 |
