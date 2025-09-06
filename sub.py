import paho.mqtt.client as mqtt

BROKER = "10.40.21.37"  # 🔹 Cambia por la IP de tu PC broker
PUERTO = 1883
TOPICO = "test/prueba"

def on_connect(client, userdata, flags, rc, properties=None):
    print("✅ Conectado al broker con código:", rc)
    client.subscribe(TOPICO)
    print(f"📡 Suscrito al tópico: {TOPICO}")

def on_message(client, userdata, msg):
    print(f"📩 Mensaje recibido en {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)  # versión nueva
client.on_connect = on_connect
client.on_message = on_message

print("⏳ Conectando al broker...")
client.connect(BROKER, PUERTO, 60)
client.loop_forever()
