import pymysql
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
# from keys import get_conn
from datetime import datetime, timedelta
import random
from pprint import pprint

def get_conn():
    return pymysql.connect(
        host='',
        user='root',
        password='',
        port=3306,
        db='logforyoudb',
        charset='utf8')



weekday = {"월":0, "화":1, "수":2, "목":3, "금":4, "토":5, "일":6}
weekday_converted = {}
for key, value in weekday.items():
    weekday_converted[value] = key

print(weekday_converted)
col = {"col_1" : 2, "col_2" : 11, "col_3" : 14, "col_4" : 18}
pat = [1, 2, 3]
data = []

for j in pat:
    i = 0
    s = datetime(2019, 3, 1, 0, 0)
    while(i<35):
        col_1 = random.randrange(1, 5)  # 수전증
        col_2 = str(random.randrange(5, 11)) + ":" + str(random.randrange(0, 59)) # 기상시간
        col_3 = round(random.random())  # 파국반응 
        col_4 = random.randrange(1, 10) # 술
        # print(">>>>>", s, type(s), weekday_converted[s.weekday()], " | col_1::", col_1, " | col_2::", col_2, " | col_3::", col_3, " | col_4::", col_4)
        # data.append({"pat_id" : j, "date" : s.strftime("%Y-%m-%d"), "col_id" : col['col_1'], "value" : col_1})
        # data.append({"pat_id" : j, "date" : s.strftime("%Y-%m-%d"), "col_id" : col['col_2'], "value" : col_2})
        # data.append({"pat_id" : j, "date" : s.strftime("%Y-%m-%d"), "col_id" : col['col_3'], "value" : col_3})
        # data.append({"pat_id" : j, "date" : s.strftime("%Y-%m-%d"), "col_id" : col['col_4'], "value" : col_4})
        data.append((j, s.strftime("%Y-%m-%d"), col['col_1'], col_1))
        data.append((j, s.strftime("%Y-%m-%d"), col['col_2'], col_2))
        data.append((j, s.strftime("%Y-%m-%d"), col['col_3'], col_3))
        data.append((j, s.strftime("%Y-%m-%d"), col['col_4'], col_4))   
        a = timedelta(days=1)
        s = s + a
        i += 1

pprint(data)

sql = '''
    insert into Log(pat_id, date, usercol_id, value) values(%(pat_id)s, %(usercol_id)s, %(date)s, %(value)s)
    '''

sql_1 = "insert into Log(pat_id, date, usercol_id, value) value(%s, %s, %s, %s)"

conn = get_conn()
try:
    with conn:
        cur = conn.cursor()
        # cur.executemany(sql, data)
        # cur.execute(sql, {'col_id': 18, 'date': '2019-04-04', 'pat_id': 3, 'value': 2})
        cur.executemany(sql_1, data)
        conn.commit()
except Exception as err:
    try:
        conn.rollback()
    except:
        print("Error on Rollback!!")


print("EEEEENNNNNNDDDDD!!!!!")