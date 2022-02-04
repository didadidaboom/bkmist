from math import floor,ceil

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.conf import settings

from api import models

class CreateAskAnythingModelSerializer(ModelSerializer):
    user_id = serializers.IntegerField(source="user.id",read_only=True)

    class Meta:
        model = models.TacitRecord
        fields = ["id","type","user_id"]

class SubmitAskAnythingModelSerializer(ModelSerializer):
    # user_id = serializers.IntegerField(source="user.id",read_only=True)
    #user__nickName = serializers.CharField(source="nickName" ,read_only=True)
    #user__avatarUrl = serializers.CharField(source="avatarUrl",read_only=True)
    #user__nickName = serializers.SerializerMethodField(read_only=True)
    #user__avatarUrl = serializers.SerializerMethodField(read_only=True)
    reply_id = serializers.IntegerField(source="reply.id",read_only=True)
    reply__user_id = serializers.IntegerField(source="reply.user.id",read_only=True)
    #reply__nickName = serializers.CharField(source="reply.nickName",read_only=True)
    reply__nickName = serializers.SerializerMethodField(read_only=True)
    #create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"),read_only=True)
    create_date = serializers.SerializerMethodField()
    root_id = serializers.IntegerField(source="root.id",read_only=True)
    favor_count = serializers.IntegerField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)
    nickName = serializers.SerializerMethodField()

    class Meta:
        model = models.AskAnythingRecord
        exclude = ["user"]

    def get_nickName(self,obj):
        request = self.context.get("request")
        if obj.user.id == request.user.id:
            return obj.nickName+'(我)'
        return obj.nickName

    def get_reply__nickName(self,obj):
        request = self.context.get("request")
        if not obj.reply:
            return None
        if obj.reply.user.id == request.user.id:
            return obj.reply.nickName+('(我)')
        return obj.reply.nickName

    def get_status(self, obj):
        '''
        1.判断评论者是否为瞬间发布本人：如果不是评论区状态显示 根据评论状态而定
        2.如果是本人，判断瞬间发布的状态
        3.如果状态为公开0，评论区状态显示 根据评论状态而定
        4.如果状态为条件隐身，评论区状态根据瞬间状态而定，如果瞬间受欢迎达到上线，评论区楼主状态 根据评论状态而定
        '''
        if obj.tacitrecord.user.id != obj.user.id:
            if obj.comment_status==0:
                return {"comment_status_user_id":obj.user.id,"comment_status_user_real_avatarUrl":obj.user.real_avatarUrl,"comment_status_name":None}
            if obj.favor_count < settings.MAX_FAVOR_COUNT_IF_STATUS_COMMENT:
                return {"comment_status_user_id":None,"comment_status_user_real_avatarUrl":None,"comment_status_name":"条"}
            return {"comment_status_user_id":obj.user.id,"comment_status_user_real_avatarUrl":obj.avatarUrl,"comment_status_name":"裂"}
        else:
            return {"comment_status_user_id": obj.user.id,"comment_status_user_real_avatarUrl":obj.user.real_avatarUrl,"comment_status_name": None}

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

class AskMeAnythingDetailModelSerializer(ModelSerializer):
    user_id = serializers.IntegerField(source="user.id",read_only=True)
    real_avatarUrl = serializers.CharField(source="user.real_avatarUrl",read_only=True)
    real_nickName = serializers.CharField(source="user.real_nickName",read_only=True)
    create_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.TacitRecord
        fields = ["user_id","real_avatarUrl","real_nickName","create_date"]

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

class AskMeAnythingCommentModelSerializer(ModelSerializer):
    user_id = serializers.IntegerField(source="user.id",read_only=True)
    user__real_avatarUrl = serializers.CharField(source="user.real_avatarUrl",read_only=True)
    #user__nickName = serializers.SerializerMethodField(read_only=True)
    #user__avatarUrl = serializers.SerializerMethodField(read_only=True)
    reply_id = serializers.IntegerField(source="reply.id",read_only=True)
    reply__user_id = serializers.IntegerField(source="reply.user.id",read_only=True)
    reply__nickName = serializers.CharField(source="reply.nickName",read_only=True)
    #create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"),read_only=True)
    create_date = serializers.SerializerMethodField()
    root_id = serializers.IntegerField(source="root.id",read_only=True)
    favor_count = serializers.IntegerField(read_only=True)
    is_favor = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField(read_only=True)
    reply_comment = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.AskAnythingRecord
        exclude = ["user"]

    def get_reply_comment(self,obj):
        reply_obj_ori = models.AskAnythingRecord.objects.filter(root_id=obj.id)
        exist = reply_obj_ori.exists()
        if not exist:
            return None
        else:
            reply_obj = reply_obj_ori.first()
            content = reply_obj.content
            create_date = reply_obj.create_date
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
                 tmp_create_date = str(day) + "天前"
            else:
                if (hour_ori > 1):
                    tmp_create_date = str(hour_floor) + "小时前"
                else:
                    if (minute_ori > 1):
                        tmp_create_date = str(minute_floor) + "分钟前"
                    else:
                        tmp_create_date = str(second) + "秒前"
            return {"content":content,"create_date":tmp_create_date}

    def get_status(self, obj):
        '''
        1.判断评论者是否为瞬间发布本人：如果不是评论区状态显示 根据评论状态而定
        2.如果是本人，判断瞬间发布的状态
        3.如果状态为公开0，评论区状态显示 根据评论状态而定
        4.如果状态为条件隐身，评论区状态根据瞬间状态而定，如果瞬间受欢迎达到上线，评论区楼主状态 根据评论状态而定
        '''
        if obj.tacitrecord.user.id != obj.user.id:
            if obj.comment_status == 0:
                return {"comment_status_user_id": obj.user.id, "comment_status_name": None}
            if obj.favor_count < settings.MAX_FAVOR_COUNT_IF_STATUS_COMMENT:
                return {"comment_status_user_id": None, "comment_status_name": "条"}
            return {"comment_status_user_id": obj.user.id, "comment_status_name": "裂"}
        else:
            return {"comment_status_user_id": obj.user.id, "comment_status_name": None}

    def get_is_favor(self,obj):
        request = self.context.get("request")
        if not request.user:
            return False
        askanythingfavor_object = models.AskAnythingFavorRecord.objects.filter(user=request.user,askanythingrecord=obj)
        exists = askanythingfavor_object.exists()
        if exists:
            return True
        return False

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
