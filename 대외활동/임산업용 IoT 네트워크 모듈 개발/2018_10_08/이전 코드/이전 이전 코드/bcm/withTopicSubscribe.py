import paho.mqtt.client as paho
import time
import json
broker = "220.69.209.45"

def on_message(client, userdata, message):
	print(str(message.payload.decode("utf-8")))
client = paho.Client("bcmTest2")
client.on_message = on_message

client.connect(broker)
client.loop_start()

client.subscribe("sensor/+/+/+")

try:
	while True:
		time.sleep(1)
except:
	print("Exiting...")
	client.disconnect()
	client.loop_stop()
