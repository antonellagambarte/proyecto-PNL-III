# Corridas del sistema completo

Cada corrida de `scripts.evaluar_sistema` suma una fila. Sirve para comparar antes y después de un cambio en `configs/config.yaml`.

- **p50** es la mediana: la mitad de las preguntas tarda (o gasta) eso o menos. **p95**: solo 5 de cada 100 tardan más.
- **Acierto:** en las de opciones, elegir la correcta. En las libres, que la respuesta traiga el dato clave (`clave` en el archivo de preguntas).
- **Tutor solo** es el borrador del tutor en la primera vuelta, antes de que lo revise el verificador.
- **Parecido** es la similitud de significado (coseno entre embeddings, como Semantic Similarity de RAGAS) entre la respuesta y la esperada, con el modelo de la búsqueda. Con este modelo los valores quedan entre 0,7 y 1: sirve para comparar, no como porcentaje de acierto.
- El costo usa los precios de `configs/config.yaml` y no descuenta la caché de OpenAI: es un techo.

| Corrida | Preguntas de | Candidatos | Fragmentos | Preguntas | Aciertos | Aciertos con opciones | Aciertos libres (dato clave) | Aciertos del tutor solo | Cita la página esperada | Sin respaldo | Con 2 vueltas | La 2.ª vuelta arregló / arruinó | Parecido p50 | Segundos p50 | Segundos p95 | Tutor p50 (s) | Verificador p50 (s) | Tokens de entrada p50 | Tokens de salida p50 | Costo p50 (US$) | Costo total (US$) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| antes | practica | 30 | 5 | 30 | 28 de 30 | 3 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 1 | 2 | 0 / 2 | 0.92 | 6.8 | 13.0 | 4.8 | 1.9 | 5658 | 288 | 0.0007 | 0.0248 |
| cuatro_fragmentos | practica | 30 | 4 | 30 | 27 de 30 | 3 de 5 | 24 de 25 | 29 de 30 | 29 de 30 | 0 | 3 | 0 / 2 | 0.92 | 8.3 | 23.6 | 5.5 | 2.3 | 4928 | 288 | 0.00065 | 0.0257 |
| veinte_candidatos | practica | 20 | 5 | 30 | 27 de 30 | 4 de 5 | 23 de 25 | 28 de 30 | 29 de 30 | 0 | 1 | 0 / 1 | 0.92 | 6.3 | 11.1 | 4.1 | 2.0 | 5656 | 294 | 0.00072 | 0.0246 |
| antes_2 | practica | 30 | 5 | 30 | 28 de 30 | 4 de 5 | 24 de 25 | 29 de 30 | 29 de 30 | 1 | 3 | 1 / 2 | 0.92 | 6.6 | 15.3 | 4.4 | 2.0 | 5618 | 286 | 0.00071 | 0.0279 |
| cuatro_fragmentos_2 | practica | 30 | 4 | 30 | 28 de 30 | 4 de 5 | 24 de 25 | 29 de 30 | 29 de 30 | 0 | 2 | 0 / 1 | 0.91 | 7.5 | 15.2 | 5.1 | 2.0 | 5014 | 290 | 0.00064 | 0.0248 |
| veinte_candidatos_2 | practica | 20 | 5 | 30 | 28 de 30 | 3 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 1 | 2 | 0 / 2 | 0.93 | 5.9 | 14.1 | 4.0 | 2.1 | 5612 | 282 | 0.00071 | 0.0252 |
| antes_3 | practica | 30 | 5 | 30 | 28 de 30 | 3 de 5 | 25 de 25 | 30 de 30 | 29 de 30 | 0 | 3 | 0 / 2 | 0.92 | 6.7 | 19.4 | 4.8 | 2.2 | 5678 | 312 | 0.00071 | 0.0285 |
| cuatro_fragmentos_3 | practica | 30 | 4 | 30 | 27 de 30 | 4 de 5 | 23 de 25 | 28 de 30 | 29 de 30 | 0 | 2 | 0 / 1 | 0.91 | 7.0 | 16.5 | 5.1 | 2.1 | 4938 | 306 | 0.00064 | 0.0238 |
| veinte_candidatos_3 | practica | 20 | 5 | 30 | 29 de 30 | 4 de 5 | 25 de 25 | 29 de 30 | 29 de 30 | 0 | 2 | 1 / 1 | 0.94 | 6.4 | 13.6 | 4.1 | 2.1 | 5615 | 302 | 0.00071 | 0.0258 |
