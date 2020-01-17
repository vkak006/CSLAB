#스크립트 작성 규칙이 정의된 프로그램
#웹에서 장치 검색시, 명칭 : MAC 주소 형태여야한다.
#1) 메타데이터로 부터 해당 파일이 있는지 확인한다. 
#2) 메타데이터의 변동이 있을 때에만 실행되야함

import json
import os
import sys
import AddScript as ms

class ItemScript(ms.ScriptWriter):
    def __init__(self):
        #파일 유무 탐색을 위한 변수
        super(ItemScript,self).__init__()
    
    def check_file(self, device_id, resource_id):
        super(ItemScript,self).check_file(device_id, resource_id)

    
    def script_combine(self):
        device_item = ""
        resource_item = ""
        
        if self.search == True:
            device_item = "String state_" + str(self.device_id['num']) + " \"상태[%s]\"\n"
            device_item += "String gateway_id_" + str(self.device_id['num']) + " \"설치 지역[%s]\"\n"
            device_item += "String uid_" + str(self.device_id['num']) + " \"단말 고유번호[%s]\"\n"
            device_item += "String name_" + str(self.device_id['num']) + " \"단말 명칭[%s]\"\n"
            device_item += "String date_" + str(self.device_id['num']) + " \"단말 생성일자[%s]\"\n"
            device_item += "String user_id_" + str(self.device_id['num']) + " \"사용자[%s]\"\n"
            device_item += "String gps_lat_" + str(self.device_id['num']) + " \"설치위치(위도)[%s]\"\n"
            device_item += "String gps_lon_" + str(self.device_id['num']) + " \"설치위치(경도)[%s]\""

            for i in self.resource_id[self.device]:
                resource_item += "String " + i['type'] + "_" + str(self.device_id['num']) + " \"" + ms.changeType(i['resource_id'])[0] + "[%s]\" "+ms.changeType(i['resource_id'])[1]+"\n"
                resource_item += "String " + i['type'] + "_" + str(self.device_id['num']) + "_name \"제품명[%s]\"\n"
                resource_item += "String " + i['type'] + "_" + str(self.device_id['num']) + "_company \"제조사[%s]\"\n\n"
    
        else:
            print("Error : Not found device data")

        return device_item, resource_item


    def script_write(self):
        device, resource = self.script_combine()

        with open("etc/openhab2/items/device_" + str(self.device_id['num']) + ".items",'w') as f:
            f.write(device)

        if resource != "":    
            with open("etc/openhab2/items/resource_" + str(self.device_id['num']) + ".items",'w') as f:
                f.write(resource)

        print("Success!")        


#example
#a = ms.InitSetting()

#b = ItemScript()
#b.check_file("000000330846A001","1")
#b.script_write()



