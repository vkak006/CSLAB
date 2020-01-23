%pyspark
from pyspark import SparkContext
from pyspark.sql import SQLContext
from pyspark.sql.window import *
from pyspark.sql import functions as f
from pyspark.sql.functions import col, lit, exp, udf
from pyspark.sql.functions import when
from pyspark.sql.types import *
from pyspark.sql.functions import monotonically_increasing_id 

import pandas as pd
import numpy as np
import datetime

#세션 분석관련 함수
#별도로 사용 X
def sessionCal(data):
    try:
        temp = 0
        for i in range(len(data.index)):
            if i == len(data.index)-1:
                if (data.timestamps[i] - data.timestamps[i-1]).seconds < 1:
                    data.session[i] = temp
                else:
                    data.session[i] = temp+1
                break
            if (data.timestamps[i+1] - data.timestamps[i]).seconds < 1:
                data.session[i] = temp
            else:
                data.session[i] = temp
                temp += 1
    except:
        data.session[i] = 0
        print("Except : This user has one row. So, Session num is 0")

sqlContext = SQLContext(sc)
df = sqlContext.read.json("/data/json_file_100000.json")
df.printSchema()
df.createOrReplaceTempView("tables")

allDF = spark.sql("SELECT geoip, user_agent, os FROM tables GROUP BY geoip, user_agent, os")
allDF.createOrReplaceTempView("all")

#hacking bot 탐색쿼리.
#out ===> ip, user_agent
req_h = "request LIKE '%php%' OR request LIKE '%admin%' OR request LIKE '%username=root%' OR user_agent LIKE '%mj12%' OR user_agent LIKE '%bot%'"
sub_h = "SELECT geoip.ip, user_agent FROM tables WHERE " + req_h

#searching bot 탐색쿼리.
#out ===> ip, user_agent
req_s = "user_agent LIKE '%Daum%' OR user_agent LIKE '%Mozilla/5.0%' OR user_agent LIKE '%Chrome%'"
sub_s = "SELECT geoip.ip, user_agent FROM tables WHERE " + req_s

#botDF 정의
bot_hDF = spark.sql("SELECT DISTINCT a.* FROM all a, ("+sub_h+") sub WHERE a.geoip.ip = sub.ip AND a.user_agent = sub.user_agent")
bot_s = spark.sql("SELECT DISTINCT a.* FROM all a, ("+sub_s+") sub WHERE a.geoip.ip = sub.ip AND a.user_agent = sub.user_agent")

bot_hDF.createOrReplaceTempView("hack")
bot_s.createOrReplaceTempView("bot_s")

bot_sDF = spark.sql("SELECT s.* FROM bot_s s LEFT JOIN hack h ON s.geoip.ip=h.geoip.ip AND s.user_agent=h.user_agent WHERE h.geoip.ip IS NULL")
bot_sDF.createOrReplaceTempView("search")

hackDF = bot_hDF.withColumn("bot",lit("hack"))
searchDF = bot_sDF.withColumn("bot",lit("search"))

#userDF 정의
userDF_h = spark.sql("SELECT a.* FROM all a LEFT JOIN hack b ON a.geoip.ip = b.geoip.ip AND a.user_agent = b.user_agent WHERE b.geoip.ip IS NULL")
userDF_h.createOrReplaceTempView("userDF_h")

userDF = spark.sql("SELECT DISTINCT a.* FROM userDF_h a LEFT JOIN search b ON a.geoip.ip = b.geoip.ip AND a.user_agent = b.user_agent WHERE b.geoip.ip IS NULL")
botDF.coalesce(1).write.format("json").save("/output/botDF")

#게시글 관련 DF
urlDF = sqlContext.read.json("/data/url_json.json")
urlDF.printSchema()
urlDF.createOrReplaceTempView("url_tables")

request_subquery2 = "SELECT b.uid, b.post_num, b.post_name, a.geoip, a.request FROM tables a, url_tables b WHERE a.request LIKE CONCAT('%','uid=',b.uid,'%')"

uidDF = spark.sql(request_subquery2)
uidDF.show()
