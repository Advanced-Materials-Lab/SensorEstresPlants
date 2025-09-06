import paho.mqtt.client as mqtt

# Configuración
broker = "hivemq.client.1755895129346"
port = 8883
username = "eve_esp32"
password = "73Rb2!rI9AMeLC$,hai>"
topic = "eve/esp32/test"

# Funciones de callback
def on_connect(client, userdata, flags, rc):
    print(f"Conectado con código {rc}")
    client.subscribe(topic)

def on_message(client, userdata, msg):
    print(f"{msg.topic} → {msg.payload.decode()}")

# Cliente MQTT
client = mqtt.Client()
client.username_pw_set(username, password)
client.on_connect = on_connect
client.on_message = on_message

# Conexión segura
client.tls_set()
client.connect(broker, port, 60)

client.loop_forever()
