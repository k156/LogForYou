from datetime import datetime, timedelta, timezone, time

# l = "2019-03-01 07:28:00"

# ll = datetime.strptime(l,"%Y-%m-%d %H:%M:%S")
# print(ll.tzinfo)

# print("--------")
# print(datetime.utcnow())
# print(datetime.now())

# # lll = ll.timestamp * 1000
# lll = ll.timestamp() * 1000
# result = (timedelta(days=1) * 1000).total_seconds()
# # lll *= 1000

# print(l, type(l))
# print(ll, type(ll))
# print(lll, type(lll))
# print(result, type(result))

# l = "07:00"
# ll = datetime(2017, 11, 14)
# m, v = l.split(":")
# print(int(m), int(v))
import random

d = random.randrange(1, 20)
c = d if d < 10 else d * 2
print(">>>>>>>> ", c)


