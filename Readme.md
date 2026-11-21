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

### Probar el flujo máximo

Desde la raíz del repositorio, ejecutar `python3 -B flujo.py` para calcular el flujo de `A` a `J` en la red inicial y ver el flujo y la capacidad de cada ruta.

`calcular_flujo_maximo(red, origen, destino)` devuelve el valor total y un diccionario de flujos por arco activo. La prueba de redirección por un arco residual inverso se ejecuta con `python3 -B -m unittest test_flujo`.
