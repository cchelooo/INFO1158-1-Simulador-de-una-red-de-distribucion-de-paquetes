# Para seguir con el Tkinter

En `santana` quedo el dibujo actualizado de Martin con los calculos y la comparacion de escenarios conectados. Abre `interfaz.py` con `python3 -B interfaz.py`. Si tu Python no trae Tkinter, prueba con uno que si lo tenga. `python3 -m tkinter` sirve para comprobarlo.

## Si vas a seguir en la rama Martin

Puedes llevarte `interfaz.py`, `red.py` y `flujo.py` de `santana`. Si ya avanzaste en tu ventana, asi quedaron conectadas las partes:

1. Crea la red con `Red(CENTROS_INICIALES, RUTAS_INICIALES)` al abrir la ventana. Usa `red.rutas()` para dibujar todas las rutas y `red.rutas_activas()` para saber cuales siguen abiertas.
2. Pon una funcion en el boton Calcular que llame a `calcular_flujo_y_corte(red, origen.get(), destino.get())`. Devuelve el total, el flujo por ruta y el corte. Muestra `S`, `T`, los arcos de `corte["arcos"]` y `corte["capacidad"]`. En cada ruta muestra flujo y capacidad.
3. Conecta los botones de edicion a `red.agregar_ruta`, `red.modificar_capacidad` y `red.desactivar_ruta`. Si vuelves a abrir una ruta apagada, primero guarda la capacidad elegida y despues usa `red.reactivar_ruta`. Si un cambio da `ValueError`, muestra el mensaje en una ventanita.
4. Borra el resultado anterior al editar la red o cambiar el origen o destino. El boton Calcular vuelve a llenar todo. Para restablecer, crea otra `Red` con los datos iniciales.
5. Despues de calcular, guarda el total, la capacidad del corte y los cambios. Asi puedes comparar las redes aunque despues restablezcas la red. Los escenarios quedan guardados hasta que cierres el simulador.

La copia de `santana` ya hace esos pasos. Si la llevas tal cual, queda probarla en el equipo que usaremos en la presentacion. En la rama vieja puedes sacar `import tkinterplus`, la ventana usa solo Tkinter.

## Prueba rapida para la demo

Pulsa **Guardar escenario** despues de cada calculo. Al final puedes volver a la tabla con **Comparar escenarios**.

- Con `A` y `J` deberia dar **14**. El corte pasa por `A -> B` y `A -> C`.
- Apaga `A -> B` y vuelve a calcular. Deberia dar **6** y la ruta apagada se ve punteada.
- Restablece la red, sube `A -> C` a 12 y calcula. Deberia dar **16**.
- Para probar el boton de agregar, restablece otra vez y agrega `A -> J` con capacidad 4. Deberia dar **18**.

La comparacion de las tres redes y el caso de cinco centros estan en `Readme.md`. Para la entrega queda pasar eso al informe PDF, poner el enlace al codigo que vamos a entregar y ensayar la demo entre los tres.
