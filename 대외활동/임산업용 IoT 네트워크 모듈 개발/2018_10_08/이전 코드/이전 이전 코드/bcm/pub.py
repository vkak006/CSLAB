#-*-coding: utf-8-*-

import paho.mqtt.client as paho
import paho.mqtt.publish as publish
import crawler
import json
import time
import datetime


#크롤러 객체 저장
crawlerList = []

#센서 key값과 port 번호
port = {"temp": 2, "hum" : 3, "wind" : 4, "wind_dir" : 7, "rain" : 9, "sun" : 1, "soil10" : 6}



#크롤러 객체 생성 함수
def makeCrl():
    for code in states:
        crawlerList.append(crawler.Crawler(code))


#uid 매개변수 추가해야됨
#센서값을 MQTT 메시지로 변환, MQTT 브로커로 전송

def changeMessagePublish(code, sensor, data):
    snode = "0000001"
    client_id = str(code.zfill(16))
    sensor_id = str(port[sensor])
    topic = "sensor/" + client_id + "/" + sensor_id
    #uuid = hex(int(uuid, 16))
    msg = {"time" : time, "data" : data}
    publish.single(topic, str(msg), hostname = "220.69.209.45", port = 1883, protocol = paho.MQTTv311)
    print(topic)
    print(msg)
    

states = ["716823A001", "336812A001"]
makeCrl()


#changeMessagePublish 함수에 사용되는 전역변수
time = ""

for crl in crawlerList:    
    
    msg = crl.pubMessage()
    #메시지가 없을 때
    if (msg == None or msg == ""):
        print(".")
        continue

    #풍향이 정온인 경우 0.0으로 수정
    msg = msg.replace(":'정온'", ":'0.0'") 
    msg = msg.replace("'", '''"''')


    dict = json.loads(msg)


    #전역변수 time값 설정
    timeStr = dict["x"]
    t = datetime.datetime.strptime(timeStr, "%Y/%m/%d %H:%M")
    ###############만약 연도값이 2자리라면 %Y를 %y로 교체해주세요################
    dict["x"] = t.strftime("%Y-%m-%dT%H:%M:%S")
    time = dict["x"]


    for sensor in dict:
        #key 값이 x, lat, lon, region일 경우 메시지 발행 X -> port에 존재하지 않는 key
        #값이 "X", "-", "*"일 경우 메시지 발행 X
        try:
            print(sensor + " " + dict[sensor])
            if(sensor == "sun"):
                dict[sensor] = float(dict[sensor].replace(",", ""))
            else:
                dict[sensor] = float(dict[sensor])
            changeMessagePublish(crl._code, sensor, dict[sensor])
        except:
            continue


    
    #print(dict)
    #msg = json.dumps(dict, ensure_ascii=False)

    
    #mqttc.publish(crl.topic, msg)
