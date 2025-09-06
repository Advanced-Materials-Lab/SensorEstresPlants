import paho.mqtt.client as mqtt

BROKER = "10.40.21.37"   # cámbialo por tu IP local si pruebas desde otro PC
PORT = 1883

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado correctamente al broker MQTT")
        client.disconnect()
    else:
        print(f"❌ Error de conexión. Código: {rc}")

client = mqtt.Client()
client.on_connect = on_connect

print("⏳ Intentando conectar al broker...")
client.connect(BROKER, PORT, 60)
client.loop_forever()