import urllib.request
from bs4 import BeautifulSoup
import json
import datetime
import time


def getStates():
    state = []
    while True:
        try:
            page = urllib.request.urlopen("http://weather.rda.go.kr/weather/observation.jsp")
            break
        except:
            continue

    text = page.read().decode("utf8")
    html = BeautifulSoup(text, 'html.parser')
    rows = html.find_all("tr")

    count = 0

    for row in rows:
        if(count >= 2):
            data = row.find_all("td")
            source = str(data[0])
            name = source.split(">")[1]
            name = name.replace("</td", "").strip()
            data = source.split("'")[1]
            state.append(data)
	    
        count = count+1
    
    return state

class Crawler:
    _code = ""
    topic = ""
    
    today = ""
    time = ""

    lat = ""
    lon = ""
    region = ""
    
    chartData = []
    data = ""

    def __init__(self, code):
        self._code = code
        self.topic = "crl-" + code

    def getTime(self):
        now = datetime.datetime.now()
        now = now + datetime.timedelta(hours=-2)

        self.today = now.strftime("%Y%m%d%H")
        
        now = now + datetime.timedelta(hours=-1)
        
        self.time = now.strftime("%H:%M")
        self.time = self.time[:4] + "0"

    def getChartData(self):
        url = "http://weather.rda.go.kr/weather/observationGraph.jsp?time=" + self.today + "&stncode=" + self._code

        page = urllib.request.urlopen(url)

        text = page.read().decode("utf8")
        html = BeautifulSoup(text, 'html.parser')
 
        rows = html.find_all("script")[9]

        l = str(rows).split("SubCaption text=")[1]
        l = l.split("styleName")[0]

        self.chartData = str(rows).split("{")

        self.lon = l.split("(")[1].split(")")[0]
        self.lat = l.split("(")[2].split(")")[0]

        title = str(rows).split("Caption text=")[1]
        title = title.split("styleName")[0]

        self.region = title.split("(")[1].split(")")[0]
        
                
    def extData(self):
        self.data = ""
        count = 0
        self.chartData.pop(0)
        for dot in self.chartData:
            try:
                dataTime = dot.split("'x':")[1]
                dataTime = dataTime.split("'")[1]
            except:
                return
            
            if(dataTime[-5:] == str(self.time)):
                self.data = "{" + dot.split("}")[0] + ",'lat':" + self.lat + ",'lon':" + self.lon + ",'region':'" + str(self.region) + "'}"
                return

    def pubMessage(self):
        self.getTime()
        self.getChartData()
        self.extData()

        if(self.data != ""):
            return self.data
        

