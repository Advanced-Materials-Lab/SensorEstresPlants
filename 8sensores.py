import tkinter as tk
from tkinter import ttk, simpledialog
import serial
import threading
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# --- Variables globales ---
numSensores = 8
max_puntos = 50
humedades = [[] for _ in range(numSensores)]
voltajes = [[] for _ in range(numSensores)]
leds = [0]*numSensores
tiempos = []
colores = ['red','blue','green','orange','purple','brown','cyan','magenta']
umbral = 10
pausado = False

# --- Función para pedir puerto COM ---
def pedir_com():
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    puerto_com = simpledialog.askstring("Puerto COM", "Ingrese el puerto COM (ejemplo COM3):")
    root.destroy()
    return puerto_com

puerto_com = pedir_com()
try:
    arduino = serial.Serial(puerto_com, 9600, timeout=1)
except Exception as e:
    print("Error al abrir el puerto COM:", e)
    exit()

# --- Archivo para guardar datos ---
archivo = open("datos_humedad.txt", "w")
archivo.write("Tiempo(s)\t" + "\t".join([f"HUM{i+1}\tV{i+1}" for i in range(numSensores)]) + "\n")

# --- Función para leer datos del Arduino ---
def leer_datos():
    global pausado
    while True:
        if not pausado:
            try:
                linea = arduino.readline().decode("utf-8").strip()
                if not linea or linea.startswith("Tiempo"):  # Ignorar encabezado
                    continue
                partes = linea.split("\t")
                if len(partes) >= 1 + numSensores*2:
                    tiempo = float(partes[0])
                    tiempos.append(tiempo)
                    fila_guardar = [str(tiempo)]
                    for i in range(numSensores):
                        h = float(partes[1 + i*2])
                        v = float(partes[2 + i*2])
                        humedades[i].append(h)
                        voltajes[i].append(v)
                        leds[i] = 1 if h < umbral else 0
                        fila_guardar.append(f"{h:.2f}")
                        fila_guardar.append(f"{v:.2f}")
                        if len(humedades[i]) > max_puntos:
                            humedades[i] = humedades[i][-max_puntos:]
                            voltajes[i] = voltajes[i][-max_puntos:]
                    if len(tiempos) > max_puntos:
                        tiempos[:] = tiempos[-max_puntos:]
                    if not archivo.closed:
                        archivo.write("\t".join(fila_guardar) + "\n")
                        archivo.flush()
            except Exception as e:
                print("Error:", e)

# --- Crear ventana principal ---
ventana = tk.Tk()
ventana.title("Monitoreo de Humedad y Voltaje")
ventana.geometry("1400x1000")

# --- Figura Matplotlib con 8 subplots ---
fig, axs = plt.subplots(4, 2, figsize=(14, 10))
axs = axs.flatten()
canvas = FigureCanvasTkAgg(fig, master=ventana)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

# --- Función para actualizar gráficas ---
def actualizar_graficas():
    for i, ax in enumerate(axs):
        ax.clear()
        ax.plot(tiempos, humedades[i], marker='o', color=colores[i], label=f"HUM {i+1}")
        ax.set_ylim(0, 200)
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Humedad (%)")
        ax.grid(True)
        ax.set_title(f"Sensor {i+1}", fontsize=10, fontweight='bold')

        # LED simulado grande junto al título
        led_color = "red" if leds[i] else "green"
        trans = ax.transAxes
        circle = Circle((1.1, 1.05), 0.05, transform=trans, color=led_color)
        ax.add_patch(circle)

        # Valores de humedad y voltaje arriba de la línea del último punto
        if humedades[i]:
            x_val = tiempos[-1] if tiempos else 0
            y_val = humedades[i][-1]
            ax.text(x_val, y_val + 5, f"H: {humedades[i][-1]:.1f}%\nV: {voltajes[i][-1]:.2f}V",
                    color=colores[i], fontsize=9, ha='center', va='bottom', fontweight='bold')

        ax.legend(loc="upper right", fontsize=8)

    canvas.draw()
    ventana.after(1000, actualizar_graficas)

# --- Funciones de los botones ---
def pausar():
    global pausado
    pausado = not pausado
    btn_pausa.config(text="Reanudar" if pausado else "Pausar")

def salir():
    archivo.close()
    ventana.destroy()

# --- Botones ---
frame_botones = tk.Frame(ventana)
frame_botones.pack(pady=5)
btn_pausa = ttk.Button(frame_botones, text="Pausar", command=pausar)
btn_pausa.pack(side=tk.LEFT, padx=10)
btn_salir = ttk.Button(frame_botones, text="Salir", command=salir)
btn_salir.pack(side=tk.LEFT, padx=10)

# --- Hilo para leer datos ---
hilo = threading.Thread(target=leer_datos, daemon=True)
hilo.start()

# --- Iniciar actualización de gráficas ---
ventana.after(1000, actualizar_graficas)
ventana.mainloop()
