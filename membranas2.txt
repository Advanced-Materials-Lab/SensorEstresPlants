import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import simpledialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import threading
import time

# ---------- Configuración inicial ----------
# Preguntar COM al usuario
root = tk.Tk()
root.withdraw()
puerto = simpledialog.askstring("Puerto COM", "Ingresa el número de puerto COM (ej: COM3):")

if puerto is None:
    messagebox.showinfo("Cancelado", "No se seleccionó puerto. Saliendo...")
    exit()

try:
    ser = serial.Serial(puerto, 9600, timeout=1)
except:
    messagebox.showerror("Error", f"No se pudo abrir el puerto {puerto}")
    exit()

# Variables para graficar
tiempos = []
datos = [[] for _ in range(8)]  # 8 sensores

# Umbral igual que en Arduino
umbral = 10

# ---------- Interfaz gráfica ----------
ventana = tk.Tk()
ventana.title("Adquisición de Humedad en Tiempo Real")

# Canvas para LEDs virtuales
canvas = tk.Canvas(ventana, width=400, height=200, bg="white")
canvas.pack()

# Crear círculos (LEDs)
leds = []
for i in range(8):
    x = 40 + (i % 4) * 90
    y = 60 + (i // 4) * 90
    led = canvas.create_oval(x, y, x+50, y+50, fill="grey")
    leds.append(led)

# ---------- Funciones ----------
def actualizar_leds(valores):
    """Encender/apagar LEDs según valores recibidos"""
    for i, valor in enumerate(valores):
        if valor < umbral:
            canvas.itemconfig(leds[i], fill="green")
        else:
            canvas.itemconfig(leds[i], fill="red")

def leer_datos():
    """Leer datos desde Arduino"""
    while True:
        try:
            linea = ser.readline().decode("utf-8").strip()
            if linea.startswith("H1:"):
                partes = linea.replace("H1:", "").replace("H2:", "").replace("H3:", "").replace("H4:", "").replace("H5:", "").replace("H6:", "").replace("H7:", "").replace("H8:", "").replace("|", "").split()
                valores = list(map(int, partes))
                if len(valores) == 8:
                    tiempos.append(time.time() - inicio)
                    for i in range(8):
                        datos[i].append(valores[i])
                    actualizar_leds(valores)
        except:
            pass

def actualizar_grafica(i):
    """Graficar en tiempo real"""
    plt.cla()
    for i in range(8):
        plt.plot(tiempos, datos[i], label=f"HUM{i+1}")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Valor ADC")
    plt.legend(loc="upper right")
    plt.title("Sensores de Humedad en Tiempo Real")

# ---------- Iniciar adquisición ----------
inicio = time.time()
hilo = threading.Thread(target=leer_datos, daemon=True)
hilo.start()

# Configuración matplotlib
fig = plt.figure()
ani = FuncAnimation(fig, actualizar_grafica, interval=1000)

# Ejecutar GUI + Gráfica
threading.Thread(target=plt.show, daemon=True).start()
ventana.mainloop()
