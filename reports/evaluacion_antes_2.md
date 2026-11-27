# Evaluación: antes_2

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_antes_2.csv`.

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
| Aciertos con opciones | 4 de 5 |
| Aciertos libres (dato clave) | 24 de 25 |
| Aciertos del tutor solo | 29 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 1 |
| Con 2 vueltas | 3 |
| La 2.ª vuelta arregló / arruinó | 1 / 2 |
| Parecido p50 | 0.92 |
| Segundos p50 | 6.6 |
| Segundos p95 | 15.3 |
| Tutor p50 (s) | 4.4 |
| Verificador p50 (s) | 2.0 |
| Tokens de entrada p50 | 5618 |
| Tokens de salida p50 | 286 |
| Costo p50 (US$) | 0.00071 |
| Costo total (US$) | 0.0279 |

## Tres variantes

| Variante | Aciertos |
|---|---|
| Modelo solo, sin el manual | 25 de 30 |
| Tutor solo, sin el verificador | 29 de 30 |
| Sistema completo | 28 de 30 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Parecido | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.888 | 11.65 | 11181 | 451 | 0.001344 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.92 | 6.52 | 5486 | 276 | 0.000687 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 6.86 | 5178 | 388 | 0.000712 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.95 | 6.46 | 5462 | 189 | 0.000641 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 6.05 | 5986 | 212 | 0.000705 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.43 | 5622 | 161 | 0.000643 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 5.42 | 5344 | 167 | 0.000618 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.91 | 6.46 | 5652 | 286 | 0.000708 |
| eval-09 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.816 | 14.66 | 14905 | 1030 | 0.002005 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 8.37 | 5594 | 485 | 0.000802 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.95 | 6.15 | 5658 | 265 | 0.000698 |
| eval-12 | opciones | Sí | **No** | Sí | 2 | arreglo | aprobada | 0.852 | 15.86 | 15195 | 1219 | 0.002129 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.956 | 5.53 | 5626 | 179 | 0.000652 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.966 | 9.11 | 4980 | 856 | 0.000926 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.944 | 6.65 | 5695 | 364 | 0.000751 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 5.74 | 5614 | 138 | 0.00063 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.914 | 6.38 | 5623 | 273 | 0.000699 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.939 | 6.83 | 5524 | 392 | 0.000748 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.918 | 6.24 | 5256 | 295 | 0.000673 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.847 | 9.65 | 11396 | 388 | 0.001334 |
| eval-21 | libre | **No** | Sí | **No** | 2 | arruino | corregir | 0.842 | 23.73 | 21935 | 2036 | 0.003211 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 5.55 | 5188 | 204 | 0.000621 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.933 | 6.93 | 5608 | 394 | 0.000758 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.904 | 8.6 | 10204 | 286 | 0.001163 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.973 | 6.35 | 5231 | 312 | 0.000679 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 5.44 | 5023 | 146 | 0.000575 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.908 | 5.72 | 5257 | 247 | 0.000649 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.93 | 5469 | 261 | 0.000677 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 6.63 | 5757 | 263 | 0.000707 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.948 | 7.55 | 5704 | 452 | 0.000796 |
