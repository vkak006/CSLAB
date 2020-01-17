import json
import os
import sys

def convertStr(item):
    convert_str = "Float::parseFloat(String::format(\"%s\","+ item + ".state).replace(\' \',\'\'))"
    return convert_str

#상황인지 서비스

class ContextAware():
    def __init__(self, device, resource, act):
        self.search = False
        self.device = device

        #배열
        self.resource = resource
        self.act = act 
        self.num = -1

    def search_file(self):
        resource = []
        
        if self.device != "" || len(self.resource) != 0 :  
            #파일 유무 조건문 사실 필요없음. 이미 ES에 있는걸 저장해두었기 때문.
            with open("device/" + self.device + ".json", 'r')as f:
                device = f.read()
                self.num = device['num']

            for i in self.resource: 
                with open("resource/" + self.device + "/" + self.resource + ".json",'r') as f:
                    resource.append(i)
                    
    #조건 스크립트 코드
    def setIf(self,resource):
        string = "if(){\n"
        string += "\t내용\n}"
        string += "else{\n"
        string += "\t내용\n}"

        return string
    
    def script_combine(self, item_num):
        num = item_num
        
        rule_script = []
        rule_script.append("rule CA_" + num)
        rule_script.append("when\n" + "Items status_" + num + " received update")
        rule_script.append("then")

        #상황인지 스크립트
        #서비스의 종류에 따라 스크립트가 달라진다.
        #1. 한개의 센서 - 한개의 엑츄에이터 : 변수 한개
        #2. 두개의 센서 - 한개의 액츄에이터 : 변수 두개

        #일단 1의 경우만 생각하고 코딩
        rule_script.append("var sensor_1 = " + convertStr(self.resource))
        rule_script.append(self.setIf(self.resource))
`       rule_script.append("end")

        "\n".join(rule_script)
        
        return rule_script

    def script_write(self):
        pass
    
#example

a = ContextAware("000000330846A001",1,5)

