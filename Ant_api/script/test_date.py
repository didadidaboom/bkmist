import os
import sys
import django
import time
import datetime
from datetime import timezone
from math import floor,ceil



base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE","Ant_api.settings")
django.setup()

from api import models

def getDate():
    obj = models.Moment.objects.get(id=52)
    a = obj.create_date
    #b = obj.create_date.now(timezone.utc)
    b = obj.create_date.now()
    c = datetime.datetime.now()
    delta = b-a
    second = delta.seconds
    minute_ori = second/60
    minute_ceil = ceil(minute_ori)
    minute_floor = floor(minute_ori)
    hour_ori = minute_ori/60
    hour_ceil = ceil(hour_ori)
    hour_floor = floor(hour_ori)
    day_ori = delta.days
    day = day_ori+1

    print(a)
    print(b)
    print(c)
    print(delta)
    print(delta.seconds)
    print("minute")
    print(minute_ori)
    print(minute_ceil)
    print(minute_floor)
    print("hour")
    print(hour_ori)
    print(hour_ceil)
    print(hour_floor)
    print("day")
    print(day_ori)
    print(day)
    if(day_ori):
        return str(day)+"天内"
    else:
        if(hour_ori>1):
            return str(hour_ceil)+"小时内"
        else:
            if(minute_ori>1):
                return str(minute_ceil)+"分内"
            else:
                return str(second)+"秒内"

if __name__ =="__main__":
    ss = getDate()
    print(ss)
    print(datetime.datetime.now())
    from django.utils import timezone
    print(timezone.now())