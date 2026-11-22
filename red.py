class Red:
    # Recibe centros y rutas en el formato (origen, destino, capacidad)
    def __init__(self, centros, rutas=()):
        self.centros = tuple(centros)
        if len(set(self.centros)) != len(self.centros):
            raise ValueError("Hay centros repetidos.")

        self._capacidades = {}
        self._desactivadas = set()
        for origen, destino, capacidad in rutas:
            self.agregar_ruta(origen, destino, capacidad)

    # Registra una nueva ruta activa si cumple las reglas de la red
    def agregar_ruta(self, origen, destino, capacidad):
        if origen not in self.centros or destino not in self.centros:
            raise ValueError("Los dos centros deben pertenecer a la red.")
        if origen == destino:
            raise ValueError("La red no admite lazos.")
        if (origen, destino) in self._capacidades:
            raise ValueError("La ruta ya existe.")
        if (destino, origen) in self._capacidades:
            raise ValueError("La red no admite rutas reciprocas.")
        self._validar_capacidad(capacidad)
        self._capacidades[(origen, destino)] = capacidad

    @staticmethod
    def _validar_capacidad(capacidad):
        if type(capacidad) is not int or not 1 <= capacidad <= 12:
            raise ValueError("La capacidad debe ser un entero entre 1 y 12.")

    def modificar_capacidad(self, origen, destino, capacidad):
        # Cambia cuantos paquetes admite la ruta y deja igual su estado
        arco = (origen, destino)
        if arco not in self._capacidades:
            raise ValueError("La ruta no existe.")
        self._validar_capacidad(capacidad)
        self._capacidades[arco] = capacidad

    # Quita una ruta de los recorridos disponibles y conserva su capacidad
    def desactivar_ruta(self, origen, destino):
        arco = (origen, destino)
        if arco not in self._capacidades:
            raise ValueError("La ruta no existe.")
        self._desactivadas.add(arco)

    def reactivar_ruta(self, origen, destino):
        # Vuelve a abrir una ruta con la capacidad que ya tenia
        arco = (origen, destino)
        if arco not in self._capacidades:
            raise ValueError("La ruta no existe.")
        self._desactivadas.discard(arco)

    def rutas(self):
        # Incluye las rutas apagadas para que se puedan dibujar en la ventana
        return self._capacidades.copy()

    # Devuelve un diccionario con cada arco activo y su capacidad
    def rutas_activas(self):
        return {
            arco: capacidad
            for arco, capacidad in self._capacidades.items()
            if arco not in self._desactivadas
        }

    # Comprueba las condiciones iniciales del proyecto para el par elegido
    # Si alguna no se cumple, indica el problema mediante ValueError
    def validar_configuracion_inicial(self, origen, destino):
        if origen not in self.centros or destino not in self.centros:
            raise ValueError("Los dos centros deben pertenecer a la red.")
        if origen == destino:
            raise ValueError("El origen y el destino deben ser distintos.")

        rutas = self.rutas_activas()
        if not 10 <= len(self.centros) <= 12:
            raise ValueError("La red inicial debe tener entre 10 y 12 centros.")
        if not 15 <= len(rutas) <= 20:
            raise ValueError("La red inicial debe tener entre 15 y 20 rutas activas.")

        vecinos = {centro: [] for centro in self.centros}
        centros_conectados = set()
        for inicio, fin in rutas:
            vecinos[inicio].append(fin)
            centros_conectados.update((inicio, fin))
        if len(centros_conectados) != len(self.centros):
            raise ValueError("La red inicial no puede tener centros aislados.")

        # Explora caminos dirigidos y se detiene al encontrar dos distintos
        pendientes = [(origen,)]
        encontrados = 0
        while pendientes:
            camino = pendientes.pop()
            ultimo = camino[-1]
            if ultimo == destino:
                encontrados += 1
                if encontrados == 2:
                    return
                continue

            for vecino in vecinos[ultimo]:
                if vecino not in camino:
                    pendientes.append(camino + (vecino,))

        raise ValueError("Deben existir al menos dos caminos del origen al destino.")


def clasificar_recorrido(red, secuencia):
    # Recibe una red y una secuencia de centros
    # Devuelve un valor booleano para cada categoria de la secuencia
    vertices = tuple(secuencia)
    arcos = list(zip(vertices, vertices[1:]))
    rutas = red.rutas_activas()
    recorrido = (
        bool(vertices)
        and all(vertice in red.centros for vertice in vertices)
        and all(arco in rutas for arco in arcos)
    )

    sendero = recorrido and len(set(arcos)) == len(arcos)
    camino = recorrido and len(set(vertices)) == len(vertices)
    cerrado = recorrido and vertices[0] == vertices[-1]
    circuito = sendero and cerrado

    # Un circuito puede tener longitud cero
    # Un ciclo requiere tres arcos como minimo y solo repite el centro del cierre
    ciclo = (
        cerrado
        and len(arcos) >= 3
        and len(set(vertices[:-1])) == len(arcos)
    )

    return {
        "recorrido": recorrido,
        "sendero": sendero,
        "camino": camino,
        "circuito": circuito,
        "ciclo": ciclo,
    }


# Centros y capacidades de la red de demostracion de la rama Martin
CENTROS_INICIALES = ("A", "B", "C", "D", "E", "F", "G", "H", "I", "J")
RUTAS_INICIALES = (
    ("A", "B", 8),
    ("A", "C", 6),
    ("B", "D", 5),
    ("B", "E", 4),
    ("C", "D", 3),
    ("C", "F", 7),
    ("D", "E", 4),
    ("D", "G", 6),
    ("E", "H", 5),
    ("F", "G", 8),
    ("F", "I", 4),
    ("G", "H", 6),
    ("G", "I", 3),
    ("H", "J", 7),
    ("I", "J", 9),
    ("E", "I", 2),
)


def _mostrar_clasificacion(red, secuencia):
    # Imprime las categorias que cumple una secuencia para la demostracion
    resultado = clasificar_recorrido(red, secuencia)
    categorias = [nombre for nombre, cumple in resultado.items() if cumple]
    print(" -> ".join(secuencia), "|", ", ".join(categorias) or "recorrido invalido")


if __name__ == "__main__":
    red = Red(CENTROS_INICIALES, RUTAS_INICIALES)
    red.validar_configuracion_inicial("A", "J")
    print(f"Red inicial valida: {len(red.centros)} centros y {len(red.rutas_activas())} rutas.")
    _mostrar_clasificacion(red, ("A", "B", "D"))
    _mostrar_clasificacion(red, ("A", "B", "A"))

    red.desactivar_ruta("A", "B")
    print("\nDespues de desactivar A -> B:")
    _mostrar_clasificacion(red, ("A", "B", "D"))

    # Los dos triangulos dirigidos permiten comparar un ciclo y un circuito
    red_ejemplo = Red(
        ("A", "B", "C", "D", "E"),
        (
            ("A", "B", 1),
            ("B", "C", 1),
            ("C", "A", 1),
            ("A", "D", 1),
            ("D", "E", 1),
            ("E", "A", 1),
        ),
    )
    print("\nRed auxiliar con dos triangulos dirigidos:")
    _mostrar_clasificacion(red_ejemplo, ("A", "B", "C", "A"))
    _mostrar_clasificacion(red_ejemplo, ("A", "B", "C", "A", "D", "E", "A"))
