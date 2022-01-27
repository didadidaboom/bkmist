from math import ceil,floor

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models

class getAllOpenidUsedListModelSerializer(ModelSerializer):
    last_login = serializers.SerializerMethodField()
    class Meta:
        model = models.UserInfo
        fields=["id","real_nickName","openID","last_login"]

    def get_last_login(self,obj):
        create_date = obj.last_login
        a = create_date
        b = create_date.now()
        delta = b - a
        second = delta.seconds
        minute_ori = second / 60
        minute_ceil = ceil(minute_ori)
        minute_floor = floor(minute_ori)
        hour_ori = minute_ori / 60
        hour_ceil = ceil(hour_ori)
        hour_floor = floor(hour_ori)
        day_ori = delta.days
        day = day_ori + 1
        if (day_ori):
            return str(day) + "天前"
        else:
            if (hour_ori > 1):
                return str(hour_ceil) + "小时前"
            else:
                if (minute_ori > 1):
                    return str(minute_ceil) + "分钟前"
                else:
                    return str(second) + "秒前"

class UpdateopenidModelSerializer(ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields=["openID"]