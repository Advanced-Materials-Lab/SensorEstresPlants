import paho.mqtt.client as mqtt

BROKER = "localhost"  # prueba en tu propia PC
PUERTO = 1883
TOPICO = "test/prueba"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("✅ Conectado al broker MQTT local")
        client.publish(TOPICO, "Hola desde prueba MQTT")
        print(f"Mensaje enviado al tópico {TOPICO}")
    else:
        print("❌ Error al conectar, código:", rc)

client = mqtt.Client()
client.on_connect = on_connect

try:
    client.connect(BROKER, PUERTO, 60)
    client.loop_forever()
except Exception as e:
    print("❌ No se pudo conectar al broker:", e)
