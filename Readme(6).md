## Proyecto 2
### Simulación Simulador de una red de distribución de paquetes
- `Interfaz`: Martin 
- `Codigo`: Marcelo
- `Calculos`: Yaninna
---
- `Ford-Fulkerson (Método)`: Es un enfoque general para encontrar el flujo máximo en una red buscando repetidamente "caminos aumentantes" (caminos desde la fuente hasta el sumidero con capacidad disponible) y sumando flujo. Se le llama método (y no algoritmo) porque su eficiencia depende de cómo elijas esos caminos; si se eligen mal con capacidades con números reales, podría no terminar nunca.
- `Edmonds-Karp (Algoritmo)`: Es una implementación específica y segura del método de Ford-Fulkerson. Utiliza BFS (Búsqueda en Anchura) para encontrar siempre el camino aumentante con menor cantidad de aristas. Esto garantiza que el algoritmo siempre termine y tenga una complejidad polinómica eficiente ($O(V E^2)$).
- `Teorema de flujo máximo-corte mínimo`: Establece que en cualquier red de flujo, el valor máximo que puede viajar de la fuente al sumidero es exactamente igual a la capacidad mínima del corte que separa la fuente del sumidero (el cuello de botella de la red). Es la base teórica que demuestra cuándo se ha alcanzado el flujo máximo.
- `NO`: Lazos, arcos repetidos ni arcos recíprocos.

```
 La aplicación deberá permitir realizar las siguientes modificaciones desde la interfaz, sin editar el
código fuente:
Desactivar una ruta existente.
Modificar la capacidad de una ruta.
Agregar una nueva conexión
```