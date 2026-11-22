from red import CENTROS_INICIALES, RUTAS_INICIALES, Red


def _buscar_anteriores(residual, origen, destino):
    # La busqueda en anchura sigue arcos con capacidad residual positiva
    # Guarda el centro anterior de cada centro alcanzado desde el origen
    # Si el destino es inalcanzable la busqueda recorre todo el lado del origen
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

    return anteriores


def _reconstruir_camino(anteriores, origen, destino):
    # Sigue los centros anteriores y devuelve los arcos de origen a destino
    camino = []
    centro = destino
    while centro != origen:
        anterior = anteriores[centro]
        camino.append((anterior, centro))
        centro = anterior
    camino.reverse()
    return camino


def calcular_flujo_y_corte(red, origen, destino):
    # Recibe una red y dos centros distintos
    # Devuelve el flujo maximo, los flujos por ruta activa y el corte minimo
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
        anteriores = _buscar_anteriores(residual, origen, destino)
        if destino not in anteriores:
            break

        camino = _reconstruir_camino(anteriores, origen, destino)
        # El menor espacio disponible limita lo que puede aumentar el flujo
        aumento = min(residual[inicio][fin] for inicio, fin in camino)
        for inicio, fin in camino:
            residual[inicio][fin] -= aumento
            # El arco residual inverso permite deshacer parte de este paso
            residual[fin][inicio] += aumento
        valor += aumento

    # En una ruta original, el flujo es la capacidad inicial menos la libre
    flujos = {
        (inicio, fin): capacidad - residual[inicio][fin]
        for (inicio, fin), capacidad in capacidades.items()
    }

    # La ultima busqueda alcanza todos los centros del lado del origen
    lado_origen = set(anteriores)
    lado_destino = set(red.centros) - lado_origen
    arcos_corte = {
        (inicio, fin): capacidad
        for (inicio, fin), capacidad in capacidades.items()
        if inicio in lado_origen and fin in lado_destino
    }
    corte = {
        "S": lado_origen,
        "T": lado_destino,
        "arcos": arcos_corte,
        "capacidad": sum(arcos_corte.values()),
    }
    return valor, flujos, corte


def calcular_flujo_maximo(red, origen, destino):
    # Recibe una red y dos centros distintos y devuelve el valor y los flujos
    valor, flujos, _ = calcular_flujo_y_corte(red, origen, destino)
    return valor, flujos


if __name__ == "__main__":
    red = Red(CENTROS_INICIALES, RUTAS_INICIALES)
    origen, destino = "A", "J"
    red.validar_configuracion_inicial(origen, destino)
    valor, flujos, corte = calcular_flujo_y_corte(red, origen, destino)
    print(f"Flujo maximo de {origen} a {destino}: {valor} paquetes/hora")
    print("Ruta | Flujo/Capacidad")
    for (inicio, fin), capacidad in red.rutas_activas().items():
        flujo = flujos[inicio, fin]
        print(f"{inicio} -> {fin} | {flujo}/{capacidad}")

    print("\nCorte minimo")
    for conjunto in ("S", "T"):
        centros = ", ".join(
            centro for centro in red.centros if centro in corte[conjunto]
        )
        print(conjunto, "= {" + centros + "}")
    print("Arcos de S a T | Capacidad")
    for (inicio, fin), capacidad in corte["arcos"].items():
        print(f"{inicio} -> {fin} | {capacidad}")
    print(f"Capacidad del corte: {corte['capacidad']} paquetes/hora")
