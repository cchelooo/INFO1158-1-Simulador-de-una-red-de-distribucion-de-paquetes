import tkinter as tk
from tkinter import ttk, messagebox
import tkinterplus
import math
try:
    from flujo import calcular_flujo_maximo
except ImportError:
    calcular_flujo_maximo = None
from red import Red, CENTROS_INICIALES, RUTAS_INICIALES

# Colores
FONDO = "#101827"
PANEL = "#1E293B"
TEXTO = "#FFFFFF"
SECUNDARIO = "#A8B3C7"
AZUL = "#3B82F6"

# Ventana principal
ventana = tk.Tk()
ventana.title("Simulador de Red de Distribución de Paquetes")
ventana.geometry("1200x750")
ventana.minsize(1000, 600)
ventana.configure(bg=FONDO)

# Encabezado
encabezado = tk.Frame(ventana, bg=FONDO)
encabezado.pack(fill="x", padx=20, pady=(20, 15))

tk.Label(
    encabezado,
    text="SIMULADOR DE DISTRIBUCIÓN DE PAQUETES",
    font=("Arial", 20, "bold"),
    bg=FONDO,
    fg=TEXTO
).pack(anchor="w")

tk.Label(
    encabezado,
    text="Teoría de Grafos | INFO1158",
    font=("Arial", 11),
    bg=FONDO,
    fg=SECUNDARIO
).pack(anchor="w", pady=(5, 0))

# Contenedor principal
contenido = tk.Frame(ventana, bg=FONDO)
contenido.pack(fill="both", expand=True, padx=20, pady=(0, 20))

contenido.grid_rowconfigure(0, weight=1)
contenido.grid_columnconfigure(0, weight=0, minsize=240)
contenido.grid_columnconfigure(1, weight=1)
contenido.grid_columnconfigure(2, weight=0, minsize=260)

