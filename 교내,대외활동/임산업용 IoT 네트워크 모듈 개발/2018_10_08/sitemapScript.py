import json
import os
import sys
import AddScript as ms

class SitemapScript(ms.ScriptWriter):
    def __init__(self):
        #파일 유무 탐색을 위한 변수
        super(SitemapScript,self).__init__()
    
    def check_file(self, device_id, resource_id):
        super(SitemapScript,self).check_file(device_id, resource_id)

    
    def script_combine(self):
        sitemap_str = ""
        
        if self.search == True:
            sitemap_name = i['snode']
            
            sitemap_str = "sitemap " + sitemap_name + " label=" + i['name'] + "{\n"
            sitemap_str += "Frame label=\"단말정보\"{\n"
            sitemap_str += "Text item=state_" + str(a) + "\n"
            sitemap_str += "Text item=gateway_id_" + str(a) + "\n"
            sitemap_str += "Text item=uid_" + str(a) + "\n"
            sitemap_str += "Text item=name_" + str(a) + "\n"
            sitemap_str += "Text item=date_" + str(a) + "\n"
            sitemap_str += "Text item=user_id_" + str(a) + "\n"
            sitemap_str += "Text item=gps_lat_" + str(a) + "\n"
            sitemap_str += "Text item=gps_lon_" + str(a) + "\n}\n"

            for i in self.resource_id[self.device]:
                sitemap_str += "Frame label=\"" + changeType(j['resource_id'])[0] + "\"{\n"
                sitemap_str += "Text item=" + i['type'] + "_" + str(self.device_id['num']) + "{\n"
                sitemap_str += "Text item=" + i['type'] + "_" + str(self.device_id['num']) + "_name\n"
                sitemap_str += "Text item=" + i['type'] + "_" + str(self.device_id['num']) + "_company\n}\n}\n" 

            sitemap_str += "\n}"

        else:
            print("Error : Not found device data")

        return sitemap_str


    def script_write(self):
        sitemap = self.script_combine()

        with open("etc/openhab2/sitemaps/" + str(self.device_id['num']) + ".sitemaps",'w') as f:
            f.write(device)

        print("Success!")    
