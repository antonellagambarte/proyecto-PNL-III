# Evaluación: veinte_candidatos_2

Se genera con `uv run python -m scripts.evaluar_sistema`. Una fila por pregunta en `evaluacion_veinte_candidatos_2.csv`.

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
| Sin respaldo | 1 |
| Con 2 vueltas | 2 |
| La 2.ª vuelta arregló / arruinó | 0 / 1 |
| Semantic similarity (promedio) | 0.92 |
| Segundos p50 | 6.3 |
| Segundos p95 | 11.9 |
| Tutor p50 (s) | 4.0 |
| Verificador p50 (s) | 2.2 |
| Tokens de entrada (promedio) | 6430 |
| Tokens de salida (promedio) | 359 |
| Costo por pregunta (promedio, US$) | 0.00082 |
| Costo total (US$) | 0.0247 |

## Por pregunta

| Id | Forma | ¿Acertó? | Tutor solo | ¿Citó la página? | Vueltas | 2.ª vuelta | Veredicto | Semantic similarity | Segundos | Tokens de entrada | Tokens de salida | Costo (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| eval-01 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.859 | 6.67 | 6144 | 199 | 0.000714 |
| eval-02 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.898 | 7.76 | 5589 | 536 | 0.000827 |
| eval-03 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 6.44 | 5494 | 373 | 0.000736 |
| eval-04 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 6.11 | 5817 | 250 | 0.000707 |
| eval-05 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.946 | 6.34 | 5992 | 238 | 0.000718 |
| eval-06 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.861 | 6.31 | 5622 | 155 | 0.00064 |
| eval-07 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 5.07 | 5383 | 166 | 0.000621 |
| eval-08 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.899 | 5.85 | 5664 | 272 | 0.000702 |
| eval-09 | opciones | **No** | Sí | **No** | 2 | arruino | buscar_mas | 0.824 | 18.44 | 15148 | 1359 | 0.002194 |
| eval-10 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.88 | 7.36 | 5558 | 471 | 0.000791 |
| eval-11 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 6.08 | 5510 | 258 | 0.00068 |
| eval-12 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.86 | 8.85 | 5407 | 719 | 0.0009 |
| eval-13 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 6.05 | 5652 | 214 | 0.000672 |
| eval-14 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.959 | 5.31 | 5616 | 212 | 0.000668 |
| eval-15 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.955 | 6.77 | 5699 | 438 | 0.000789 |
| eval-16 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.895 | 5.02 | 5635 | 191 | 0.000659 |
| eval-17 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.942 | 4.74 | 5626 | 151 | 0.000638 |
| eval-18 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.916 | 6.35 | 5754 | 331 | 0.000741 |
| eval-19 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.894 | 6.46 | 5672 | 314 | 0.000724 |
| eval-20 | opciones | Sí | Sí | Sí | 1 | — | aprobada | 0.851 | 8.49 | 11781 | 403 | 0.00138 |
| eval-21 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.954 | 7.6 | 5825 | 532 | 0.000848 |
| eval-22 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.965 | 5.08 | 5196 | 200 | 0.00062 |
| eval-23 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.936 | 6.72 | 5486 | 394 | 0.000746 |
| eval-24 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.894 | 6.09 | 5571 | 279 | 0.000697 |
| eval-25 | libre | Sí | Sí | Sí | 2 | igual | aprobada | 0.969 | 14.48 | 14749 | 666 | 0.001808 |
| eval-26 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.903 | 4.88 | 5024 | 142 | 0.000573 |
| eval-27 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.907 | 6.3 | 5254 | 261 | 0.000656 |
| eval-28 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.953 | 6.65 | 5372 | 281 | 0.000678 |
| eval-29 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.889 | 5.77 | 5962 | 284 | 0.000738 |
| eval-30 | libre | Sí | Sí | Sí | 1 | — | aprobada | 0.949 | 6.94 | 5711 | 492 | 0.000817 |
