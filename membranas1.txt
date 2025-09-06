import tkinter as tk
from tkinter import messagebox
import serial
import threading
import time

# Variables globales
ser = None
lectura_activa = False

def iniciar_lectura():
    global ser, lectura_activa

    puerto = entry_com.get()
    if not puerto.isdigit():
        messagebox.showerror("Error", "El puerto COM debe ser un número. Ejemplo: 3 para COM3")
        return

    try:
        ser = serial.Serial(f"COM{puerto}", 9600, timeout=1)
        lectura_activa = True
        messagebox.showinfo("Conectado", f"Conectado a COM{puerto}")
        threading.Thread(target=leer_datos, daemon=True).start()
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo abrir COM{puerto}\n{e}")

def detener_lectura():
    global lectura_activa, ser
    lectura_activa = False
    if ser:
        ser.close()
    messagebox.showinfo("Desconectado", "Lectura detenida y puerto cerrado.")

def leer_datos():
    global ser, lectura_activa
    with open("datos_guardados.txt", "a") as archivo:  # Guarda datos en txt
        while lectura_activa:
            try:
                if ser.in_waiting > 0:
                    linea = ser.readline().decode("utf-8").strip()
                    if linea:
                        archivo.write(linea + "\n")
                        archivo.flush()
                        text_salida.insert(tk.END, linea + "\n")
                        text_salida.see(tk.END)
            except Exception as e:
                text_salida.insert(tk.END, f"Error: {e}\n")
                break
            time.sleep(0.1)

# ------------------ Interfaz Tkinter ------------------
root = tk.Tk()
root.title("Adquisición de Datos - Arduino Mega")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack()

label = tk.Label(frame, text="Número de Puerto COM:")
label.grid(row=0, column=0, sticky="w")

entry_com = tk.Entry(frame)
entry_com.grid(row=0, column=1)

btn_iniciar = tk.Button(frame, text="Conectar", command=iniciar_lectura, bg="lightgreen")
btn_iniciar.grid(row=1, column=0, pady=5)

btn_detener = tk.Button(frame, text="Detener", command=detener_lectura, bg="tomato")
btn_detener.grid(row=1, column=1, pady=5)

text_salida = tk.Text(root, height=15, width=60)
text_salida.pack(padx=10, pady=10)

root.mainloop()
