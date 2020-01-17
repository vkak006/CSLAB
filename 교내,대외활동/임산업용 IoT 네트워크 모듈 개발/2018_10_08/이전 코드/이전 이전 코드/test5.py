import elasticsearch as es
import json
import os
import sys
import requests

sensor_data = []
dirname = 'client'
file = ""

#단말 정보 확인
if os.path.isfile("snode.txt"):
    with open("snode.txt",'r') as f:
        file = f.read()
else:
    print("Not found clientID info")
    sys.exit(1)

client = es.Elasticsearch("220.69.209.17:9200")
clientID = client.search(index = 'test2', doc_type = 'clients', body = {'query':{'match':{'snode':file }}})['hits']

#해당 단말과 맞는 단말인지 아닌지 판별
if clientID['total'] == 0:
    print("Client ID not found")
    sys.exit(1)

#clientID를 JSON형태로 저장!
clientID = clientID['hits'][0]['_source']
clientID_search = clientID['client_id']

#단말기의 정보와 동일한 센서들의 정보를 가져온다
#위와 동일하게 센서정보가 있는지 없는지 판별
sensors = client.search(index = 'test3', doc_type = 'sensors', body = {'query':{'match':{'client_id':clientID_search}}})['hits']

if sensors['total'] == 0:
    print("Not found sensors info")
    sys.exit(1)

for i in range(sensors['total']):
    sensor_data.append(sensors['hits'][i]['_source'])
    print(sensor_data[i])

#센서 정보는 client라는 폴더에 저장
#단, 폴더가 존재하지않는다면 만들어준다. + 수정시에는 dirname을 client ID 값을 넣어준다.
if not os.path.isdir(clientID_search):
    os.mkdir(clientID_search)

#JSON 형태로 단말정보, 센서정보 저장
with open(clientID_search + ".json",'w') as f:
    f.write(str(clientID))

for j in sensor_data:
    with open(clientID_search + "/" + str(j['sensor_id']) + ".json",'w') as f:
        f.write(str(j))

#센서 정보 아이템파일 작성
#수정 필요. 하나의 아이템 파일에 작성하며, 파일 명칭은 단말의 Client_ID와 같다
if not os.path.isfile("/etc/openhab2/items/" + clientID_search + ".items"):
    for i in sensor_data:
        sensor_str = "String " + i['type'] + "_1 \"" + i['type'] + "[%s]\"\n"
        sensor_str += "String " + i['type'] + "_1_name \"제품명[%s]\"\n"
        sensor_str += "String " + i['type'] + "_1_company \"제조사[%s]\"\n\n"

        with open("/etc/openhab2/items/" + clientID_search + ".items", 'a') as f:
            f.write(sensor_str)
            
    sensor_main = "String state_1 \"받은 데이터[%s]\" {mqtt=\"<[mosq:#:state:default]\"}"
    with open("/etc/openhab2/items/" + clientID_search + ".items", 'a') as f:
            f.write(sensor_main)

    
#단말 정보 업데이트
requests.put("http://192.168.1.50:8080/rest/items/snode_1/state", clientID['snode'])
requests.put("http://192.168.1.50:8080/rest/items/uid_1/state", clientID['client_id'])
requests.put("http://192.168.1.50:8080/rest/items/name_1/state", clientID['name'].encode('utf-8'))
requests.put("http://192.168.1.50:8080/rest/items/date_1/state", clientID['date'])
requests.put("http://192.168.1.50:8080/rest/items/user_id_1/state", clientID['user_id'])
requests.put("http://192.168.1.50:8080/rest/items/gps_lat_1/state", str(clientID['gps:lat']))
requests.put("http://192.168.1.50:8080/rest/items/gps_lon_1/state", str(clientID['gps:lon']))

#센서 정보 업데이트
#하나의 파일에 모아두어도 상관없다. 왜냐하면 아이템 설정값 접근시에는 파일에 따라 접근하는 것이 아닌
#아이템의 존재 유무에 따라 접근하기 때문.

for i in sensor_data:
    requests.put("http://192.168.1.50:8080/rest/items/" + i['type'] + "_1_name/state", str(i['product_name']))
    requests.put("http://192.168.1.50:8080/rest/items/" + i['type'] + "_1_company/state", str(i['produce_company']))


#단말명/센서/센서타입?- 데이터만 딸랑오면 얘가 뭔지모르니까
#아이템 파일입출력 토픽을 실시간으로 기재해야하는데, # {"topic" : "2222/1222/412412"}

#구현해야할 것 리스트
#1) 토픽형태로 조합해서 아이템에 기술해주면 개꿀맛
#2) 이미 생성되어있는 아이템이 있다면 생성 생략하도록 파일 이름을 읽을 수 있는 코드 작성

#try / except 문으로 변경할 것`
