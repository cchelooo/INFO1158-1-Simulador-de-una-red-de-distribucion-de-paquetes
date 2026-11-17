import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Crear ventana con un tema moderno de Bootstrap (ej. 'darkly' para modo oscuro o 'cosmo' para claro)
root = ttk.Window(title="Simulador de Red - Ttkbootstrap", themename="darkly", size=(520, 400))

# Título
titulo = ttk.Label(root, text="Panel de Control - Red de Distribución", font=("Helvetica", 14, "bold"), bootstyle="info")
titulo.pack(pady=15)

# Marco contenedor con estilo
frame_datos = ttk.Labelframe(root, text=" Modelos Matemáticos Activos ", padding=15, bootstyle="info")
frame_datos.pack(fill="both", expand=True, padx=20, pady=10)

# Etiquetas estilizadas con Bootstrap
lbl_capacidad = ttk.Label(frame_datos, text="• Restricción: 0 ≤ f(u, v) ≤ c(u, v)", font=("Courier", 11), bootstyle="light")
lbl_capacidad.pack(anchor="w", pady=5)

lbl_flujo = ttk.Label(frame_datos, text="• Algoritmo: Edmonds-Karp (O(V E²))", font=("Courier", 11), bootstyle="light")
lbl_flujo.pack(anchor="w", pady=5)

# Botón con estilo Bootstrap (success = verde)
btn_probar = ttk.Button(root, text="Ejecutar Simulación", bootstyle="success-outline", width=25)
btn_probar.pack(pady=15)

root.mainloop()