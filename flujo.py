from red import CENTROS_INICIALES, RUTAS_INICIALES, Red


def _buscar_camino_aumentante(residual, origen, destino):
    # BFS recorre los arcos con capacidad residual positiva.
    # Devuelve el camino con menos arcos, o una lista vacia si no existe.
    anteriores = {origen: None}
    cola = [origen]
    indice = 0
    while indice < len(cola) and destino not in anteriores:
        centro = cola[indice]
        indice += 1
        for vecino, capacidad in residual[centro].items():
            if capacidad > 0 and vecino not in anteriores:
                anteriores[vecino] = centro
                cola.append(vecino)

    if destino not in anteriores:
        return []

    camino = []
    centro = destino
    while centro != origen:
        anterior = anteriores[centro]
        camino.append((anterior, centro))
        centro = anterior
    camino.reverse()
    return camino


def calcular_flujo_maximo(red, origen, destino):
    # Recibe una Red y dos centros distintos. Devuelve el valor del flujo
    # maximo y un diccionario con el flujo de cada ruta activa original.
    if origen not in red.centros or destino not in red.centros:
        raise ValueError("Los dos centros deben pertenecer a la red.")
    if origen == destino:
        raise ValueError("El origen y el destino deben ser distintos.")

    capacidades = red.rutas_activas()
    residual = {centro: {} for centro in red.centros}
    for (inicio, fin), capacidad in capacidades.items():
        residual[inicio][fin] = capacidad
        residual[fin][inicio] = 0

    valor = 0
    while True:
        camino = _buscar_camino_aumentante(residual, origen, destino)
        if not camino:
            break

        # El menor espacio disponible limita lo que puede aumentar el flujo.
        aumento = min(residual[inicio][fin] for inicio, fin in camino)
        for inicio, fin in camino:
            residual[inicio][fin] -= aumento
            # El arco residual inverso permite deshacer parte de este paso.
            residual[fin][inicio] += aumento
        valor += aumento

    # En una ruta original, el flujo es la capacidad inicial menos la libre.
    flujos = {
        (inicio, fin): capacidad - residual[inicio][fin]
        for (inicio, fin), capacidad in capacidades.items()
    }
    return valor, flujos


if __name__ == "__main__":
    red = Red(CENTROS_INICIALES, RUTAS_INICIALES)
    origen, destino = "A", "J"
    red.validar_configuracion_inicial(origen, destino)
    valor, flujos = calcular_flujo_maximo(red, origen, destino)
    print(f"Flujo maximo de {origen} a {destino}: {valor} paquetes/hora")
    print("Ruta | Flujo/Capacidad")
    for (inicio, fin), capacidad in red.rutas_activas().items():
        flujo = flujos[inicio, fin]
        print(f"{inicio} -> {fin} | {flujo}/{capacidad}")
