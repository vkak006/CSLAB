import json
import os
import sys

class ScriptWriter():
    def __init__(self):
        #파일 유무 탐색을 위한 변수
        self.search = False
        self.device = ""
        self.device_id = {}
        self.resource_id = {}
    
    def check_file(self, device_id, resource_id):
        device_path = "device/" + device_id + ".json"
        resource_path = "resource/"
        resource_list = []
        
        if os.path.isfile(device_path):

            self.device = device_id
            
            with open(device_path, 'r') as f:
                mid = f.readline()
                mid = mid.replace("'",'"')
                self.device_id = json.loads(mid)
                self.search = True

                file_list = os.listdir(resource_path + device_id)
                file_list.sort()

                #이 밑에서 센서값이 있는가 없는가가 결정됨
                if len(file_list) != 0:
                    for i in file_list:
                        with open(resource_path + device_id + "/" + i, "r") as f:
                            resource = f.readline().replace("'",'"').replace("None" , 'null')
                            resource_list.append(json.loads(resource))
                            
                    self.resource_id[device_id] = resource_list
                else:
                    self.resource_id = None
                    print("Warning : Success found device data. but, Not found resource data")
        else:
            print("Error : Not found device data")
            self.search = False    

    def script_combine(self):
        pass

    def script_write(self):
        pass


class InitSetting():
    def __init__(self):
        self.device = "device"
        self.resource = "resource"

        if not os.path.isdir(self.device):
            os.mkdir("device")
        if not os.path.isdir(self.resource):
            os.mkdir("resource")


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
