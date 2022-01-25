from math import ceil,floor
from django.conf import settings

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models
from utils.randomName import getRandomName,getMosaic

class GetNotificationFlagModelSerializer(ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ["userHasChecked"]

class GetNotificationModelSerializer(ModelSerializer):
    '''首页第一次加载时 瞬间的序列化器'''
    fromUser = serializers.SerializerMethodField()
    create_time = serializers.SerializerMethodField()
    moment_id = serializers.IntegerField(source='moment.id',read_only=True)
    tacit_id = serializers.IntegerField(source='tacit.id',read_only=True)
    tacit_user_id = serializers.IntegerField(source="tacit.user.id",read_only=True)
    comment_content = serializers.CharField(source="comment.content",read_only=True)

    class Meta:
        model = models.Notification
        fields = ["id","notificationType","fromUser","userHasChecked","create_time","moment_id","tacit_id","tacit_user_id","comment_content"]
        #fields="__all__"
        #fields = ["id","content","topic","address","user","create_date","imageList"]

    def get_fromUser(self,obj):
        request = self.context.get("request")
        if obj.notificationType is 21 or obj.notificationType is 22 or obj.notificationType is 23:
            if obj.comment.comment_status:
                nickName = obj.comment.nickName
                avatarUrl = getMosaic()
                if_status_name = '条'
                user_id = None
                if obj.comment.favor_count > settings.MAX_FAVOR_COUNT_IF_STATUS:
                    user_id = obj.comment.user.id
                    if_status_name = "裂"
                if obj.comment.user.id is request.user.id:
                    nickName = nickName + "(我)"
                return {"id": user_id, "nickName": nickName, "avatarUrl": avatarUrl, "if_status_name": if_status_name}
            nickName = obj.comment.nickName
            avatarUrl = obj.comment.avatarUrl
            if obj.comment.user.id is request.user.id:
                nickName = nickName + "(我)"
            return {"id": obj.comment.user.id, "nickName": nickName, "avatarUrl": avatarUrl, "if_status_name": None}
        else:
            return {"id": obj.toUser.id, "nickName": obj.toUser.nickName, "avatarUrl": obj.toUser.avatarUrl, "if_status_name": None}

    def get_create_time(self,obj):
        create_time = obj.create_time
        a = create_time
        b = create_time.now()
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

class ViewerNotificationModelSerializer(ModelSerializer):

    class Meta:
        model = models.ViewerNotification
        fields = ["id","focused_count","viewer_count_page1","viewer_count_page2","viewer_count_page3","tacit_viewer_count","tacit_write_count"]


class MomentViewerNotificationModelSerializer(ModelSerializer):
    class Meta:
        model = models.MomentViewerNotification
        fields = ["id", "momentviewer_count"]

class GetSystemNotificationFlagModelSerializer(ModelSerializer):
    class Meta:
        model = models.SystemNotification
        fields = ["userHasChecked"]

class GetSystemNotificationModelSerializer(ModelSerializer):
    class Meta:
        model = models.SystemNotification
        fields=["id","type","content","userHasChecked"]
