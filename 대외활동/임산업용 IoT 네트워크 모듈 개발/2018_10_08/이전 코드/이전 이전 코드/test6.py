import elasticsearch as es
import json
import os
import sys
import requests

device_data = []
device = {}
client_data = []
a = 1

file = ""

###### (0) 사용할 함수 정의 ######

def changeType(i):
    if i=='1':
        return ["일사량","<sun>"]
    elif i==2:
        return ["온도","<temperature>"]
    elif i==3:
        return ["습도","<humidity>"]
    elif i==6:
        return ["지습","<smoke>"]
    elif i==7:
        return ["풍향","<wind>"]
    elif i==8:
        return ["풍속","<flow>"]
    elif i==9:
        return ["강수량","<rain>"]
    elif i==11:
        return ["일조시간","<time>"]
    else:
        return ["not define",""]

###### (1) 데이터 가져오기 ######
#단말 정보 확인
if os.path.isfile("snode.txt"):
    with open("snode.txt",'r') as f:
        file = f.read()
else:
    print("Not found clientID info")
    sys.exit(1)

#단말 정보 가져오기.
#그 후, clientID를 JSON형태로 리스트에 저장
client = es.Elasticsearch("220.69.209.17:9200")
clientID = client.search(index = 'test2', doc_type = 'clients', body = {'query':{'match':{'snode':file }}})['hits']

if clientID['total'] == 0:
    print("Client ID not found")
    sys.exit(1)

for i in clientID['hits']:
    client_data.append(i['_source'])

#센서 정보 가져오기.
#위와 마찬가지로, 센서가 없다면 종료

for i in client_data:
    device_data = []
    sensors = client.search(index = 'test3', doc_type = 'sensors', body = {'query':{'match':{'client_id':i['client_id']}}})['hits']

    if sensors['total'] == 0:
        print("Not found sensors info")
        continue
    for j in range(sensors['total']):
        device_data.append(sensors['hits'][j]['_source'])
        
    device[i['client_id']] = device_data


#print(json.dumps(device, indent=2))
    
###### (2) 데이터 JSON 형태로 저장하기 ######
#각기 폴더 존재유무 파악 후 생성
if not os.path.isdir("deviceId"):
    os.mkdir("deviceId")
    
if not os.path.isdir("sensors"):
    os.mkdir("sensors")

#각기 데이터 저장
for i in client_data:
    with open("deviceId/" + i['client_id'] + ".json",'w') as f:
        f.write(str(i))

    if not os.path.isdir("sensors/" + i['client_id']):
        os.mkdir("sensors/" + i['client_id'])

    for j in device[i['client_id']]:
        with open("sensors/"+ i['client_id'] + "/" + str(j['sensor_id']) + ".json", 'w') as s:
            s.write(str(j))


###### (3) items, sitemap 파일입출력 ######
#센서가 추가되었을 때의 경우는 고려하지않았음. total값으로 유추하도록 코딩 수정
#item
for i in client_data:
    if not os.path.isfile("/etc/openhab2/items/client_" + str(a) + ".items"):
        client_str = "String state_" + str(a) + " \"[%s]\"\n"
        client_str += "String snode_" + str(a) + " \"[%s]\"\n"
        client_str += "String uid_" + str(a) + " \"[%s]\"\n"
        client_str += "String name_" + str(a) + " \"[%s]\"\n"
        client_str += "String date_" + str(a) + " \"[%s]\"\n"
        client_str += "String user_id_" + str(a) + " \"[%s]\"\n"
        client_str += "String gps_lat_" + str(a) + " \"[%s]\"\n"
        client_str += "String gps_lon_" + str(a) + " \"[%s]\""
        
        with open("/etc/openhab2/items/client_" + str(a) + ".items", 'a') as f:
            f.write(client_str)
    sitemap_name = i['name'].replace(" ","_")
    
    sitemap_str = "sitemap " + sitemap_name + " label=" + i['name'] + "{\n"
    sitemap_str += "Frame label=\"단말정보\"{\n"
    sitemap_str += "Text item=state_" + str(a) + "\n"
    sitemap_str += "Text item=snode_" + str(a) + "\n"
    sitemap_str += "Text item=uid_" + str(a) + "\n"
    sitemap_str += "Text item=name_" + str(a) + "\n"
    sitemap_str += "Text item=date_" + str(a) + "\n"
    sitemap_str += "Text item=user_id_" + str(a) + "\n"
    sitemap_str += "Text item=gps_lat_" + str(a) + "\n"
    sitemap_str += "Text item=gps_lon_" + str(a) + "\n}\n"
    
    if not os.path.isfile("/etc/openhab2/items/" + i['client_id'] + ".items"):
        for j in device[i['client_id']]:
            item_str = "String " + j['type'] + "_" + str(a) + " \"" + changeType(j['sensor_id'])[0] + "[%s]\" "+changeType(j['sensor_id'])[1]+"\n"
            item_str += "String " + j['type'] + "_" + str(a) + "_name \"제품명[%s]\"\n"
            item_str += "String " + j['type'] + "_" + str(a) + "_company \"제조사[%s]\"\n\n"

            sitemap_str += "Frame label=\"" + changeType(j['sensor_id'])[0] + "\"{\n"
            sitemap_str += "Text item=" + j['type'] + "_" + str(a) + "{\n"
            sitemap_str += "Text item=" + j['type'] + "_" + str(a) + "_name\n"
            sitemap_str += "Text item=" + j['type'] + "_" + str(a) + "_company\n}\n}\n" 
            
            with open("/etc/openhab2/items/" + i['client_id'] + ".items", 'a') as f:
                f.write(item_str)
                
        item_main = "String state_" + str(a) + " \"받은 데이터[%s]\" {mqtt=\"<[mosq:withTopic/#:state:default]\"}"
        sitemap_str += "\n}"

        with open("/etc/openhab2/items/" + i['client_id'] + ".items", 'a') as f:
            f.write(item_main)

        with open("/etc/openhab2/sitemap/" + sitemap_name + ".sitemap", 'w') as f:
            f.write(sitemap_str)
        a = a + 1
        
    else:
        a = a + 1

    
#rule
    
###### (4) rule 파일입출력 ######
