import sitemapScript as SS
import itemScript as IS
import ruleScript as RS

init = IS.ms.InitSetting()
item = IS.ItemScript()
sitemap = SS.SitemapScript()

def check(device_id, resource_id):
    item.check_file(device_id,resource_id)
    sitemap.check_file(device_id,resource_id)
    
def scriptWrite():
    item.script_write()
    sitemap.script_write()
    
