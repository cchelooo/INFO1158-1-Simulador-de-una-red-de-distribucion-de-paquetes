import tkinter as tk
from tkinter import ttk, messagebox
import tkinterplus

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

    centros = list(posiciones.keys())

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

        
        for u, v, _ in rutas:
            if u == inicio and v == fin:

                # Comprobar si la conexión está desactivada
                if (inicio, fin) in rutas_desactivadas:
                    reactivar = messagebox.askyesno(
                        "Ruta desactivada",
                        f"La ruta {inicio} → {fin} ya existe, "
                        "pero está desactivada.\n\n"
                        "¿Deseas reactivarla?",
                        parent=ventana_agregar
                    )

                    if reactivar:
                        rutas_desactivadas.remove((inicio, fin))
                        dibujar_red()
                        ventana_agregar.destroy()

                        messagebox.showinfo(
                            "Ruta reactivada",
                            f"La ruta {inicio} → {fin} "
                            "fue reactivada correctamente.",
                            parent=ventana
                        )

                    return

                # La ruta existe y está activa
                messagebox.showerror(
                    "Ruta duplicada",
                    "Esta conexión ya existe y está activa.",
                    parent=ventana_agregar
                )
                return

            if u == fin and v == inicio:
                messagebox.showerror(
                    "Conexión recíproca",
                    "No se permiten conexiones en ambos sentidos.",
                    parent=ventana_agregar
                )
                return


            if (u == fin and v == inicio):
                messagebox.showerror(
                    "Conexión recíproca",
                    "No se permiten conexiones en ambos sentidos.",
                    parent=ventana_agregar
                )
                return

        rutas.append((inicio, fin, int(capacidad)))

        dibujar_red()
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
    opciones = [
        f"{inicio} → {fin} (Capacidad: {capacidad})"
        for inicio, fin, capacidad in rutas
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

        inicio, fin, anterior = rutas[indice]
        nueva = int(capacidad)

        rutas[indice] = (inicio, fin, nueva)

        dibujar_red()
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
        for inicio, fin, capacidad in rutas
        if (inicio, fin) not in rutas_desactivadas
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

        rutas_desactivadas.add((inicio, fin))
        dibujar_red()
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

    tk.Button(
        panel_izquierdo,
        text="Restablecer red",
        command=restablecer_red,
        bg="#475569",
        fg="white",
        relief="flat",
        font=("Arial", 10, "bold")
    ).pack(fill="x", padx=15, pady=(20, 5))

def restablecer_red():
    confirmar = messagebox.askyesno(
        "Restablecer red",
        "¿Deseas restaurar la red original?\n\n"
        "Se perderán las conexiones agregadas, "
        "los cambios de capacidad y las desactivaciones.",
        parent=ventana
    )

    if not confirmar:
        return

    # Recuperar las conexiones y capacidades originales
    rutas.clear()
    rutas.extend(rutas_originales)

    # Reactivar todas las rutas
    rutas_desactivadas.clear()

    # Actualizar la representación gráfica
    dibujar_red()

    messagebox.showinfo(
        "Red restablecida",
        "La red original se restauró correctamente.",
        parent=ventana
    )

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
    values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
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
    values=["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"],
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
    state="disabled"
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


import math

# Red de demostración: 10 centros y 16 rutas.
# Formato: (origen, destino, capacidad)
rutas = [
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
    ("E", "I", 2)
]

# Guardar una copia de la configuración inicial
rutas_originales = rutas.copy()

# Conjunto de rutas temporalmente desactivadas
rutas_desactivadas = set()

# Posiciones proporcionales dentro del Canvas
posiciones = {
    "A": (0.08, 0.50),
    "B": (0.28, 0.25),
    "C": (0.28, 0.75),
    "D": (0.47, 0.15),
    "E": (0.47, 0.40),
    "F": (0.47, 0.85),
    "G": (0.67, 0.30),
    "H": (0.84, 0.20),
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
    for inicio, fin, capacidad in rutas:
        desactivada = (inicio, fin) in rutas_desactivadas
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
            fill="#F87171" if desactivada else "#94A3B8",
            width=3 if desactivada else 2,
            dash=(6, 4) if desactivada else (),
            arrow=tk.LAST,
            arrowshape=(10, 12, 5)
        )

        # Etiqueta de capacidad
        mx = (sx + ex) / 2
        my = (sy + ey) / 2

        canvas.create_text(
            mx, my - 9,
            text=str(capacidad),
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
origen.bind("<<ComboboxSelected>>", dibujar_red)
destino.bind("<<ComboboxSelected>>", dibujar_red)

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

tk.Label(
    panel_derecho,
    text="—",
    font=("Arial", 32, "bold"),
    bg=PANEL,
    fg=AZUL
).pack()

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

tk.Label(
    panel_derecho,
    text="Conjunto S: pendiente\n\nConjunto T: pendiente",
    justify="left",
    bg=PANEL,
    fg=SECUNDARIO
).pack(anchor="w", padx=20)

# Iniciar aplicación
ventana.mainloop()
