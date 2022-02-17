from math import ceil,floor

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models

class getDayOpenidUsedListModelSerializer(ModelSerializer):
    last_login = serializers.SerializerMethodField()
    create_date = serializers.SerializerMethodField()

    class Meta:
        model = models.UserInfo
        fields=["id","nickName","openID","last_login","create_date"]

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
        day = day_ori
        if (day_ori):
            return str(day) + "天前"
        else:
            if (hour_ori > 1):
                return str(hour_floor) + "小时前"
            else:
                if (minute_ori > 1):
                    return str(minute_floor) + "分钟前"
                else:
                    return str(second) + "秒前"

    def get_create_date(self,obj):
        create_date = obj.create_date
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
        day = day_ori
        if (day_ori):
            return str(day) + "天前"
        else:
            if (hour_ori > 1):
                return str(hour_floor) + "小时前"
            else:
                if (minute_ori > 1):
                    return str(minute_floor) + "分钟前"
                else:
                    return str(second) + "秒前"

class getPersonalDataModelSerializer(ModelSerializer):
    nickName = serializers.CharField(source="curUser.nickName")
    latest_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.PersonalData
        fields = ["nickName", "type", "count", "latest_time"]
        # fields = "__all__"

    def get_latest_time(self,obj):
        create_date = obj.latest_time
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
        day = day_ori
        if (day_ori):
            return str(day) + "天前"
        else:
            if (hour_ori > 1):
                return str(hour_floor) + "小时前"
            else:
                if (minute_ori > 1):
                    return str(minute_floor) + "分钟前"
                else:
                    return str(second) + "秒前"

class getPageDataViewModelSerializer(ModelSerializer):
    nickName = serializers.CharField(source="curUser.nickName")
    latest_time = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.PagesData
        fields = ["nickName","type","count","latest_time"]
        # fields = "__all__"

    def get_latest_time(self,obj):
        create_date = obj.latest_time
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
        day = day_ori
        if (day_ori):
            return str(day) + "天前"
        else:
            if (hour_ori > 1):
                return str(hour_floor) + "小时前"
            else:
                if (minute_ori > 1):
                    return str(minute_floor) + "分钟前"
                else:
                    return str(second) + "秒前"



