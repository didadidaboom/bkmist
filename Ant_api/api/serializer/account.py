from rest_framework import serializers
from django_redis import get_redis_connection
from rest_framework.exceptions import ValidationError
from django.forms import Form

from .validators import phone_validator

class MessageSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", validators=[phone_validator,])

class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField(label="手机号", validators=[phone_validator,])
    code = serializers.CharField(label="验证码")
    nickName = serializers.CharField(label="用户名")
    avatarUrl = serializers.CharField(label="用户头像")

    def validate_code(self, value):
        if(len(value)!=4):
            raise ValidationError("验证码格式错误")
        if(not value.isdecimal()):
            raise ValidationError("验证码非整数")
        phone = self.initial_data.get("phone")
        conn = get_redis_connection()
        code = conn.get(phone)
        if not code:
            raise ValidationError("验证码过期")
        if(value !=code.decode('utf-8')):
            raise ValidationError("验证码错误")
        return value