from rest_framework import serializers
from api import models
from api.serializer.validators import phone_validator

class LoginOpenidwithPhone(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    phone = serializers.CharField(label="手机号", validators=[phone_validator,])
    class Meta:
        model = models.UserInfo
        fields = ["nickName","avatarUrl","openID","token","phone","real_nickName","real_avatarUrl"]



class LoginOpenidwithoutPhone(serializers.ModelSerializer):
    token = serializers.CharField(read_only=True)
    class Meta:
        model = models.UserInfo
        fields = ["nickName","avatarUrl","openID","token","real_nickName","real_avatarUrl"]

class LoginOpenidModelSerializer(serializers.ModelSerializer):
    nickName = serializers.CharField(read_only=True)
    avatarUrl = serializers.CharField(read_only=True)
    token = serializers.CharField(read_only=True)

    class Meta:
        model = models.UserInfo
        fields = ["nickName","avatarUrl","openID","token","real_nickName","real_avatarUrl"]