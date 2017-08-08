import time
from datetime import datetime

print int(time.time())

timestamp = 1499904000
dt_obj = datetime.utcfromtimestamp(timestamp)
print repr(dt_obj)

timestamp = int(time.time())
dt_obj = datetime.utcfromtimestamp(timestamp)
print repr(dt_obj)
