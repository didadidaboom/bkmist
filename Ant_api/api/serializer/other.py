from math import floor,ceil

from rest_framework import serializers

from api import models

class OtherDetailsModelSerializer(serializers.ModelSerializer):
    is_focused = serializers.SerializerMethodField(read_only=True)
    create_date = serializers.SerializerMethodField()
    class Meta:
        model = models.UserInfo
        #fields = "__all__"
        exclude = ("openID","phone","token")

    def get_is_focused(self,obj):
        request = self.context.get("request")
        if not request.user:
            return False
        userfocus_obj = models.UserFocusRecord.objects.filter(user=obj, focus_user=request.user)
        exists = userfocus_obj.exists()
        if exists:
            return True
        return False
    def get_create_date(self,obj):
        create_date = obj.create_date
        a = create_date
        b = create_date.now()
        delta = b - a
        day_ori = delta.days
        return day_ori

class FocusUserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserFocusRecord
        fields = ["user"]

class OtherInviteTacitsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Notification
        fields = ["toUser","notificationType","userHasChecked"]

