import pymysql
import csv
import codecs

def get_conn():
    return pymysql.connect(
        host='35.194.112.136',
        user='root',
        password='log190321',
        port=3306,
        db='logforyoudb',
        charset='utf8')

sql_truncate = "truncate table UsercolMaster"
sql_insert = "insert into UsercolMaster(col_name, min, max, col_desc, dept_id) values(%s,%s,%s,%s,%s)"
isStart = True

def save(lst):
    try:
        conn = get_conn()
        conn.autocommit = False
        cur = conn.cursor()

        global isStart
        if isStart:
            cur.execute(sql_truncate)
            isStart = False

        cur.executemany(sql_insert, lst)
        conn.commit()
        print("Affected RowCount is", cur.rowcount, "/", len(lst))

    except Exception as err:
        try:
            conn.rollback()
        except:
            print("Error on Rollback!!")
            
        print("Error!!", err)

    finally:
        try:
            cur.close()
        except:
            print("Error on close cursor")

        try:
            conn.close()
        except Exception as err2:
            print("Fail to connect!!", err2)




csvFile = codecs.open("User_col.csv", "r", "utf-8")
reader = csv.reader(csvFile, delimiter=',', quotechar='"')

lst = []
for row in reader:
    lst.append([row[0] , row[1], row[2], row[3]])

print("00>>", lst[0])
print("11>>", lst[1])

save(lst)