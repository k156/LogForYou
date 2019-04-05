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

# sql_truncate = "truncate table UsercolMaster"
# sql_insert = "insert into UsercolMaster(col_name, min, max, col_desc) values(%s,%s,%s,%s)"
# sql_truncate = "truncate table DisCode"
# sql_insert = "insert into DisCode(code, disease, sci_name) values(%s,%s,%s)"
sql_truncate = "truncate table Departments"
sql_insert = "insert into Departments(name) value(%s)"
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

        # for l in lst:
        #     if l[1] == "":
        #         print(l)
        #         ll = (l[0], l[3])
        #         sql_insert = "insert into UsercolMaster(col_name, min, max, col_desc) values(%s,null,null,%s)"
        #         cur.execute(sql_insert, ll)
        #     else:
        #         sql_insert = "insert into UsercolMaster(col_name, min, max, col_desc) values(%s,%s,%s,%s)"
        #         cur.execute(sql_insert, l)

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


csvFile = codecs.open("/Users/mac/Downloads/진료과.csv", "r", "utf-8")
# csvFile = codecs.open("/Users/mac/Downloads/disease code - 시트11.csv", "r", "utf-8")
# csvFile = codecs.open("/Users/mac/Downloads/dd - 시트2.csv", "r", "utf-8")
reader = csv.reader(csvFile, delimiter=',', quotechar='"')

lst = []
for row in reader:
    # lst.append([row[0] , row[1], row[2], row[3]])
    # lst.append([row[0], row[1], row[2]])
    lst.append(row[0])

print("00>>", lst[0])
print("11>>", lst[1])

save(lst)