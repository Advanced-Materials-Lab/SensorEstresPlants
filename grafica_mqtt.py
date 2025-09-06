import paho.mqtt.client as mqtt
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import datetime

BROKER = "192.168.137.104"  # IP de tu PC broker
PORT = 1883
TOPIC = "sensores/datos"

# Listas para almacenar datos
tiempos = []
temperaturas = []
humedades = []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        client.subscribe(TOPIC)
    else:
        print("❌ Error de conexión:", rc)

def on_message(client, userdata, msg):
    try:
        payload = msg.payload.decode()
        # Ejemplo: "ESP32 -> Temp: 28.80°C, Hum: 55.10%"
        temp_str = payload.split("Temp:")[1].split("°C")[0].strip()
        hum_str = payload.split("Hum:")[1].replace("%","").strip()

        tiempo_actual = datetime.datetime.now().strftime("%H:%M:%S")
        tiempos.append(tiempo_actual)
        temperaturas.append(float(temp_str))
        humedades.append(float(hum_str))

        # Mantener solo últimos 20 datos
        if len(tiempos) > 20:
            tiempos.pop(0)
            temperaturas.pop(0)
            humedades.pop(0)
    except:
        pass

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, PORT, 60)
client.loop_start()

# Función de animación
def animate(i):
    plt.cla()
    plt.plot(tiempos, temperaturas, label="Temp (°C)", color="red", marker="o")
    plt.plot(tiempos, humedades, label="Hum (%)", color="blue", marker="x")
    plt.xticks(rotation=45)
    plt.ylim(0, 100)
    plt.title("Datos sensores ESP32 en tiempo real")
    plt.xlabel("Hora")
    plt.ylabel("Valor")
    plt.legend()
    plt.tight_layout()

ani = FuncAnimation(plt.gcf(), animate, interval=2000)
plt.show()
