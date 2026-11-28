# Corridas del sistema completo

Cada corrida de `scripts.evaluar_sistema` suma una fila. Sirve para comparar antes y después de un cambio en `configs/config.yaml`.

- **p50 y p95:** mediana y percentil 95.
- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).
- **Tutor solo:** el borrador de la primera vuelta, antes del verificador. Muestra cuántas habría acertado el sistema sin verificador.
- **Semantic similarity:** coseno entre los embeddings de la respuesta y de la esperada, con el modelo de la búsqueda.
- **Costo:** con los precios de `configs/config.yaml`, sin el descuento de OpenAI por caché. El costo real puede ser algo menor.

| Corrida | Preguntas de | Candidatos | Fragmentos | Preguntas | Aciertos | Aciertos con opciones | Aciertos libres (dato clave) | Aciertos del tutor solo | Cita la página esperada | Sin respaldo | Con 2 vueltas | La 2.ª vuelta arregló / arruinó | Semantic similarity (promedio) | Segundos p50 | Segundos p95 | Tutor p50 (s) | Verificador p50 (s) | Tokens de entrada (promedio) | Tokens de salida (promedio) | Costo por pregunta (promedio, US$) | Costo total (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| antes | practica | 30 | 5 | 30 | 28 de 30 | 3 de 5 | 25 de 25 | 29 de 30 | 29 de 30 | 0 | 3 | 1 / 2 | 0.92 | 6.5 | 16.7 | 4.0 | 2.1 | 6495 | 418 | 0.00086 | 0.0258 |
| cuatro_fragmentos | practica | 30 | 4 | 30 | 29 de 30 | 5 de 5 | 24 de 25 | 29 de 30 | 29 de 30 | 0 | 1 | 0 / 0 | 0.92 | 6.8 | 12.0 | 4.5 | 2.2 | 5318 | 358 | 0.00071 | 0.0213 |
| veinte_candidatos | practica | 20 | 5 | 30 | 29 de 30 | 4 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 0 | 2 | 0 / 1 | 0.92 | 6.7 | 15.6 | 4.5 | 2.1 | 6552 | 376 | 0.00084 | 0.0253 |
| antes_2 | practica | 30 | 5 | 30 | 28 de 30 | 4 de 5 | 24 de 25 | 29 de 30 | 28 de 30 | 0 | 1 | 0 / 1 | 0.92 | 7.0 | 9.8 | 4.5 | 2.2 | 6287 | 367 | 0.00081 | 0.0244 |
| cuatro_fragmentos_2 | practica | 30 | 4 | 30 | 28 de 30 | 4 de 5 | 24 de 25 | 29 de 30 | 29 de 30 | 1 | 1 | 0 / 1 | 0.92 | 6.7 | 11.7 | 4.5 | 2.3 | 5571 | 373 | 0.00074 | 0.0223 |
| veinte_candidatos_2 | practica | 20 | 5 | 30 | 29 de 30 | 4 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 1 | 2 | 0 / 1 | 0.92 | 6.3 | 11.9 | 4.0 | 2.2 | 6430 | 359 | 0.00082 | 0.0247 |
| antes_3 | practica | 30 | 5 | 30 | 28 de 30 | 3 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 0 | 3 | 0 / 2 | 0.92 | 6.6 | 18.9 | 4.2 | 2.3 | 7221 | 395 | 0.00092 | 0.0276 |
| cuatro_fragmentos_3 | practica | 30 | 4 | 30 | 28 de 30 | 3 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 0 | 3 | 0 / 2 | 0.92 | 7.0 | 16.0 | 4.4 | 2.2 | 5949 | 394 | 0.00079 | 0.0238 |
| veinte_candidatos_3 | practica | 20 | 5 | 30 | 29 de 30 | 4 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 0 | 1 | 0 / 1 | 0.92 | 7.2 | 11.6 | 4.8 | 2.2 | 6410 | 339 | 0.00081 | 0.0243 |
