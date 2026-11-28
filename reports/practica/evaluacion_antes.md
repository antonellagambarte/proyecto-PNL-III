# Evaluación: antes

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_antes.csv`.

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
| Aciertos del tutor solo | 29 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 3 |
| La 2.ª vuelta arregló / arruinó | 1 / 2 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 6.5 |
| Segundos p95 | 16.7 |
| Tutor p50 (s) | 4.0 |
| Verificador p50 (s) | 2.1 |
| Tokens de entrada (promedio) | 6495 |
| Tokens de salida (promedio) | 418 |
| Costo por pregunta (promedio, US$) | 0.00086 |
| Costo total (US$) | 0.0258 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.858 | 8.45 | 5509 | 308 | 0.000705 |
| eval-02 | opciones | **No** | Sí | Sí | 2 | arruino | aprobada | 0.888 | 18.44 | 14686 | 1479 | 0.002208 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.952 | 6.63 | 5393 | 285 | 0.000682 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.944 | 5.17 | 5413 | 245 | 0.000664 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.904 | 5.51 | 5837 | 233 | 0.0007 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 8.0 | 5622 | 167 | 0.000646 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.963 | 6.29 | 5496 | 242 | 0.000671 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.917 | 6.71 | 5358 | 307 | 0.000689 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 16.43 | 11424 | 1172 | 0.001728 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.878 | 5.74 | 5562 | 301 | 0.000707 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.938 | 8.6 | 5513 | 765 | 0.000934 |
| eval-12 | opciones | Sí | **No** | Sí | 2 | arreglo | aprobada | 0.854 | 16.98 | 15271 | 1507 | 0.002281 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 5.43 | 5249 | 194 | 0.000622 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.966 | 7.2 | 5268 | 596 | 0.000825 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.941 | 6.34 | 5708 | 396 | 0.000769 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 5.37 | 5635 | 196 | 0.000661 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 4.81 | 5626 | 153 | 0.000639 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.927 | 6.83 | 5552 | 360 | 0.000735 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.906 | 5.93 | 5686 | 309 | 0.000723 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.853 | 8.69 | 11283 | 420 | 0.001338 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.963 | 7.7 | 5568 | 354 | 0.000734 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.962 | 5.64 | 4812 | 201 | 0.000582 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.941 | 6.65 | 5466 | 374 | 0.000734 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.92 | 6.48 | 5597 | 262 | 0.000691 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.924 | 7.12 | 5535 | 362 | 0.000735 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.906 | 5.86 | 5075 | 226 | 0.00062 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.902 | 4.8 | 5256 | 189 | 0.00062 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 5.54 | 5363 | 247 | 0.00066 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 5.74 | 5660 | 296 | 0.000714 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.961 | 6.59 | 5413 | 400 | 0.000741 |