def agregar_conexion():
    # Crear ventana secundaria
    ventana_agregar = tk.Toplevel(ventana)
    ventana_agregar.title("Agregar conexión")
    ventana_agregar.geometry("350x350")
    ventana_agregar.resizable(False, False)
    ventana_agregar.configure(bg=PANEL)
    ventana_agregar.transient(ventana)
    ventana_agregar.grab_set()

    tk.Label(
        ventana_agregar,
        text="AGREGAR NUEVA CONEXIÓN",
        font=("Arial", 13, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=20)

    centros = list(red.centros)

    # Seleccionar origen
    tk.Label(
        ventana_agregar,
        text="Centro de origen",
        bg=PANEL,
        fg=TEXTO
    ).pack()

    nuevo_origen = ttk.Combobox(
        ventana_agregar,
        values=centros,
        state="readonly"
    )
    nuevo_origen.pack(pady=5)

    # Seleccionar destino
    tk.Label(
        ventana_agregar,
        text="Centro de destino",
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=(10, 0))

    nuevo_destino = ttk.Combobox(
        ventana_agregar,
        values=centros,
        state="readonly"
    )
    nuevo_destino.pack(pady=5)

    # Seleccionar capacidad
    tk.Label(
        ventana_agregar,
        text="Capacidad (1 a 12)",
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=(10, 0))

    nueva_capacidad = ttk.Combobox(
        ventana_agregar,
        values=list(range(1, 13)),
        state="readonly"
    )
    nueva_capacidad.pack(pady=5)

    def guardar_conexion():
        inicio = nuevo_origen.get()
        fin = nuevo_destino.get()
        capacidad = nueva_capacidad.get()

        if not inicio or not fin or not capacidad:
            messagebox.showwarning(
                "Datos incompletos",
                "Debes completar todos los campos.",
                parent=ventana_agregar
            )
            return

        if inicio == fin:
            messagebox.showerror(
                "Conexión inválida",
                "Un centro no puede conectarse consigo mismo.",
                parent=ventana_agregar
            )
            return

        
        
        # Si la ruta existe, comprobar si está desactivada
        if (
            (inicio, fin) in red.todas_las_rutas()
            and not red.ruta_esta_activa(inicio, fin)
        ):
            reactivar = messagebox.askyesno(
                "Ruta desactivada",
                f"La ruta {inicio} → {fin} está desactivada.\n\n"
                f"¿Deseas reactivarla con capacidad {capacidad}?",
                parent=ventana_agregar
            )

            
            if reactivar:
                try:
                    red.modificar_capacidad(inicio, fin, int(capacidad))
                    red.reactivar_ruta(inicio, fin)

                except ValueError as error:
                    messagebox.showerror(
                        "Error al reactivar",
                        str(error),
                        parent=ventana_agregar
                    )
                    return



                # Comprobación temporal
                print(f"Ruta reactivada: {inicio} -> {fin}")
                print("Rutas activas:", len(red.rutas_activas()))
                print("¿La ruta sigue activa?",
                      (inicio, fin) in red.rutas_activas())

                invalidar_resultado()
                ventana_agregar.destroy()

            return

        # Registrar la conexión en la clase Red
        try:
            red.agregar_ruta(inicio, fin, int(capacidad))

        except ValueError as error:
            messagebox.showerror(
                "Conexión inválida",
                str(error),
                parent=ventana_agregar
            )
            return
        


        invalidar_resultado()
        ventana_agregar.destroy()

        messagebox.showinfo(
            "Conexión agregada",
            f"Se agregó la ruta {inicio} → {fin} "
            f"con capacidad {capacidad}."
        )

    tk.Button(
        ventana_agregar,
        text="Guardar conexión",
        command=guardar_conexion,
        bg=AZUL,
        fg="white",
        font=("Arial", 10, "bold"),
        relief="flat"
    ).pack(pady=20)


def modificar_capacidad():
    ventana_modificar = tk.Toplevel(ventana)
    ventana_modificar.title("Modificar capacidad")
    ventana_modificar.geometry("380x320")
    ventana_modificar.resizable(False, False)
    ventana_modificar.configure(bg=PANEL)
    ventana_modificar.transient(ventana)
    ventana_modificar.grab_set()

    tk.Label(
        ventana_modificar,
        text="MODIFICAR CAPACIDAD",
        font=("Arial", 13, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=20)

    # Obtener rutas actuales
    rutas_disponibles = [
    (inicio, fin, capacidad)
    for (inicio, fin), capacidad in red.todas_las_rutas().items()
]

    opciones = [
        f"{inicio} → {fin} (Capacidad: {capacidad})"
        for inicio, fin, capacidad in rutas_disponibles
    ]

    tk.Label(
        ventana_modificar,
        text="Selecciona una ruta",
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=5)

    seleccion_ruta = ttk.Combobox(
        ventana_modificar,
        values=opciones,
        state="readonly",
        width=32
    )
    seleccion_ruta.pack(pady=5)

    tk.Label(
        ventana_modificar,
        text="Nueva capacidad (1 a 12)",
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=(15, 5))

    seleccion_capacidad = ttk.Combobox(
        ventana_modificar,
        values=list(range(1, 13)),
        state="readonly"
    )
    seleccion_capacidad.pack(pady=5)

    def guardar_cambio():
        indice = seleccion_ruta.current()
        capacidad = seleccion_capacidad.get()

        if indice == -1 or not capacidad:
            messagebox.showwarning(
                "Datos incompletos",
                "Selecciona una ruta y una capacidad.",
                parent=ventana_modificar
            )
            return
        
        inicio, fin, anterior = rutas_disponibles[indice]
        nueva = int(capacidad)

        # Actualizar la capacidad en red.py
        try:
            red.modificar_capacidad(inicio, fin, nueva)

        except ValueError as error:
            messagebox.showerror(
                "Capacidad inválida",
                str(error),
                parent=ventana_modificar
            )
            return



        # Comprobación temporal
        print("Capacidad en red.py:",
              red.todas_las_rutas().get((inicio, fin)))


        invalidar_resultado()
        ventana_modificar.destroy()

        messagebox.showinfo(
            "Capacidad actualizada",
            f"Ruta {inicio} → {fin}\n"
            f"Capacidad anterior: {anterior}\n"
            f"Nueva capacidad: {nueva}",
            parent=ventana
        )

    tk.Button(
        ventana_modificar,
        text="Guardar cambios",
        command=guardar_cambio,
        bg=AZUL,
        fg="white",
        relief="flat",
        font=("Arial", 10, "bold")
    ).pack(pady=20)


def desactivar_ruta():
    ventana_desactivar = tk.Toplevel(ventana)
    ventana_desactivar.title("Desactivar ruta")
    ventana_desactivar.geometry("380x280")
    ventana_desactivar.resizable(False, False)
    ventana_desactivar.configure(bg=PANEL)
    ventana_desactivar.transient(ventana)
    ventana_desactivar.grab_set()

    tk.Label(
        ventana_desactivar,
        text="DESACTIVAR RUTA",
        font=("Arial", 13, "bold"),
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=20)

    # Mostrar solamente las rutas activas
    rutas_activas = [
        (inicio, fin, capacidad)
        for (inicio, fin), capacidad in red.rutas_activas().items()
    ]

    opciones = [
        f"{inicio} → {fin} (Capacidad: {capacidad})"
        for inicio, fin, capacidad in rutas_activas
    ]

    tk.Label(
        ventana_desactivar,
        text="Selecciona la ruta que deseas desactivar",
        bg=PANEL,
        fg=TEXTO
    ).pack(pady=10)

    seleccion = ttk.Combobox(
        ventana_desactivar,
        values=opciones,
        state="readonly",
        width=32
    )
    seleccion.pack(pady=5)

    def confirmar_desactivacion():
        indice = seleccion.current()

        if indice == -1:
            messagebox.showwarning(
                "Ruta no seleccionada",
                "Debes seleccionar una ruta.",
                parent=ventana_desactivar
            )
            return

        inicio, fin, capacidad = rutas_activas[indice]

        confirmar = messagebox.askyesno(
            "Confirmar desactivación",
            f"¿Deseas desactivar la ruta {inicio} → {fin}?",
            parent=ventana_desactivar
        )

        if not confirmar:
            return

        
        # Desactivar la ruta en red.py
        try:
            red.desactivar_ruta(inicio, fin)

        except ValueError as error:
            messagebox.showerror(
                "Error al desactivar",
                str(error),
                parent=ventana_desactivar
            )
            return



        # Comprobación temporal
        print(f"Ruta desactivada: {inicio} -> {fin}")
        print("Rutas activas:", len(red.rutas_activas()))
        print("¿La ruta sigue activa?",
              (inicio, fin) in red.rutas_activas())

        invalidar_resultado()
        ventana_desactivar.destroy()

        messagebox.showinfo(
            "Ruta desactivada",
            f"La ruta {inicio} → {fin} fue desactivada.",
            parent=ventana
        )

    tk.Button(
        ventana_desactivar,
        text="Desactivar ruta",
        command=confirmar_desactivacion,
        bg="#DC2626",
        fg="white",
        relief="flat",
        font=("Arial", 10, "bold")
    ).pack(pady=25)

def restablecer_red():
    global red

    confirmar = messagebox.askyesno(
        "Restablecer red",
        "¿Deseas restaurar la red original?\n\n"
        "Se perderán las conexiones agregadas, "
        "los cambios de capacidad y las desactivaciones.",
        parent=ventana
    )

    if not confirmar:
        return

    # Restablecer la red de Marcelo
    red = Red(CENTROS_INICIALES, RUTAS_INICIALES)

    # Comprobación en la terminal
    print("\nRed original restablecida")
    print("Centros:", len(red.centros))
    print("Rutas activas en red.py:", len(red.rutas_activas()))
    print("Rutas en interfaz:", len(red.todas_las_rutas()))
    print("Rutas desactivadas:", len(red.todas_las_rutas()) - len(red.rutas_activas()))
    print("Capacidad A -> B:", red.rutas_activas().get(("A", "B")))

    # Actualizar la representación gráfica
    invalidar_resultado()

    messagebox.showinfo(
        "Red restablecida",
        "La red original se restauró correctamente.",
        parent=ventana
    )

resultado = None
escenarios = []

def invalidar_resultado(event=None):
    global resultado
    resultado = None
    valor_flujo.config(text="—")
    detalle_corte.config(text="Conjunto S: pendiente\nConjunto T: pendiente")
    dibujar_red()

def ejecutar_flujo():
    global resultado
    if origen.get() == destino.get():
        messagebox.showwarning("Selección inválida", "Origen y destino deben ser distintos.", parent=ventana)
        return
    if calcular_flujo_maximo is None:
        return
    try:
        resultado = calcular_flujo_maximo(red, origen.get(), destino.get())
        valor_flujo.config(text=str(resultado["valor"]))
        detalle_corte.config(text="S: " + ", ".join(sorted(resultado["S"])) + "\nT: " + ", ".join(sorted(resultado["T"])) + "\nCapacidad: " + str(resultado["capacidad_corte"]) + "\nArcos: " + ", ".join(f"{a}→{b}" for a,b in resultado["corte"]))
        dibujar_red()
    except (ValueError, KeyError, TypeError) as error:
        invalidar_resultado()
        messagebox.showerror("Error de cálculo", str(error), parent=ventana)

def guardar_escenario():
    if resultado is None:
        messagebox.showinfo("Escenarios", "Calcula el flujo antes de guardar un escenario.", parent=ventana)
        return
    escenarios.append((origen.get(), destino.get(), resultado["valor"], resultado["capacidad_corte"], red.todas_las_rutas(), red.rutas_activas()))
    comparar_escenarios()

def comparar_escenarios():
    dialogo = tk.Toplevel(ventana)
    dialogo.title("Comparación de escenarios")
    tabla = ttk.Treeview(dialogo, columns=("par", "flujo", "corte", "activas", "cambios"), show="headings")
    for col, titulo in zip(tabla["columns"], ("Origen / destino", "Flujo máximo", "Corte mínimo", "Rutas activas", "Cambios respecto a inicial")):
        tabla.heading(col, text=titulo)
        tabla.column(col, width=150 if col != "cambios" else 300)
    inicial = {(a,b):c for a,b,c in RUTAS_INICIALES}
    for i,(a,b,f,c,todas,activas) in enumerate(escenarios,1):
        cambios = [f"{u}→{v}: {inicial.get((u,v), 'nueva')} → {cap}" for (u,v),cap in todas.items() if inicial.get((u,v)) != cap]
        cambios += [f"{u}→{v}: inactiva" for u,v in todas if (u,v) not in activas]
        tabla.insert("", "end", values=(f"{i}. {a} → {b}", f,c,len(activas), "; ".join(cambios) or "Original"))
    tabla.pack(fill="both", expand=True)

# Panel izquierdo
panel_izquierdo = tk.Frame(contenido, bg=PANEL)
panel_izquierdo.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

tk.Label(
    panel_izquierdo,
    text="CONTROLES",
    font=("Arial", 14, "bold"),
    bg=PANEL,
    fg=TEXTO
).pack(pady=20)

tk.Label(
    panel_izquierdo,
    text="Centro de origen",
    bg=PANEL,
    fg=SECUNDARIO
).pack(anchor="w", padx=15)

origen = ttk.Combobox(
    panel_izquierdo,
    values=CENTROS_INICIALES,
    state="readonly"
)
origen.pack(fill="x", padx=15, pady=(5, 15))
origen.set("A")

tk.Label(
    panel_izquierdo,
    text="Centro de destino",
    bg=PANEL,
    fg=SECUNDARIO
).pack(anchor="w", padx=15)

destino = ttk.Combobox(
    panel_izquierdo,
    values=CENTROS_INICIALES,
    state="readonly"
)
destino.pack(fill="x", padx=15, pady=(5, 20))
destino.set("J")

tk.Button(
    panel_izquierdo,
    text="Calcular flujo máximo",
    bg=AZUL,
    fg=TEXTO,
    relief="flat",
    font=("Arial", 10, "bold"),
    command=ejecutar_flujo,
    state="normal" if calcular_flujo_maximo else "disabled"
).pack(fill="x", padx=15, pady=5)

tk.Label(
    panel_izquierdo,
    text="MODIFICAR RED",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=TEXTO
).pack(pady=(35, 15))


tk.Button(
    panel_izquierdo,
    text="Agregar conexión",
    command=agregar_conexion,
    bg=AZUL,
    fg="white",
    relief="flat",
    font=("Arial", 10, "bold")
).pack(fill="x", padx=15, pady=5)

tk.Button(
    panel_izquierdo,
    text="Modificar capacidad",
    command=modificar_capacidad,
    bg=AZUL,
    fg="white",
    relief="flat",
    font=("Arial", 10, "bold")
).pack(fill="x", padx=15, pady=5)

tk.Button(
    panel_izquierdo,
    text="Desactivar ruta",
    command=desactivar_ruta,
    bg="#DC2626",
    fg="white",
    relief="flat",
    font=("Arial", 10, "bold")
).pack(fill="x", padx=15, pady=5)


tk.Button(
    panel_izquierdo,
    text="Restablecer red",
    command=restablecer_red,
    bg="#475569",
    fg="white",
    relief="flat",
    font=("Arial", 10, "bold")
).pack(fill="x", padx=15, pady=(20, 5))


# Panel central
panel_central = tk.Frame(contenido, bg=PANEL)
panel_central.grid(row=0, column=1, sticky="nsew", padx=5)

tk.Label(
    panel_central,
    text="RED LOGÍSTICA",
    font=("Arial", 14, "bold"),
    bg=PANEL,
    fg=TEXTO
).pack(pady=20)

canvas = tk.Canvas(
    panel_central,
    bg="#172033",
    highlightthickness=0
)
canvas.pack(fill="both", expand=True, padx=15, pady=(0, 15))


# Crear la red utilizando el código de Marcelo
red = Red(CENTROS_INICIALES, RUTAS_INICIALES)

print("Red de Marcelo conectada correctamente")
print("Centros:", len(red.centros))
print("Rutas activas:", len(red.rutas_activas()))

# Posiciones proporcionales dentro del Canvas
posiciones = {
    "A": (0.08, 0.50),
    "B": (0.28, 0.25),
    "C": (0.28, 0.75),
    "D": (0.47, 0.15),
    "E": (0.47, 0.32),
    "F": (0.47, 0.85),
    "G": (0.67, 0.46),
    "H": (0.82, 0.12),
    "I": (0.67, 0.75),
    "J": (0.92, 0.55)
}

def dibujar_red(event=None):
    canvas.delete("all")

    ancho = canvas.winfo_width()
    alto = canvas.winfo_height()

    if ancho < 100 or alto < 100:
        return

    radio = 18

    coordenadas = {
        nodo: (x * ancho, y * alto)
        for nodo, (x, y) in posiciones.items()
    }

    # Dibujar rutas y capacidades
    for (inicio, fin), capacidad in red.todas_las_rutas().items():
        desactivada = not red.ruta_esta_activa(inicio, fin)
        x1, y1 = coordenadas[inicio]
        x2, y2 = coordenadas[fin]

        dx = x2 - x1
        dy = y2 - y1
        distancia = math.hypot(dx, dy)

        if distancia == 0:
            continue

        ux = dx / distancia
        uy = dy / distancia

        # Separar la flecha de los centros
        sx = x1 + ux * radio
        sy = y1 + uy * radio
        ex = x2 - ux * (radio + 5)
        ey = y2 - uy * (radio + 5)

        canvas.create_line(
            sx, sy, ex, ey,
            fill="#F87171" if desactivada else ("#F59E0B" if resultado and (inicio, fin) in resultado["corte"] else "#94A3B8"),
            width=3 if desactivada else 2,
            dash=(6, 4) if desactivada else (),
            arrow=tk.LAST,
            arrowshape=(10, 12, 5)
        )

        # Etiqueta de capacidad
        mx = (sx + ex) / 2 - uy * 12
        my = (sy + ey) / 2 + ux * 12

        canvas.create_text(
            mx, my,
            text=(f"{resultado['flujos'].get((inicio, fin), 0)}/{capacidad}" if resultado and not desactivada else str(capacidad)),
            fill="#F87171" if desactivada else "#FACC15",
            font=("Arial", 10, "bold")
        )

    # Dibujar centros encima de las rutas
    for nodo, (x, y) in coordenadas.items():
        if nodo == origen.get():
            color = "#10B981"
        elif nodo == destino.get():
            color = "#EF4444"
        else:
            color = "#3B82F6"

        canvas.create_oval(
            x-radio, y-radio,
            x+radio, y+radio,
            fill=color,
            outline="#FFFFFF",
            width=2
        )

        canvas.create_text(
            x, y,
            text=nodo,
            fill="white",
            font=("Arial", 11, "bold")
        )

# Actualizar al cambiar tamaño u origen/destino
canvas.bind("<Configure>", dibujar_red)
origen.bind("<<ComboboxSelected>>", invalidar_resultado)
destino.bind("<<ComboboxSelected>>", invalidar_resultado)

# Panel derecho
panel_derecho = tk.Frame(contenido, bg=PANEL)
panel_derecho.grid(row=0, column=2, sticky="nsew", padx=(10, 0))

tk.Label(
    panel_derecho,
    text="RESULTADOS",
    font=("Arial", 14, "bold"),
    bg=PANEL,
    fg=TEXTO
).pack(pady=20)

tk.Label(
    panel_derecho,
    text="Flujo máximo",
    bg=PANEL,
    fg=SECUNDARIO
).pack(pady=(15, 5))

valor_flujo = tk.Label(
    panel_derecho,
    text="—",
    font=("Arial", 32, "bold"),
    bg=PANEL,
    fg=AZUL
)
valor_flujo.pack()

tk.Label(
    panel_derecho,
    text="paquetes / hora",
    bg=PANEL,
    fg=SECUNDARIO
).pack()

tk.Label(
    panel_derecho,
    text="CORTE MÍNIMO",
    font=("Arial", 12, "bold"),
    bg=PANEL,
    fg=TEXTO
).pack(pady=(40, 15))

detalle_corte = tk.Label(
    panel_derecho,
    text="Conjunto S: pendiente\n\nConjunto T: pendiente",
    justify="left",
    bg=PANEL,
    fg=SECUNDARIO, wraplength=220
)
detalle_corte.pack(anchor="w", padx=20)

tk.Button(panel_derecho, text="Guardar escenario", command=guardar_escenario, bg=AZUL, fg=TEXTO).pack(fill="x", padx=15, pady=(20,5))
tk.Button(panel_derecho, text="Comparar escenarios", command=comparar_escenarios, bg="#475569", fg=TEXTO).pack(fill="x", padx=15, pady=5)
tk.Label(panel_derecho, text="Rojo discontinuo: ruta inactiva\nNaranja: corte mínimo\nEtiqueta: flujo/capacidad" if calcular_flujo_maximo else "Algoritmo pendiente de integración", bg=PANEL, fg=SECUNDARIO, wraplength=220).pack(padx=10,pady=10)

# Iniciar aplicación
ventana.mainloop()
