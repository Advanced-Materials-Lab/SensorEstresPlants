import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from collections import deque
import matplotlib.animation as animation

# --- Configuración de datos ---
MAX_PUNTOS = 100  # Máximo número de puntos a mostrar
tiempo = deque(maxlen=MAX_PUNTOS)
voltaje = deque(maxlen=MAX_PUNTOS)

# --- Callback MQTT ---
def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        t, v, r = payload.split(',')  # Mensaje: tiempo,voltaje,resistencia
        tiempo.append(int(t))
        voltaje.append(float(v))
    except Exception as e:
        print("Error al procesar mensaje:", e)

# --- Configurar MQTT ---
client = mqtt.Client()
client.on_message = on_message
client.connect("192.168.137.104", 1883, 60)  # Cambia por la IP de tu broker
client.subscribe("sensor/voltaje")
client.loop_start()

# --- Crear figura ---
fig, ax = plt.subplots(figsize=(10,5))
line, = ax.plot([], [], 'b-', linewidth=2, marker='o', markersize=5, label='Voltaje (V)')
ax.set_xlabel("Tiempo (s)", fontsize=12)
ax.set_ylabel("Voltaje (V)", fontsize=12)
ax.set_title("Voltaje vs Tiempo en Tiempo Real", fontsize=14)
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()

# --- Función de animación ---
def animate(i):
    line.set_data(tiempo, voltaje)
    ax.relim()
    ax.autoscale_view()
    return line,

# --- Crear animación ---
ani = animation.FuncAnimation(fig, animate, interval=1000)  # Actualiza cada 1s
plt.tight_layout()
plt.show()

