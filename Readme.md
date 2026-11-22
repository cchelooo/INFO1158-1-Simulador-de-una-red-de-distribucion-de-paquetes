## Proyecto 2
### Simulación Simulador de una red de distribución de paquetes
- `Interfaz`: Martin 
- `Codigo`: Marcelo
- `Calculos`: Yaninna
---
- **Ford–Fulkerson con DFS.** Busca cada camino aumentante en profundidad en la red residual. El camino depende del orden de exploración. Con capacidades enteras, su tiempo está acotado por $O(E \cdot |f^*|)$, donde $|f^*|$ es el flujo máximo. [MIT 6.046J, sección 13.1](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2012/7c2927794e61bd70c14c07728fa54375_MIT6_046JS12_lec13.pdf)
- **Edmonds–Karp.** Es la variante de Ford–Fulkerson que usa búsqueda en anchura (BFS) para elegir el camino aumentante con menos arcos. La elegimos porque BFS permite seguir la búsqueda por capas y da una cota $O(VE^2)$ que depende del tamaño de la red. [MIT 6.046J, sección 13.1.3](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2012/7c2927794e61bd70c14c07728fa54375_MIT6_046JS12_lec13.pdf) · [Edmonds y Karp, 1972, sección 1.2](https://web.eecs.umich.edu/~pettie/matching/Edmonds-Karp-network-flow.pdf)
- `Teorema de flujo máximo-corte mínimo`: Establece que en cualquier red de flujo, el valor máximo que puede viajar de la fuente al sumidero es exactamente igual a la capacidad mínima del corte que separa la fuente del sumidero (el cuello de botella de la red). Es la base teórica que demuestra cuándo se ha alcanzado el flujo máximo.
- `NO`: Lazos, arcos repetidos ni arcos recíprocos.

```
 La aplicación deberá permitir realizar las siguientes modificaciones desde la interfaz, sin editar el
código fuente:
Desactivar una ruta existente.
Modificar la capacidad de una ruta.
Agregar una nueva conexión
```

### Probar el flujo máximo y el corte mínimo

Desde la raíz del repositorio, ejecutar `python3 -B flujo.py` para calcular el flujo de `A` a `J` en la red inicial. La salida muestra el flujo y la capacidad de cada ruta, los conjuntos `S` y `T`, los arcos del corte y su capacidad total.

`calcular_flujo_y_corte(red, origen, destino)` devuelve `(valor, flujos, corte)`. `flujos` contiene el flujo por arco activo, y `corte` contiene `S`, `T`, `arcos` (con sus capacidades) y `capacidad` (la suma de esas capacidades). `calcular_flujo_maximo` mantiene el retorno `(valor, flujos)`.

En la red residual final, `S` reúne los centros alcanzables desde el origen mediante arcos con capacidad residual positiva, incluidos los inversos. Los demás centros forman `T`. La capacidad del corte se calcula con las rutas activas originales que van de `S` a `T`. [MIT 6.046J, sección 13.2](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2012/7c2927794e61bd70c14c07728fa54375_MIT6_046JS12_lec13.pdf)

### Comprobación manual con cinco centros

El origen es `O` y el destino es `J`. Las capacidades y los flujos están en paquetes por hora.

| Ruta | Capacidad | Flujo manual | Flujo del código |
| --- | ---: | ---: | ---: |
| O → A | 1 | 1 | 1 |
| O → B | 2 | 1 | 1 |
| A → C | 1 | 1 | 1 |
| B → C | 1 | 0 | 0 |
| B → J | 1 | 1 | 1 |
| C → J | 1 | 1 | 1 |

**Flujo factible.** Se envía un paquete por hora por `O → A → C → J` y otro por `O → B → J`. Cada ruta respeta su capacidad y en cada centro intermedio (`A`, `B` y `C`) entra y sale un paquete por hora. El flujo neto que sale de `O` es **2**.

**Corte.** Con `S = {O, A, B, C}` y `T = {J}`, cruzan las rutas `B → J` y `C → J`. La capacidad del corte es `1 + 1 = 2`. Este corte pone un límite superior de 2 y el flujo construido alcanza ese límite, así que ambos resultados son óptimos.

El código obtiene los mismos flujos, la misma partición y la misma capacidad. Para comprobarlo, ejecutar `python3 -B -m unittest -v test_flujo`.
