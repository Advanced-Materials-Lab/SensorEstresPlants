import paho.mqtt.client as mqtt
import time

BROKER = "10.40.21.37"  # 🔹 Cambia por la IP de tu PC broker
PUERTO = 1883
TOPICO = "test/prueba"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

print("⏳ Conectando al broker...")
client.connect(BROKER, PUERTO, 60)

for i in range(5):
    mensaje = f"Hola MQTT #{i+1}"
    client.publish(TOPICO, mensaje)
    print(f"📤 Enviado: {mensaje}")
    time.sleep(2)

client.disconnect()