import paho.mqtt.client as mqtt
import time

broker = "broker.emqx.io"
port = 1883

# Cliente corregido para paho-mqtt v2.x
client = mqtt.Client(client_id="EvePython", protocol=mqtt.MQTTv311, callback_api_version=1)
client.connect(broker, port, 60)

while True:
    client.publish("sensor/temperatura", "24.6")
    client.publish("sensor/humedad", "56.2")
    client.publish("sensor/luz", "310")
    client.publish("sensor/ph", "6.8")
    print("📡 Datos enviados a los tópicos")
    time.sleep(5)
