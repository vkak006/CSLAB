import json
import os
import sys
import scriptMaker as sm
import getMetadata as gm

def getMD(address,port):
    g = gm.getMetadata(address, port)
    g.checkGateway()
    g.cashingES()


def setScript(device_id, resource_id):
    sm.check(device_id, resource_id)
    sm.scriptWrite()

getMD("220.69.209.17","9200")
setScript("000000330846A001","1")
