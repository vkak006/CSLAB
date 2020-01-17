import paho.mqtt.publish as publish
import paho.mqtt.client as paho
import time
import json
broker = "220.69.209.45"

def on_message(client, userdata, message):
	#print(str(message.payload.decode("utf-8")))
	topicName = str(message.topic)
	payload = str(message.payload.decode("utf-8"))
	
	#들어오는 메시지는 작은따옴표, 일단 파이썬처리를 위해 큰따옴표로 변겅
	payload = payload.replace("'", '"')
	dict = json.loads(payload)
	dict['topic'] = topicName

	#토픽을 페이로드에 추가했으니 다시 작은따옴표로 변경
	newPayload = json.dumps(dict)
	newPayload = newPayload.replace('"', "'")
	print(newPayload)

	#그럼 이제 다시 발행할 차례
	publish.single("withTopic/" + topicName, newPayload, hostname = "220.69.209.45", port = 1883, protocol = paho.MQTTv311)
client = paho.Client("bcmTest1")
client.on_message = on_message

client.connect(broker)
client.loop_start()

#sensors/# 구독
client.subscribe("sensors/+/+")

try:
	while True:
		time.sleep(1)
except:
	print("Exiting...")
	client.disconnect()
	client.loop_stop()
