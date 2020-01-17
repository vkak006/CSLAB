import elasticsearch as es
import json
import os

ulist = [] #total id count
clients = [] #board id count

client = es.Elasticsearch("220.69.209.17:9200")
total = client.search(index = 'test', doc_type = '0001')['hits']

hit_count = total['total']


for i in range(hit_count):
    ulist.append(total['hits'][i]['_id'])


user = client.get(index = 'test', doc_type = '0001', id = ulist[ulist.index('user')])

for s in ulist:
    if s != 'user':
        clients.append(client.get(index ='test', doc_type = '0001', id = s))
        

#일단 단일 단말로 가정한다.
#유저, 단말 별 정보, 센서정보는 따로 따로 저장한다.
#user_id를 통하여 단말정보를 탐색하여야 하며, 각 센서의 uid를 통해 단말 탐색

#디렉토리 확인 및 생성

dirname = '/info/client'
if not os.path.isdir(dirname):
    os.mkdir(dirname)

with open("/home/odroid/info/user.json",'w') as f:
    f.write(user['_sourse'])
    
with open("/home/odroid/info/client.json", 'w') as f:
    f.write(clients[0]['_sourse'])

with open("/home/odroid/info/client/lux.json",'w') as f:
    f.write(


#print (json.dumps(total, indent=2))
#doc = client.get(index = 'test', doc_type = '0001', id='board')
