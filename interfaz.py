import math
import tkinter as tk
from tkinter import font, messagebox, ttk

from flujo import calcular_flujo_y_corte
from red import CENTROS_INICIALES, RUTAS_INICIALES, Red


FONDO = "#101827"
PANEL = "#1E293B"
TEXTO = "#FFFFFF"
SECUNDARIO = "#A8B3C7"
COLOR_CORTE = "#F59E0B"
COLOR_INACTIVA = "#F87171"

# Posiciones del dibujo actualizado de Martin
POSICIONES = {
    "A": (0.08, 0.50), "B": (0.28, 0.25), "C": (0.28, 0.75),
    "D": (0.47, 0.15), "E": (0.47, 0.32), "F": (0.47, 0.85),
    "G": (0.67, 0.46), "H": (0.82, 0.12), "I": (0.67, 0.75),
    "J": (0.92, 0.55),
}


class Interfaz:
    def __init__(self, ventana):
        self.ventana = ventana
        self.red = Red(CENTROS_INICIALES, RUTAS_INICIALES)
        self.red.validar_configuracion_inicial("A", "J")
        self.flujos = None
        self.corte = None
        self.escenarios = []
        self.comparacion = None

        ventana.title("Simulador de distribución de paquetes")
        ventana.geometry("1200x700")
        ventana.minsize(1000, 560)
        ventana.configure(bg=FONDO)
        tk.Label(
            ventana, text="Simulador de distribución de paquetes",
            bg=FONDO, fg=TEXTO, font=("Arial", 20, "bold"),
        ).pack(anchor="w", padx=20, pady=16)

        contenido = tk.Frame(ventana, bg=FONDO)
        contenido.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        contenido.grid_columnconfigure(1, weight=1)
        contenido.grid_rowconfigure(0, weight=1)

        controles = tk.Frame(contenido, bg=PANEL, padx=14, pady=14)
        controles.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.origen = self._selector(controles, "Centro de origen", self.red.centros)
        self.destino = self._selector(controles, "Centro de destino", self.red.centros)
        self.origen.set("A")
        self.destino.set("J")

        ttk.Button(
            controles, text="Calcular flujo máximo", command=self.calcular,
        ).pack(fill="x", pady=(6, 18))
        for texto, accion in (
            ("Agregar conexión", self.agregar_conexion),
            ("Modificar capacidad", self.modificar_capacidad),
            ("Desactivar ruta", self.desactivar_ruta),
            ("Restablecer red", self.restablecer_red),
        ):
            ttk.Button(controles, text=texto, command=accion).pack(fill="x", pady=3)

        dibujo = tk.Frame(contenido, bg=PANEL, padx=12, pady=12)
        dibujo.grid(row=0, column=1, sticky="nsew")
        self.lienzo = tk.Canvas(dibujo, bg="#172033", highlightthickness=0, width=1)
        self.lienzo.pack(fill="both", expand=True)
        tk.Label(
            dibujo, text="Verde: origen   |   Rojo: destino   |   Naranja: corte\n"
            "Línea punteada: ruta inactiva",
            bg=PANEL, fg=SECUNDARIO, font=("Arial", 11),
        ).pack(pady=(8, 0))

        resultados = tk.Frame(contenido, bg=PANEL, padx=14, pady=14)
        resultados.grid(row=0, column=2, sticky="nsew", padx=(10, 0))
        self.valor = tk.StringVar(ventana)
        self.texto_corte = tk.StringVar(ventana)
        tk.Label(
            resultados, text="Flujo máximo (paq/h)", bg=PANEL, fg=SECUNDARIO,
        ).pack(anchor="w")
        tk.Label(
            resultados, textvariable=self.valor, bg=PANEL, fg=TEXTO,
            font=("Arial", 32, "bold"),
        ).pack(anchor="w")
        tk.Label(
            resultados, textvariable=self.texto_corte, bg=PANEL, fg=TEXTO,
            justify="left", wraplength=235,
        ).pack(anchor="w", pady=(0, 12))
        ttk.Button(
            resultados, text="Guardar escenario", command=self.guardar_escenario,
        ).pack(fill="x", pady=(0, 4))
        ttk.Button(
            resultados, text="Comparar escenarios", command=self.comparar_escenarios,
        ).pack(fill="x", pady=(0, 10))

        marco_tabla = tk.Frame(resultados, bg=PANEL)
        marco_tabla.pack(fill="both", expand=True)
        columnas = ("ruta", "flujo", "capacidad")
        self.tabla = ttk.Treeview(
            marco_tabla, columns=columnas, show="headings", height=7,
        )
        for columna, titulo, ancho in (
            ("ruta", "Ruta", 88), ("flujo", "Flujo", 55), ("capacidad", "Cap.", 62),
        ):
            self.tabla.heading(columna, text=titulo)
            self.tabla.column(columna, width=ancho, anchor="center", stretch=False)
        self.tabla.tag_configure("inactiva", foreground="#B91C1C")
        barra = ttk.Scrollbar(marco_tabla, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=barra.set)
        barra.pack(side="right", fill="y")
        self.tabla.pack(side="left", fill="both", expand=True)

        self.lienzo.bind("<Configure>", self.dibujar_red)
        self.origen.bind("<<ComboboxSelected>>", self.limpiar_resultado)
        self.destino.bind("<<ComboboxSelected>>", self.limpiar_resultado)
        self.limpiar_resultado()

    def _selector(self, contenedor, titulo, opciones):
        tk.Label(contenedor, text=titulo, bg=PANEL, fg=TEXTO).pack(anchor="w")
        selector = ttk.Combobox(contenedor, values=opciones, state="readonly")
        selector.pack(fill="x", pady=(4, 10))
        return selector

    def _dialogo(self, titulo):
        dialogo = tk.Toplevel(self.ventana)
        dialogo.title(titulo)
        dialogo.configure(bg=PANEL, padx=14, pady=14)
        dialogo.transient(self.ventana)
        dialogo.resizable(False, False)
        return dialogo

    def _boton_dialogo(self, dialogo, texto, accion):
        ttk.Button(dialogo, text=texto, command=accion).pack(fill="x", pady=(6, 0))
        dialogo.grab_set()

    def agregar_conexion(self):
        dialogo = self._dialogo("Agregar conexión")
        origen = self._selector(dialogo, "Origen", self.red.centros)
        destino = self._selector(dialogo, "Destino", self.red.centros)
        capacidad = self._selector(dialogo, "Capacidad (1 a 12)", tuple(range(1, 13)))

        def guardar():
            inicio, fin = origen.get(), destino.get()
            if not inicio or not fin or not capacidad.get():
                messagebox.showwarning("Faltan datos", "Completa los tres campos", parent=dialogo)
                return

            arco = (inicio, fin)
            try:
                nueva_capacidad = int(capacidad.get())
                if arco in self.red.rutas() and arco not in self.red.rutas_activas():
                    confirmar = messagebox.askyesno(
                        "Ruta inactiva",
                        f"¿Reactivar {inicio} → {fin} con capacidad {nueva_capacidad}?",
                        parent=dialogo,
                    )
                    if not confirmar:
                        return
                    self.red.modificar_capacidad(inicio, fin, nueva_capacidad)
                    self.red.reactivar_ruta(inicio, fin)
                else:
                    self.red.agregar_ruta(inicio, fin, nueva_capacidad)
            except ValueError as error:
                messagebox.showerror("Ruta inválida", str(error), parent=dialogo)
                return
            dialogo.destroy()
            self.limpiar_resultado()

        self._boton_dialogo(dialogo, "Guardar conexión", guardar)

    def modificar_capacidad(self):
        dialogo = self._dialogo("Modificar capacidad")
        rutas = self.red.rutas()
        arcos = list(rutas)
        opciones = [f"{a} → {b} ({rutas[a, b]})" for a, b in arcos]
        ruta = self._selector(dialogo, "Ruta", opciones)
        capacidad = self._selector(dialogo, "Capacidad (1 a 12)", tuple(range(1, 13)))

        def guardar():
            indice = ruta.current()
            if indice == -1 or not capacidad.get():
                messagebox.showwarning("Faltan datos", "Elige una ruta y su capacidad", parent=dialogo)
                return
            inicio, fin = arcos[indice]
            self.red.modificar_capacidad(inicio, fin, int(capacidad.get()))
            dialogo.destroy()
            self.limpiar_resultado()

        self._boton_dialogo(dialogo, "Guardar cambios", guardar)

    def desactivar_ruta(self):
        activas = self.red.rutas_activas()
        if not activas:
            messagebox.showinfo("Rutas", "Ya no quedan rutas activas", parent=self.ventana)
            return

        dialogo = self._dialogo("Desactivar ruta")
        arcos = list(activas)
        opciones = [f"{inicio} → {fin} ({activas[inicio, fin]})" for inicio, fin in arcos]
        ruta = self._selector(dialogo, "Ruta", opciones)

        def guardar():
            indice = ruta.current()
            if indice == -1:
                messagebox.showwarning("Faltan datos", "Elige una ruta", parent=dialogo)
                return
            inicio, fin = arcos[indice]
            confirmar = messagebox.askyesno(
                "Desactivar ruta", f"¿Desactivar {inicio} → {fin}?", parent=dialogo,
            )
            if not confirmar:
                return
            self.red.desactivar_ruta(inicio, fin)
            dialogo.destroy()
            self.limpiar_resultado()

        self._boton_dialogo(dialogo, "Desactivar ruta", guardar)

    def restablecer_red(self):
        confirmar = messagebox.askyesno(
            "Restablecer red", "¿Volver a la red inicial y borrar los cambios?",
            parent=self.ventana,
        )
        if confirmar:
            self.red = Red(CENTROS_INICIALES, RUTAS_INICIALES)
            self.limpiar_resultado()

    def calcular(self):
        try:
            valor, self.flujos, self.corte = calcular_flujo_y_corte(
                self.red, self.origen.get(), self.destino.get(),
            )
        except ValueError as error:
            self.limpiar_resultado()
            messagebox.showerror("Revisa el origen y el destino", str(error), parent=self.ventana)
            return

        self.valor.set(str(valor))
        lado_origen = ", ".join(centro for centro in self.red.centros if centro in self.corte["S"])
        lado_destino = ", ".join(centro for centro in self.red.centros if centro in self.corte["T"])
        arcos = ", ".join(f"{a} → {b}" for a, b in self.corte["arcos"])
        self.texto_corte.set(
            f"Corte mínimo: {self.corte['capacidad']} paq/h\n"
            f"S = {{{lado_origen}}}\nT = {{{lado_destino}}}\n"
            f"Arcos del corte: {arcos or 'ninguno'}"
        )
        self.dibujar_red()
        self.actualizar_tabla()

    def guardar_escenario(self):
        if self.corte is None:
            messagebox.showinfo(
                "Escenarios", "Calcula el flujo antes de guardar", parent=self.ventana,
            )
            return

        # Guarda como estaba la red al calcular para poder cambiarla despues
        iniciales = {(inicio, fin): capacidad for inicio, fin, capacidad in RUTAS_INICIALES}
        activas = self.red.rutas_activas()
        cambios = []
        for arco, capacidad in self.red.rutas().items():
            anterior = iniciales.get(arco)
            detalle = []
            if anterior is None:
                detalle.append(f"nueva ({capacidad})")
            elif capacidad != anterior:
                detalle.append(f"{anterior} → {capacidad}")
            if arco not in activas:
                detalle.append("inactiva")
            if detalle:
                inicio, fin = arco
                cambios.append(f"{inicio} → {fin}: " + ", ".join(detalle))

        self.escenarios.append((
            f"{self.origen.get()} → {self.destino.get()}", self.valor.get(),
            self.corte["capacidad"], len(activas), " | ".join(cambios) or "Red inicial",
        ))
        self.comparar_escenarios()

    def comparar_escenarios(self):
        if not self.escenarios:
            messagebox.showinfo(
                "Escenarios", "Guarda un escenario para compararlo", parent=self.ventana,
            )
            return

        if self.comparacion is None or not self.comparacion.winfo_exists():
            ventana = tk.Toplevel(self.ventana)
            ventana.title("Comparación de escenarios")
            ventana.geometry("660x260")
            ventana.transient(self.ventana)
            ventana.grid_columnconfigure(0, weight=1)
            ventana.grid_rowconfigure(0, weight=1)

            columnas = ("par", "flujo", "corte", "activas", "cambios")
            tabla = ttk.Treeview(ventana, columns=columnas, show="headings")
            for columna, titulo, ancho in (
                ("par", "Origen y destino", 98), ("flujo", "Flujo máx.", 76),
                ("corte", "Corte mín.", 76), ("activas", "Rutas activas", 88),
                ("cambios", "Cambios", 120),
            ):
                tabla.heading(columna, text=titulo)
                anclaje = "w" if columna == "cambios" else "center"
                tabla.column(columna, width=ancho, anchor=anclaje, stretch=columna == "cambios")
            vertical = ttk.Scrollbar(ventana, orient="vertical", command=tabla.yview)
            horizontal = ttk.Scrollbar(ventana, orient="horizontal", command=tabla.xview)
            tabla.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
            tabla.grid(row=0, column=0, sticky="nsew")
            vertical.grid(row=0, column=1, sticky="ns")
            horizontal.grid(row=1, column=0, sticky="ew")
            self.comparacion = ventana
            self.tabla_escenarios = tabla

        tabla = self.tabla_escenarios
        tabla.delete(*tabla.get_children())
        letra = font.nametofont("TkDefaultFont", root=self.comparacion)
        ancho_cambios = max(letra.measure(escenario[-1]) for escenario in self.escenarios)
        tabla.column("cambios", minwidth=max(120, ancho_cambios + 20))
        for escenario in self.escenarios:
            fila = tabla.insert("", "end", values=escenario)
        tabla.see(fila)
        self.comparacion.lift()

    def limpiar_resultado(self, evento=None):
        # Si cambia la red hay que calcular de nuevo
        self.flujos = None
        self.corte = None
        self.valor.set("-")
        self.texto_corte.set("Pulsa Calcular para ver el corte")
        self.dibujar_red()
        self.actualizar_tabla()

    def actualizar_tabla(self):
        self.tabla.delete(*self.tabla.get_children())
        activas = self.red.rutas_activas()
        for (inicio, fin), capacidad in self.red.rutas().items():
            arco = (inicio, fin)
            flujo = "-" if self.flujos is None else self.flujos.get(arco, 0)
            etiquetas = () if arco in activas else ("inactiva",)
            self.tabla.insert(
                "", "end", values=(f"{inicio} → {fin}", flujo, capacidad), tags=etiquetas,
            )

    def dibujar_red(self, evento=None):
        lienzo = self.lienzo
        lienzo.delete("all")
        ancho, alto = lienzo.winfo_width(), lienzo.winfo_height()
        if ancho < 100 or alto < 100:
            return

        radio = 18
        coordenadas = {centro: (x * ancho, y * alto) for centro, (x, y) in POSICIONES.items()}
        activas = self.red.rutas_activas()
        arcos_corte = self.corte["arcos"] if self.corte else {}
        rotulos = []
        for (inicio, fin), capacidad in self.red.rutas().items():
            arco = (inicio, fin)
            inactiva = arco not in activas
            color = "#94A3B8"
            if inactiva:
                color = COLOR_INACTIVA
            elif arco in arcos_corte:
                color = COLOR_CORTE

            x1, y1 = coordenadas[inicio]
            x2, y2 = coordenadas[fin]
            distancia = math.hypot(x2 - x1, y2 - y1)
            paso_x = (x2 - x1) / distancia
            paso_y = (y2 - y1) / distancia
            lienzo.create_line(
                x1 + paso_x * radio, y1 + paso_y * radio,
                x2 - paso_x * radio, y2 - paso_y * radio,
                fill=color, width=3 if arco in arcos_corte else 2,
                dash=(6, 4) if inactiva else (), arrow=tk.LAST,
            )
            texto = str(capacidad)
            if self.flujos is not None:
                texto = f"{self.flujos.get(arco, 0)}/{capacidad}"
            centro_x = (x1 + x2) / 2 + paso_y * 12
            centro_y = (y1 + y2) / 2 - paso_x * 12
            rotulos.append((centro_x, centro_y, texto, color))

        # Los numeros van encima de las flechas
        for x, y, texto, color in rotulos:
            lienzo.create_text(x, y, text=texto, fill=color, font=("Arial", 11, "bold"))

        for centro, (x, y) in coordenadas.items():
            color = "#3B82F6"
            if centro == self.origen.get():
                color = "#10B981"
            elif centro == self.destino.get():
                color = "#EF4444"
            lienzo.create_oval(
                x - radio, y - radio, x + radio, y + radio, fill=color, outline=TEXTO,
            )
            lienzo.create_text(x, y, text=centro, fill=TEXTO, font=("Arial", 11, "bold"))


if __name__ == "__main__":
    ventana = tk.Tk()
    Interfaz(ventana)
    ventana.mainloop()
