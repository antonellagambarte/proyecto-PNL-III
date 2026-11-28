# Evaluación: antes_3

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_antes_3.csv`.

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
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 6.6 |
| Segundos p95 | 18.9 |
| Tutor p50 (s) | 4.2 |
| Verificador p50 (s) | 2.3 |
| Tokens de entrada (promedio) | 7221 |
| Tokens de salida (promedio) | 395 |
| Costo por pregunta (promedio, US$) | 0.00092 |
| Costo total (US$) | 0.0276 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.887 | 6.8 | 6154 | 264 | 0.000747 |
| eval-02 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.883 | 20.77 | 14606 | 958 | 0.00194 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.46 | 5401 | 310 | 0.000695 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.948 | 6.56 | 5834 | 312 | 0.000739 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.944 | 5.65 | 6009 | 157 | 0.000679 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.86 | 5.87 | 5616 | 219 | 0.000671 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 5.8 | 5496 | 230 | 0.000665 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.915 | 7.07 | 5660 | 265 | 0.000699 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.82 | 22.89 | 22005 | 1400 | 0.0029 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.878 | 8.19 | 5608 | 493 | 0.000807 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.934 | 6.55 | 5507 | 271 | 0.000686 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 16.18 | 10552 | 925 | 0.001518 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 8.5 | 5678 | 275 | 0.000705 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.966 | 6.25 | 5666 | 209 | 0.000671 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 9.01 | 5716 | 513 | 0.000828 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.896 | 5.84 | 5681 | 149 | 0.000643 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.931 | 5.02 | 5625 | 154 | 0.000639 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.925 | 7.47 | 5569 | 384 | 0.000749 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 6.33 | 5284 | 301 | 0.000679 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.842 | 9.42 | 11852 | 373 | 0.001372 |
| eval-21 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.963 | 16.71 | 18678 | 1119 | 0.002427 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 5.83 | 4812 | 197 | 0.00058 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.923 | 6.96 | 5484 | 402 | 0.000749 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.93 | 6.42 | 5570 | 193 | 0.000654 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.931 | 7.41 | 5543 | 422 | 0.000765 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.91 | 5.78 | 5326 | 189 | 0.000627 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.908 | 6.57 | 5266 | 240 | 0.000647 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.939 | 6.12 | 5492 | 270 | 0.000684 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.886 | 6.58 | 5518 | 318 | 0.000711 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.935 | 7.19 | 5418 | 341 | 0.000712 |
