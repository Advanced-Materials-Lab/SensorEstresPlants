import paho.mqtt.client as mqtt

BROKER = "192.168.137.104"  # IP de tu PC broker
PORT = 1883
TOPIC = "sensores/datos"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker MQTT")
        client.subscribe(TOPIC)
    else:
        print("❌ Error de conexión:", rc)

def on_message(client, userdata, msg):
    print(f"📩 {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_forever()