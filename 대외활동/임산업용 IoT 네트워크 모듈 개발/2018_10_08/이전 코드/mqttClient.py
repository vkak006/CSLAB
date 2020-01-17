import paho.mqtt.client as mqtt
import time

def on_connect(client, obj, flags, rc):
    print("Connected!")
    client.subscribe("00-00-00-00-00/#")

def on_message(client, obj, msg):
    print("Topic : ", msg.topic + "\nPayload : " + str(msg.payload))
    #여기서 1차 판별. 어떤 디바이스가 있는지 확인 - 이 때, 다른 파일 함수호출
    #없으면 수고링

def on_subscribe(client, obj, mid, qos):
    print("Subscribed : " + str(mid))

broker = "220.69.209.45"
port = 4001

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect(broker, port, 60)
client.loop_start()


#스크립트에 필요한 요소
#입력되는 값 - gateway_id, device_id, resource_id
#토픽 - gateway_id/#
#메타데이터를 통해 해당 디바이스가 있는지부터 탐색. items 번호는 메타데이터에 같이 저장할 것.


