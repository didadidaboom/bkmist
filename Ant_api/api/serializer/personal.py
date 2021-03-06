from math import floor,ceil
from django.forms.models import model_to_dict

from rest_framework import serializers

from api import models

class PersonalInfoModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["focus_count","focused_count","viewer_count","create_date","viewer_count_page2","viewer_count_page3","tacit_viewer_count","tacit_write_count"]

    def get_create_date(self,obj):
        create_date = obj.create_date
        a = create_date
        b = create_date.now()
        delta = b - a
        day_ori = delta.days
        return day_ori

class UpdateNamePersonalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["nickName"]

class UpdateAvatarPersonalModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields = ["avatarUrl","gender"]

class PersonalViewerPage1ModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    viewer_user = serializers.SerializerMethodField()
    class Meta:
        model = models.UserViewerRecord
        #fields = "__all__"
        fields = ["viewer_user","viewer_count","create_date"]

    def get_viewer_user(self,obj):
        return model_to_dict(obj.viewer_user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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

class PersonalViewerPage2ModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    viewer_user = serializers.SerializerMethodField()
    class Meta:
        model = models.UserViewerRecordPage2
        #fields = "__all__"
        fields = ["viewer_user","viewer_count","create_date"]

    def get_viewer_user(self,obj):
        return model_to_dict(obj.viewer_user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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

class PersonalViewerPage3ModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    viewer_user = serializers.SerializerMethodField()
    class Meta:
        model = models.UserViewerRecordPage3
        #fields = "__all__"
        fields = ["viewer_user","viewer_count","create_date"]

    def get_viewer_user(self,obj):
        return model_to_dict(obj.viewer_user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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

class PersonalViewerPage3ScanModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    viewer_user = serializers.SerializerMethodField()
    class Meta:
        model = models.TacitReplyViewer
        #fields = "__all__"
        fields = ["viewer_user","viewer_count","create_date","source"]

    def get_viewer_user(self,obj):
        return model_to_dict(obj.viewer_user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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

class PersonalViewerPage3SubmitModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    viewer_user = serializers.SerializerMethodField()
    class Meta:
        model = models.TacitReplyWrite
        #fields = "__all__"
        fields = ["viewer_user","write_count","create_date","source"]

    def get_viewer_user(self,obj):
        return model_to_dict(obj.viewer_user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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

class PersonalMomentViewerViewModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    viewer_user = serializers.SerializerMethodField()
    class Meta:
        model = models.MomentViewerRecord
        #fields = "__all__"
        fields = ["viewer_user","viewer_count","create_date"]

    def get_viewer_user(self,obj):
        return model_to_dict(obj.viewer_user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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

class PersonalFocusListModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = models.UserFocusRecord
        #fields = "__all__"
        fields = ["user","create_date"]

    def get_user(self,obj):
        return model_to_dict(obj.user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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

class PersonalFocusedListModelSerializer(serializers.ModelSerializer):
    create_date = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    class Meta:
        model = models.UserFocusRecord
        #fields = "__all__"
        fields = ["user","create_date"]

    def get_user(self,obj):
        return model_to_dict(obj.focus_user, fields=['id', 'nickName', 'avatarUrl'])

    def get_create_date(self,obj):
        create_date = obj.create_time
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