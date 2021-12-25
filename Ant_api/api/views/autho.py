import uuid
import random

from django_redis import get_redis_connection
from  rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings

from api.serializer.account import MessageSerializer, LoginSerializer
from api import models
from sts.sts import Sts
from utils.tencent.msg import send_message

class MessageCodeView(APIView):
    '''
    #1, 获取手机号
    #2, 验证手机号
    #3, 生成随机验证码
    #4, 发送短信  购买服务器进行短信服务：阿里云/腾讯云
    #5, 保留验证码+手机号(30秒过期)
        #   5.1. 搭建 redis服务器（或者云redis）
        # conn.set('12333333333','12345',ex=30)
    '''
    def get(self, request, *args, **kwargs):
        ser = MessageSerializer(data=request.query_params)
        if(not ser.is_valid()):
            return Response({"status": False, "message": "手机格式错误"})
        phone = ser.validated_data.get("phone")
        #3, 生成随机验证码
        random_code = random.randint(1000,9999)
        print(random_code)
        #4, 发送短信  购买服务器进行短信服务：阿里云/腾讯云
        '''
        result = send_message(phone, random_code)
        if(not result):
            Response({"status": False, "message": "发送失败"})
        '''
        #5, 保留验证码+手机号(30秒过期)
        #   5.1. 搭建 redis服务器（或者云redis）
        # conn.set('12333333333','12345',ex=30)
        conn = get_redis_connection()
        conn.set(phone, random_code, ex=30)
        return Response({"status": True, "message": "发送成功"})

class LoginView(APIView):
    '''
    1. 手机号验证
    2. 验证码验证
        无验证码，不成功
        有验证码，不成功
        有验证码，成功
    3. 数据库中获取或者创建用户信息
    4. 返回信息
    '''
    def post(self, request, *args, **kwargs):
        ser = LoginSerializer(data=request.data)
        if(not ser.is_valid()):
            return Response({"status": False, "message": "验证码错误"})
        phone = ser.validated_data.get("phone")
        nickName = ser.validated_data.get("nickName")
        avatarUrl = ser.validated_data.get("avatarUrl")
        #delet user info
        #models.UserInfo.objects.filter(phone=phone).delete()
        user_object, flag = models.UserInfo.objects.get_or_create(
            phone=phone,
            defaults={
                "nickName":nickName,
                "avatarUrl":avatarUrl
            })
        user_object.token = str(uuid.uuid4())
        user_object.save()
        return Response({"status": True, "data":{"phone": phone, "token": user_object.token}})

class CredentialView(APIView):
    '''
    获取临时密钥
    '''
    def get(selfs, *args, **kwargs):
        try:
            sts = Sts(settings.TENCENT_FILE_CONFIG)
            response = sts.get_credential()
            return Response(response)
        except Exception as e:
            print(e)