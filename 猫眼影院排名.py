import requests,sqlite3,time
请求头={
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
    "Host": "box.maoyan.com",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; Coolpad Y91-921 Build/LMY47V)",
    "Connection": "Keep-Alive",
}
数据库=sqlite3.connect("数据.db")
游标=数据库.cursor()
try:
    游标.execute("DROP TABLE 影院数据")
except:
    pass
游标.execute("CREATE TABLE 影院数据 (排名 INTEGER PRIMARY KEY,影院编码 INTEGER,影院,票房,人次,场均人次,平均票价)")
数据库.commit()
日期=time.strftime("%Y%m%d", time.localtime())
响应=requests.get("https://box.maoyan.com/api/cinema/cinemaBox/filter/list.json?typeId=0&date="+日期+"&limit=799",headers=请求头)
响应数据=响应.json()["data"]
全国=响应数据["all"]
游标.execute("INSERT INTO 影院数据 (影院,票房,人次,场均人次,平均票价) VALUES ('"+全国["cinemaName"]+"','"+全国["boxInfo"]+"','"+全国["viewInfo"]+"','"+全国["avgShowView"]+"','"+全国["avgViewBox"]+"')")
print("写入数据："+全国["cinemaName"])
for 临时 in 响应数据["list"]:
    游标.execute("INSERT INTO 影院数据 (影院编码,影院,票房,人次,场均人次,平均票价) VALUES ("+str(临时["cinemaId"])+",'"+临时["cinemaName"]+"','"+临时["boxInfo"]+"','"+临时["viewInfo"]+"','"+临时["avgShowView"]+"','"+临时["avgViewBox"]+"')")
    print("写入数据："+临时["cinemaName"])
数据库.commit()
数据库.close()