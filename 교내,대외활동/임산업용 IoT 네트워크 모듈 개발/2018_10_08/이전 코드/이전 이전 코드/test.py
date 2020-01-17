import elasticsearch as es
import json

client = es.Elasticsearch("220.69.209.17:9200")
doc = client.get(index = 'test', doc_type = '0001', id='board')

error =  True
overlap = False

#에러체크

#우선, 아이템에 중복된 내용이 있는가 체크. 폴더 검사


#items 생성시켜줄 정보
if error:
    j = doc["_source"]

    snode = "String snode \"위치[" + j["snode"] + "]\"\n"
    uid = "String uid \"Uid[" + j["uid"] + "]\"\n"
    name = "String name \"센서명[" + j["name"] + "]\"\n"
    date = "String date \"등록날짜[" + j["date"] + "]\"\n" 
    user_id = "String user_id \"사용자 ID[" + j["user_id"] + "]\"\n"
    gps_lat = "String gps_lat \"위도[" + str(j["gps:lat"]) + "]\"\n"
    gps_lon = "String gps_lon \"경도[" + str(j["gps:lon"]) + "]\"" 
    state = "String state \"단말 정보\""

    send = state + snode + uid + name + date + user_id + gps_lat + gps_lon

    #sitemap 추가시켜줄 정보
    snode_s = "Text item=snode"
    uid_s = "Text item=uid"
    name = "Text item=name"
    date = "Text item=date"
    user_id_s = "Text item=user_id"
    gps_lat_s = "Text item=gps_lat"
    gps_lon_s = "Text item=gps_lon"
    state_s ="Text item=state"

    send_s = "\tFrame label=\"단말정보\"\n\t\t" + state_s + "{\n\t\t\t" + uid_s  + "\n\t\t\t" + name  + "\n\t\t\t" + date + "\n\t\t\t" + user_id_s + "\n\t\t\t" + gps_lat_s + "\n\t\t\t" + gps_lon_s + "\n\t\t}\n\t}"

    #with open("/etc/openhab2/items/" + j["uid"], "w") as items:
    #    items.write(send)
    

    print(send)
    print(send_s)
