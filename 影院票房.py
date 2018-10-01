import requests,sqlite3,time
请求头={
    "Content-Type": "application/json",
    "Accept-Encoding": "gzip",
    "Accept-Language": "zh-Hans-CN, zh-Hans; q=0.8, en-US; q=0.5, en; q=0.3",
    "Host": "box.maoyan.com",
    "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1.1; Coolpad Y91-921 Build/LMY47V)",
    "Connection": "Keep-Alive",
    "refresh": "false",
}
数据库=sqlite3.connect("数据.db")
游标=数据库.cursor()
try:
    游标.execute("DROP TABLE 影院票房数据")
except:
    pass
游标.execute("CREATE TABLE 影院票房数据 (影院,片名,上映天数,实时票房,人次,场次,场均人次,平均票价,上座率,票房占比,拍片占比,排座占比,累计票房)")
数据库.commit()
日期=time.strftime("%Y%m%d", time.localtime())
游标.execute("SELECT 影院编码,影院 FROM 影院数据")
for 临时2 in 游标.fetchall()[1:]:
    响应=requests.get("https://box.maoyan.com/api/cinema/cinemaBox/movie/box/list.json?cinemaId="+str(临时2[0])+"&date="+日期,headers=请求头)
    响应数据=响应.json()["data"]
    for 临时1 in 响应数据["list"]:
        游标.execute("INSERT INTO 影院票房数据 (影院,片名,上映天数,实时票房,人次,场次,场均人次,平均票价,上座率,票房占比,拍片占比,排座占比,累计票房) VALUES ('"+临时2[1]+"','"+临时1["movieName"]+"','"+临时1["releaseInfo"]+"','"+临时1["boxInfo"]+"','"+临时1["viewInfo"]+"','"+临时1["showInfo"]+"','"+临时1["avgShowView"]+"','"+临时1["avgViewBox"]+"','"+临时1["avgSeatView"]+"','"+临时1["boxRate"]+"','"+临时1["showRate"]+"','"+临时1["seatRate"]+"','"+临时1["sumBoxInfo"]+"')")
    print("写入数据："+临时2[1])
    数据库.commit()
数据库.close()