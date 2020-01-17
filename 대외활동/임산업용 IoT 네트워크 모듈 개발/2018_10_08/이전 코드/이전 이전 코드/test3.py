import elasticsearch as es
import json
import os
import sys
import requests

sensor_data = []

with open("snode.txt",'r') as f:
    snode = f.read()


client = es.Elasticsearch("220.69.209.17:9200")
clientID = client.search(index = 'lora_c', doc_type = 'clients', body = {'query':{'match':{'snode': snode }}})['hits']

if clientID['total'] == 0:
    print("not found1")
    sys.exit(1)

#clientID를 JSON형태로 저장!
clientID = clientID['hits'][0]['_source']
uid = clientID['uid']

#sensors에서 port와 type를 얻어낸다.
sensors = client.search(index = 'lora', doc_type = 'sensors', body = {'query':{'match':{'uid' : uid}}})['hits']

if sensors['total'] == 0:
    print("not found2")
    sys.exit(1)

for i in range(sensors['total']):
    sensor_data.append(sensors['hits'][i]['_source'])
    print(sensor_data[i])

#센서 정보는 client라는 폴더에 저장
dirname = 'client'
if not os.path.isdir(dirname):
    os.mkdir(dirname)

with open(snode + ".json",'w') as f:
    f.write(str(clientID))

for j in sensor_data:
    with open("client/" + j['type'] + ".json",'w') as f:
        f.write(str(j))

requests.put("http://192.168.1.50:8080/rest/items/snode_1/state", clientID['snode'])
requests.put("http://192.168.1.50:8080/rest/items/uid_1/state", clientID['uid'])
requests.put("http://192.168.1.50:8080/rest/items/name_1/state", clientID['name'])
requests.put("http://192.168.1.50:8080/rest/items/date_1/state", clientID['date'])
requests.put("http://192.168.1.50:8080/rest/items/user_id_1/state", clientID['user_id'])
requests.put("http://192.168.1.50:8080/rest/items/gps_lat_1/state", str(clientID['gps_lat']))
requests.put("http://192.168.1.50:8080/rest/items/gps_lon_1/state", str(clientID['gps_lon']))


