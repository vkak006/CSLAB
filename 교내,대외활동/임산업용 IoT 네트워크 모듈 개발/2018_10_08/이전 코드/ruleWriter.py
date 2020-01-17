import json
import os
import sys

#가지고있는 값들
#게이트웨이에 연결된 단말리스트, 디바이스 정보 리스트 및 디바이스 아이디에 따른 센서정보들
#device_id의 type : 
#resource_id의 type :
#items 판별 : 

class RuleWriter:
    def __init__(self,mod):
        self.script = ""
        self.mods = mod


    def setScript(self, data):
        self.script = data


    def getScript(self):
        return self.script


    def ruleImport(self, mods):
        import_line = ""
        for i in mods:
            import_line += "import " + i
            import_line += "\n"
        path = "var path = '/home/odroid/info/'\n\n"
        import_line += path
        
        return import_line

              
    def ruleIf(self,gPath,resource_id,items):
        if_line = ""
        data = []
        data.append("if(file.exists()){\n" + "var gateway = new BufferedReader(new FileReader(" + gPath + "))}")
        data.append("if(file_sensor.exists()){")        
        data.append("var data = new BufferedReader(new FileReader(path + clientId + '/' + sensorId + '.json'))")
        data.append("var datas = transform('JSONPATH', '$.resource_id',data.readLine())\n")

        for i in resource_id:
            #items : 외부로 부터 받는 번호값
            if_line += "if(datas == '" + i['resource_id'] + "'){\n\t"
            if_line += "postUpdate(" + i['type'] + "_" + items + ",input_data)\n}\n"

        return "\n".join(data) + if_line + "}\n"


    def ruleValue(self,gPath,rPath,item):
        value = []
        value.append("var Topic = transform('JSONPATH','$.topic',status_"+ item +")")
        value.append("var input_data = transform('JSONPATH','$.topic',status_"+ item +")")
        value.append("var clientId = Topic.split('/').get(1)")
        value.append("var sensorId = Topic.split('/').get(2)")
        value.append("var file = new File(" + gPath +  ")")
        value.append("var file_sensor = new File(" + rPath + ")\n")

        return "\n".join(value)


    def ruleMain(self, device_id, resource_id, items):
        item = str(items)

        gPath = "path + clientId +'.json'"
        rPath = "path + clientId + '/' + sensorId + '.json'"

        main = self.ruleImport(self.mods)
        main = "rule \"update_sensor" + device_id + "\"\n"
        main += "when\n" + "Item status_" + item + " received update\n"
        main += "then\n"
        main += self.ruleValue(gPath,rPath,item) + self.ruleIf(gPath,resource_id,item)
        main += "end"

        self.setScript(main)

        #with open("/etc/openhab2/rules/" + i['device_id'] + ".rules", 'w') as f:
        #    f.write(self.script)

    
