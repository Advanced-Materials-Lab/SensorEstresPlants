import paho.mqtt.client as mqtt
import time
import random

BROKER = "192.168.137.104"
PORT = 1883
TOPIC = "sensores/datos"

client = mqtt.Client()
client.connect(BROKER, PORT, 60)

while True:
    temperatura = round(random.uniform(20, 30), 1)
    humedad = round(random.uniform(40, 60), 1)
    mensaje = f"Temperatura: {temperatura}°C, Humedad: {humedad}%"
    client.publish(TOPIC, mensaje)
    print(f"📤 Enviado: {mensaje}")
    time.sleep(2)