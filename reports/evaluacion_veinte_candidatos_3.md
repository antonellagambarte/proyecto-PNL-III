# Evaluación: veinte_candidatos_3

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_veinte_candidatos_3.csv`.

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
| Aciertos | 29 de 30 |
| Aciertos con opciones | 4 de 5 |
| Aciertos libres (dato clave) | 25 de 25 |
| Aciertos del tutor solo | 29 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 2 |
| La 2.ª vuelta arregló / arruinó | 1 / 1 |
| Parecido p50 | 0.94 |
| Segundos p50 | 6.4 |
| Segundos p95 | 13.6 |
| Tutor p50 (s) | 4.1 |
| Verificador p50 (s) | 2.1 |
| Tokens de entrada p50 | 5615 |
| Tokens de salida p50 | 302 |
| Costo p50 (US$) | 0.00071 |
| Costo total (US$) | 0.0258 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 29 de 30 |
| Sistema completo | 29 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.874 | 12.06 | 10944 | 812 | 0.0015 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.893 | 7.88 | 5581 | 597 | 0.000857 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 5.88 | 5372 | 210 | 0.000642 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.95 | 5.69 | 5807 | 267 | 0.000714 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.943 | 8.89 | 5985 | 195 | 0.000696 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 4.83 | 5616 | 160 | 0.000642 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.974 | 5.51 | 5436 | 174 | 0.000631 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.92 | 5.64 | 5648 | 263 | 0.000696 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 14.85 | 11631 | 1005 | 0.001666 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 9.53 | 11056 | 651 | 0.001431 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 6.66 | 5486 | 304 | 0.000701 |
| eval-12 | opciones | Sí | **No** | Sí | 2 | arreglo | aprobada | 0.851 | 17.6 | 15202 | 1027 | 0.002034 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 5.95 | 5627 | 357 | 0.000741 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 10.53 | 5660 | 1005 | 0.001069 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 6.76 | 5702 | 402 | 0.000771 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 4.4 | 5614 | 138 | 0.00063 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.944 | 5.33 | 5614 | 150 | 0.000636 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.934 | 6.45 | 5777 | 385 | 0.00077 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.921 | 5.63 | 5675 | 300 | 0.000718 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.853 | 10.15 | 11854 | 502 | 0.001436 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 7.46 | 5554 | 487 | 0.000799 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.962 | 5.11 | 5140 | 166 | 0.000597 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.938 | 6.46 | 5409 | 413 | 0.000747 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.919 | 6.35 | 5563 | 247 | 0.00068 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 6.76 | 5235 | 380 | 0.000714 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 5.22 | 5015 | 150 | 0.000576 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.907 | 4.85 | 5231 | 220 | 0.000633 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.952 | 5.69 | 5362 | 219 | 0.000646 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 5.83 | 5359 | 291 | 0.000681 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 6.64 | 5734 | 425 | 0.000786 |
