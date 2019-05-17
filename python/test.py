from datetime import datetime, timedelta, timezone

l = "2019-03-01 07:28:00"

ll = datetime.strptime(l,"%Y-%m-%d %H:%M:%S")
# lll = ll.timestamp * 1000
lll = ll.timestamp() * 1000
result = (timedelta(days=1) * 1000).total_seconds()
# lll *= 1000

print(l, type(l))
print(ll, type(ll))
print(lll, type(lll))
print(result, type(result))


a = ll.astimezone(tz=utc_timezone)
print(a)