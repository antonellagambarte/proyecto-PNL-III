# Evaluación: veinte_candidatos_3

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_veinte_candidatos_3.csv`.

- **p50 y p95:** mediana y percentil 95.
- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).
- **Tutor solo:** el borrador de la primera vuelta, antes del verificador. Muestra cuántas habría acertado el sistema sin verificador.
- **Semantic similarity:** coseno entre los embeddings de la respuesta y de la esperada, con el modelo de la búsqueda.
- **Costo:** con los precios de `configs/config.yaml`, sin el descuento de OpenAI por caché. El costo real puede ser algo menor.

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
| Aciertos del tutor solo | 30 de 30 |
| Cita la página esperada | 29 de 30 |
| Sin respaldo | 0 |
| Con 2 vueltas | 1 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 7.2 |
| Segundos p95 | 11.6 |
| Tutor p50 (s) | 4.8 |
| Verificador p50 (s) | 2.2 |
| Tokens de entrada (promedio) | 6410 |
| Tokens de salida (promedio) | 339 |
| Costo por pregunta (promedio, US$) | 0.00081 |
| Costo total (US$) | 0.0243 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.883 | 7.56 | 6161 | 278 | 0.000755 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.908 | 7.98 | 5545 | 544 | 0.000826 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.963 | 6.17 | 5375 | 284 | 0.000679 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.95 | 6.35 | 5853 | 288 | 0.000729 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 5.1 | 6007 | 197 | 0.000699 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 5.17 | 5622 | 161 | 0.000643 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.957 | 5.63 | 5708 | 200 | 0.000671 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.913 | 6.59 | 5399 | 227 | 0.000653 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | aprobada | 0.819 | 20.2 | 20847 | 1352 | 0.002761 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.882 | 7.34 | 5592 | 211 | 0.000665 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.936 | 6.89 | 5501 | 259 | 0.00068 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.854 | 10.51 | 9876 | 466 | 0.001221 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 8.3 | 5654 | 406 | 0.000768 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.95 | 5061 | 208 | 0.00061 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.948 | 8.88 | 5712 | 399 | 0.000771 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.896 | 5.97 | 5650 | 148 | 0.000639 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.943 | 5.54 | 5625 | 151 | 0.000638 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.941 | 7.94 | 5558 | 395 | 0.000753 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.887 | 7.72 | 5701 | 386 | 0.000763 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.849 | 12.5 | 11120 | 474 | 0.001349 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.944 | 10.03 | 5521 | 633 | 0.000869 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.96 | 6.85 | 5399 | 232 | 0.000656 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 7.52 | 5498 | 378 | 0.000739 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 7.21 | 5560 | 245 | 0.000678 |
| eval-25 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.969 | 7.81 | 5454 | 372 | 0.000731 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.911 | 5.92 | 5060 | 191 | 0.000602 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.905 | 5.73 | 5252 | 205 | 0.000628 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.951 | 6.45 | 5475 | 208 | 0.000651 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 7.17 | 5778 | 284 | 0.00072 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.955 | 7.48 | 5736 | 388 | 0.000768 |
