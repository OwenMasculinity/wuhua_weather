import datetime
import requests
from bs4 import BeautifulSoup as bs
import pymysql
import time
import sys
import os

"""
观测地点：武汉，天河机场	METAR ZHHH 041900Z 23003MPS 3000 BR NSC 30/27 Q1001 NOSIG
"""

# 重启程序
def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


# 设置日期
if os.path.exists(r'err_date.txt'):
    with open('err_date.txt', 'r') as f_open:
        for line in f_open:
            date_str = line.strip("\n")
        date = datetime.datetime.strptime(date_str, '%Y/%m/%d')
else:
    date = datetime.datetime.strptime('2001/03/20', '%Y/%m/%d')  # 初始日期从2001年3月20日开始

delta = datetime.timedelta(days=1)  # 初始间隔为1天
now = datetime.datetime.now()
now_str = str(now)[0:10].replace("-", "/")


# 数据库设置
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='19950624zlx', db='wuhan_environment', charset='utf8mb4')
cursor = conn.cursor()
sql_insert_history_weather = "INSERT INTO history_weather VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"


# 网络连接设置
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}


# 爬取数据
while 1:
    try:
        date_str = str(date)[0:10].replace("-", "/")
        url = "https://www.wunderground.com/history/airport/ZHHH/"+date_str+"/DailyHistory.html?req_city=Wuhan&req_state=&req_statename=China&reqdb.zip=&reqdb.magic=&reqdb.wmo="
        r = requests.get(url,headers=headers)
        soup = bs(r.text, "html.parser")
        metars = soup.find_all(name="tr",attrs={"class":"no-metars"})
        metars = metars[::-1]  # 序列翻转

        for metar in metars:
            current_weather=metar.find_all("td")
            if len(current_weather)==12:
                Time_CST=current_weather[0].text.replace("\n","")
                Temperature=current_weather[1].text.replace("\n","")
                Windchill = ""
                Dew_Point=current_weather[2].text.replace("\n","")
                Humidity=current_weather[3].text.replace("\n","")
                Pressure=current_weather[4].text.replace("\n","")
                Visibility=current_weather[5].text.replace("\n","")
                Wind_Dir=current_weather[6].text.replace("\n","")
                Wind_Speed=current_weather[7].text.replace("\n","")
                Gust_Speed=current_weather[8].text.replace("\n","")
                Precip=current_weather[9].text.replace("\n","")
                Events=current_weather[10].text.replace("\n","")
                Conditions=current_weather[11].text.replace("\n","")
            elif len(current_weather)==13:
                Time_CST=current_weather[0].text.replace("\n","")
                Temperature=current_weather[1].text.replace("\n","")
                Windchill = current_weather[2].text.replace("\n","")
                Dew_Point=current_weather[3].text.replace("\n","")
                Humidity=current_weather[4].text.replace("\n","")
                Pressure=current_weather[5].text.replace("\n","")
                Visibility=current_weather[6].text.replace("\n","")
                Wind_Dir=current_weather[7].text.replace("\n","")
                Wind_Speed=current_weather[8].text.replace("\n","")
                Gust_Speed=current_weather[9].text.replace("\n","")
                Precip=current_weather[10].text.replace("\n","")
                Events=current_weather[11].text.replace("\n","")
                Conditions=current_weather[12].text.replace("\n","")

            print("Date:{}\t"
                  "Time_CST:{}\tTemperature:{}\tWindchill:{}\tDew_Point:{}\tHumidity:{}\tPressure:{}\tVisibility:{}\t"
                  "Wind_Dir:{}\tWind_Speed:{}\tGust_Speed:{}\tPrecip:{}\tEvents:{}\tConditions:{}"
                  .format(date_str,Time_CST,Temperature,Windchill,Dew_Point,Humidity,Pressure,Visibility,Wind_Dir,Wind_Speed,Gust_Speed,Precip,Events,Conditions))

            # 数据插入数据库
            try:
                cursor.execute(sql_insert_history_weather,
                               (date_str,Time_CST,Temperature,Windchill,Dew_Point,Humidity,Pressure,Visibility,Wind_Dir,Wind_Speed,Gust_Speed,Precip,Events,Conditions))
                conn.commit()
                print("已插入数据库" + "\n")
            except pymysql.err.IntegrityError:
                print("数据库中已经存在" + "\n")

        if date_str==now_str:
            break

        date=date+delta
        time.sleep(0.5)

    except Exception as e:
        print("程序运行错误:{}".format(e))
        print("1s后，程序重新运行...." + "\n")
        with open('err_date.txt', 'a', encoding='utf-8') as err_page:
            err_page.write(date_str+"\n")
        conn.close()
        time.sleep(1)
        restart_program()

print("任务完成")