import json
import os
import sys

#상황인지 서비스

class ContextAware():
    def __init__(self, device, resource, act):
        self.search = False
        self.device = device
        self.resource = resource
        self.act = act
        pass

    def check_file(self):
        
        pass
    
    def script_combine(self, random_num, service):
        rule_script = []
        rule_script.append("rule CA_" + random_num)
        rule_script.append("when\n" + "Items status_" + random_num + " received update")
        rule_script.append("then")

        #상황인지 스크립트
        #서비스의 종류에 따라 스크립트가 달라진다.
        
        rule_script.append("end")

        "\n".join(rule_script)
        
        pass

    def script_write(self):
        pass
    
#example

a = ContextAware("000000330846A001",1,5)

