import serial
import serial.tools.list_ports
import tkinter as tk
from tkinter import ttk
import threading
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.animation as animation

# Variables globales
arduino = None
datos = []
num_sensores = 8

# --- Selección de puerto ---
def listar_puertos():
    return [p.device for p in serial.tools.list_ports.comports()]

def conectar():
    global arduino
    puerto = combo_puertos.get()
    if puerto:
        try:
            arduino = serial.Serial(puerto, 9600, timeout=1)
            estado.set(f"Conectado a {puerto}")
            threading.Thread(target=leer_serial, daemon=True).start()
        except:
            estado.set("❌ Error al conectar")

# --- Lectura de datos ---
def leer_serial():
    global datos
    while True:
        if arduino and arduino.in_waiting > 0:
            try:
                linea = arduino.readline().decode(errors="ignore").strip()
                partes = linea.split("\t")

                # Ignorar líneas incompletas
                if len(partes) < (num_sensores*2 + 1):
                    continue

                # Validar que la primera columna sea un número
                try:
                    tiempo = float(partes[0])
                except ValueError:
                    continue  # <- si no es número, saltar

                voltajes = [float(partes[i*2+1]) for i in range(num_sensores)]
                humedades = [float(partes[i*2+2]) for i in range(num_sensores)]

                datos.append((tiempo, voltajes, humedades))

                # Actualizar LEDs + valores
                actualizar_cuadros(voltajes, humedades)

            except Exception as e:
                print("Error:", e)

# --- GUI LEDs + Valores ---
def actualizar_cuadros(voltajes, humedades):
    for i in range(num_sensores):
        humedad = humedades[i]
        voltaje = voltajes[i]

        intensidad = int((humedad/100)*255)
        color = f"#{intensidad:02x}{intensidad:02x}00"  # Verde-Amarillo
        canvas_leds[i].itemconfig(circulos[i], fill=color)

        etiquetas_voltaje[i].config(text=f"Voltaje: {voltaje:.2f} V")
        etiquetas_humedad[i].config(text=f"Humedad: {humedad:.1f} %")

# --- Gráficas individuales ---
def animar(i):
    if len(datos) > 0:
        tiempos = [d[0] for d in datos]

        for s in range(num_sensores):
            hums = [d[2][s] for d in datos]

            # --- asegurar que tiempos y hums tengan la misma longitud ---
            min_len = min(len(tiempos), len(hums))
            if min_len == 0:
                continue

            t_plot = tiempos[:min_len]
            h_plot = hums[:min_len]

            axs[s].clear()
            axs[s].plot(t_plot, h_plot, color=colores[s % len(colores)])

            # Mantener siempre mismo rango
            axs[s].set_ylim(0, 110)
            axs[s].set_xlim(left=max(0, t_plot[-1]-60), right=t_plot[-1]+1)
            axs[s].set_title(f"Sensor {s+1}", fontsize=8)
            axs[s].tick_params(axis='both', labelsize=6)

            # Si quieres más limpio, comenta esto:
            # axs[s].set_xticks([])
            # axs[s].set_yticks([])

            canvas_graficos[s].draw()

# --- Tkinter UI ---
root = tk.Tk()
root.title("Monitor de Sensores - Arduino")

frame = ttk.Frame(root, padding=10)
frame.pack()

ttk.Label(frame, text="Selecciona puerto Arduino:").grid(row=0, column=0, padx=5, pady=5)
combo_puertos = ttk.Combobox(frame, values=listar_puertos(), width=15)
combo_puertos.grid(row=0, column=1, padx=5, pady=5)

btn_conectar = ttk.Button(frame, text="Conectar", command=conectar)
btn_conectar.grid(row=0, column=2, padx=5, pady=5)

estado = tk.StringVar(value="No conectado")
ttk.Label(frame, textvariable=estado).grid(row=1, column=0, columnspan=3, pady=5)

# --- Cuadros con LED + Voltaje + Humedad + Mini gráfica ---
cuadros = []
canvas_leds = []
circulos = []
etiquetas_voltaje = []
etiquetas_humedad = []
figs = []
axs = []
canvas_graficos = []

frame_leds = ttk.Frame(root, padding=10)
frame_leds.pack()

# Colores distintos para cada sensor
colores = ["blue", "red", "green", "orange", "purple", "brown", "cyan", "magenta"]

for i in range(num_sensores):
    cuadro = ttk.Frame(frame_leds, borderwidth=2, relief="groove", padding=5)
    cuadro.grid(row=i//4, column=i%4, padx=10, pady=10)  # 4 columnas

    ttk.Label(cuadro, text=f"Sensor {i+1}", font=("Arial", 10, "bold")).pack()

    # LED
    canvas = tk.Canvas(cuadro, width=50, height=50, bg="white")
    canvas.pack(pady=3)
    c = canvas.create_oval(10, 10, 40, 40, fill="gray")

    # Valores
    lbl_v = ttk.Label(cuadro, text="Voltaje: 0.00 V")
    lbl_v.pack()
    lbl_h = ttk.Label(cuadro, text="Humedad: 0.0 %")
    lbl_h.pack()

    # Mini gráfica
    fig, ax = plt.subplots(figsize=(2,1.5))
    fig.subplots_adjust(left=0.25, right=0.95, bottom=0.25, top=0.8)
    grafico = FigureCanvasTkAgg(fig, master=cuadro)
    grafico.get_tk_widget().pack()

    # Guardar referencias
    cuadros.append(cuadro)
    canvas_leds.append(canvas)
    circulos.append(c)
    etiquetas_voltaje.append(lbl_v)
    etiquetas_humedad.append(lbl_h)
    figs.append(fig)
    axs.append(ax)
    canvas_graficos.append(grafico)

# --- Animación global para actualizar todas las gráficas ---
ani = animation.FuncAnimation(figs[0], animar, interval=1000, cache_frame_data=False)

root.mainloop()
