import serial
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime

# Configura el puerto
puerto = input("Ingresa el puerto COM (ej: COM3): ")
ser = serial.Serial(puerto, 9600)

# Variables para datos
tiempos = []
voltajes = []

# Crear figura
fig, ax = plt.subplots()
linea, = ax.plot([], [], 'r-')
ax.set_xlim(0, 60)  # 60 muestras visibles
ax.set_ylim(0, 5)   # Voltaje de 0 a 5V
ax.set_xlabel("Tiempo (s)")
ax.set_ylabel("Voltaje (V)")

# Función de actualización
def update(frame):
    if ser.in_waiting > 0:
        dato = ser.readline().decode().strip()
        try:
            voltaje = float(dato)
            t = datetime.now().strftime("%H:%M:%S")
            tiempos.append(t)
            voltajes.append(voltaje)
            # Guardar en TXT
            with open("datos.txt", "a") as f:
                f.write(f"{t},{voltaje}\n")
            # Mantener solo últimas 60 muestras
            if len(tiempos) > 60:
                tiempos.pop(0)
                voltajes.pop(0)
            linea.set_data(range(len(voltajes)), voltajes)
        except:
            pass
    return linea,

ani = animation.FuncAnimation(fig, update, interval=500)
plt.show()
