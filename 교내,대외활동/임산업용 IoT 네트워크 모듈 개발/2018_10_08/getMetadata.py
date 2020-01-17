#save Metadata
#device json파일에 번호값 저장

import elasticsearch as es
import json
import os
import sys

class getMetadata():

    def __init__(self, addr, port):
        self.gateway_data = [] #Gateway 정보 리스트.
        self.device_data = [] #Device 정보 리스트
        self.device = {} #Device_id : {센서정보,센서정보,센서정보}, Device_id        
        self.gateway = es.Elasticsearch(addr+":"+port)
        self.gateway_id = ""

        self.checkDir()

    def checkGateway(self):
        if os.path.isfile("gateway_id.txt"):
            with open("gateway_id.txt","r") as f:
                self.gateway_id = f.read()
                print("Found gateway txt data")       
        else:
            print("ERROR : Not found gateway information.")
            sys.exit(1)
            
    def checkDir(self):
        if not os.path.isdir("device"):
            os.mkdir("device")
            
        if not os.path.isdir("resource"):
            os.mkdir("resource")


    def setES(self):

        gateway_temp = []
        gatewayID = self.gateway.search(index = 'test2', doc_type = 'clients', body = {'query':{'match':{'snode':self.gateway_id }}})['hits']
        if gatewayID['total'] != 0:
            for i in gatewayID['hits']:
                gateway_temp.append(i['_source'])
                #print(i['_source'])
            
        else:
            print("ERROR : Not found gateway information. (400)")
            sys.exit(1)

        for i in gateway_temp:
            resource = self.gateway.search(index = 'test3', doc_type = 'sensors', body = {'query':{'match':{'device_id':i['device_id']}}})['hits']
            if resource['total'] == 0:
                #Device 정보만 저장하고 센서값을 저장하는 디바이스 폴더는 생성하지않음
                print(i['name'] + " - Not found sensors info")
                with open("device/" + i['device_id'] + ".json",'w') as f:
                    f.write(str(i))
                continue
            else:
                self.gateway_data.append(i)

            for j in range(resource['total']):
                self.device_data.append(resource['hits'][j]['_source'])

            self.device[i['device_id']] = self.device_data
            
    def cashingES(self):
        self.setES()

        for i in self.gateway_data:
            with open("device/" + i['device_id'] + ".json",'w') as f:
                f.write(str(i))

            if not os.path.isdir("resource/" + i['device_id']):
                os.mkdir("resource/" + i['device_id'])

            for j in self.device[i['device_id']]:
                with open("resource/"+ i['device_id'] + "/" + str(j['resource_id']) + ".json", 'w') as s:
                    s.write(str(j))


#a = getMetadata("220.69.209.17","9200")
#a.checkGateway()
#a.cashingES()
