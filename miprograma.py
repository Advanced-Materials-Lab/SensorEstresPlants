import tkinter as tk
from tkinter import messagebox

# Función para guardar en archivo
def guardar_nombre():
    nombre = entrada.get().strip()
    if nombre:
        with open("datos.txt", "a", encoding="utf-8") as f:
            f.write(nombre + "\n")
        messagebox.showinfo("Guardado", f"El nombre '{nombre}' se guardó en datos.txt")
        entrada.delete(0, tk.END)  # limpia la caja de texto
    else:
        messagebox.showwarning("Error", "Por favor, ingresa un nombre.")

# Crear ventana
ventana = tk.Tk()
ventana.title("Programa con Botones")
ventana.geometry("300x200")

# Etiqueta
etiqueta = tk.Label(ventana, text="Ingresa tu nombre:", font=("Arial", 12))
etiqueta.pack(pady=10)

# Caja de texto
entrada = tk.Entry(ventana, font=("Arial", 12))
entrada.pack(pady=5)

# Botón para guardar
btn_guardar = tk.Button(ventana, text="Guardar", command=guardar_nombre, bg="lightgreen")
btn_guardar.pack(pady=5)

# Botón para salir
btn_salir = tk.Button(ventana, text="Salir", command=ventana.quit, bg="lightcoral")
btn_salir.pack(pady=5)

# Iniciar ventana
ventana.mainloop()
