import customtkinter as ctk

# Configuración de apariencia
ctk.set_appearance_mode("Dark")  # Opciones: "System", "Dark", "Light"
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Simulador de Red - CustomTkinter")
app.geometry("520x400")

# Título principal
titulo = ctk.CTkLabel(app, text="Módulo de Cálculos: Simbología", font=("Arial", 16, "bold"))
titulo.pack(pady=15)

# Usando un cuadro de texto con símbolos Unicode para matemáticas (evitando problemas de LaTeX nativo)
formulas_texto = (
    "1. Restricción de Capacidad:\n"
    "    0 ≤ f(u, v) ≤ c(u, v)\n\n"
    "2. Conservación de Flujo:\n"
    "    ∑ f(u, z) = ∑ f(z, w)\n\n"
    "3. Flujo Máximo (Edmonds-Karp):\n"
    "    Val(f) = ∑ f(s, v)"
)

caja_formulas = ctk.CTkTextbox(app, width=440, height=200, font=("DejaVu Sans", 13))
caja_formulas.pack(pady=5)
caja_formulas.insert("0.0", formulas_texto)
caja_formulas.configure(state="disabled")  # Solo lectura

btn_ejecutar = ctk.CTkButton(app, text="Calcular Flujo de Red", fg_color="#1f6feb", hover_color="#1158c7")
btn_ejecutar.pack(pady=15)

app.mainloop()