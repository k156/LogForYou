# [ [name, email, password, birth, gender] , [] ]

import pymysql
import random
from sqlalchemy import func
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))
from keys import get_conn

fam_names = list("김이박최강고윤엄한배성백전황서천방지마피")
first_names = list("건성현욱정민현주희진영래주동혜도모영진선재현호시우인성마무병별솔하라")

alphas = list("abcdefghijklmnopqrstuvwxyz" * 3)

m30 = [4,6,9,11]

years = list(range(70, 99))
monthes = list(range(1, 13))
days = list(range(1, 32))
days30 = list(range(1, 31))
days28 = list(range(1, 29))


def make_birth():
    y = random.choice(years)
    m = random.choice(monthes)
    d = random.choice(days)
    if m in m30 and d > 30:
        d = random.choice(days30)
    elif m == 2 and d > 28:
        d = random.choice(days28)
    
    return "{}{:02d}{:02d}".format(y, m, d)

def ar(n=5):
    return "".join(random.sample(alphas, n))


def make_data():
    sung = random.choice(fam_names)
    name = "".join(random.sample(first_names, 2))
    email = "{}@gmail.com".format(ar(random.randrange(3,9)))
    pw = "a"
    birth = make_birth()
    gender = round(random.random())
    return (sung + name, email, birth, gender, pw)


data = []
for i in range(0, 1000):
    data.append(make_data())

print(data)


def save():
    try:
        conn = get_conn()
        conn.autocommit = False
        cur = conn.cursor()

        sql1 = "truncate table Patients"
        sql = "insert into Patients(name, email, birth, gender, password) values(%s,%s,%s,%s,%s) on duplicate key update email = email"
        cur.execute(sql1)
        cur.executemany(sql, data)
        print("AffecedRowCount is", cur.rowcount)
        conn.commit()

        print("Affected RowCount is", cur.rowcount, "/")


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


save()






