import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    print("Conectado al broker con código:", rc)
    client.subscribe("sensor/plantas")  # Suscribirse al mismo topic

def on_message(client, userdata, msg):
    print(f"📩 Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.hivemq.com", 1883, 60)  # Dominio fijo

print("Esperando mensajes en tiempo real...")
client.loop_forever()
