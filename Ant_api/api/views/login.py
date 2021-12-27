import json
import uuid
import requests
import base64

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from api import models
from api.serializer.loginOpenid import LoginOpenidwithPhone,LoginOpenidwithoutPhone,LoginOpenidModelSerializer
from utils.randomName import getNameAvatarlist,getRegisterNameAvatarlist

class LoginOpenidView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        1.确定有没有手机号
        2.如果有手机号 验证手机号
        3.通过code 换取openid
        4.产生token
        5.存入手机号,openid,token
        6.返回token
        '''
        return Response({"status":True,"message":"发送成功"})
    def post(self, request, *args, **kwargs):
        '''
        1.通过code 换取openid
        2.产生随机名字，头像和token
        3.存入手机号,openid,token
        4.确定有没有手机号
        5.如果有手机号 验证手机号
        6.返回token
        '''
        code = request.data.get("code")
        phone = request.data.get("phone")
        real_avatarUrl = request.data.get("real_avatarUrl")
        real_nickName = request.data.get("real_nickName")
        data = {
            "appid": settings.TENCENT_APPID,
            "secret": settings.TENCENT_APPSECRET,
            "js_code": code,
            "grant_type":"authorization_code"
        }
        #jointdata = "&".join(["{}={}".format(k,value) for k,value in data.items()])
        url = "https://api.weixin.qq.com/sns/jscode2session?"
        results = requests.get(url,params=data)
        openid = results.json().get("openid")
        nickName, avatarUrl = getRegisterNameAvatarlist()
        userobj = models.UserInfo.objects.filter(openID=openid).first()
        exists = models.UserInfo.objects.filter(openID=openid).exists()
        if exists:
            ser = LoginOpenidModelSerializer(instance=userobj)
            return Response(ser.data,status=status.HTTP_200_OK)
        info = {
            "nickName": nickName,
            "avatarUrl": avatarUrl,
            "openID": openid,
            "real_nickName":real_nickName,
            "real_avatarUrl":real_avatarUrl
        }
        if not phone:
            ser = LoginOpenidwithoutPhone(data=info)
            if not ser.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            print("no phone")
            phone = ser.validated_data.get("phone")
            nickName = ser.validated_data.get("nickName")
            avatarUrl = ser.validated_data.get("avatarUrl")
            real_nickName = ser.validated_data.get("real_nickName")
            real_avatarUrl = ser.validated_data.get("real_avatarUrl")
            user_object, flag = models.UserInfo.objects.get_or_create(**ser.validated_data)
            user_object.token = str(uuid.uuid4())
            user_object.save()
            return Response({
                "nickName": nickName,
                "avatarUrl":avatarUrl,
                "token": user_object.token,
                "real_nickName": real_nickName,
                "real_avatarUrl": real_avatarUrl
            },status=status.HTTP_200_OK)
        info["phone"] = phone
        ser = LoginOpenidwithPhone(data=info)
        if not ser.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        phone = ser.validated_data.get("phone")
        nickName = ser.validated_data.get("nickName")
        avatarUrl = ser.validated_data.get("avatarUrl")
        real_nickName = ser.validated_data.get("real_nickName")
        real_avatarUrl = ser.validated_data.get("real_avatarUrl")
        user_object, flag = models.UserInfo.objects.get_or_create(**ser.validated_data)
        user_object.token = str(uuid.uuid4())
        user_object.save()
        print("with phone")
        return Response({
            "nickName": nickName,
            "avatarUrl":avatarUrl,
            "token": user_object.token,
            "real_nickName":real_nickName,
            "real_avatarUrl":real_avatarUrl
        },status=status.HTTP_200_OK)


class getAccessView(APIView):
    def get(self, request, *args, **kwargs):
        tacitid = request.query_params.get("tacitid")
        data = {
            "grant_type": "client_credential",
            "appid": settings.TENCENT_APPID,
            "secret": settings.TENCENT_APPSECRET,
        }
        url = "https://api.weixin.qq.com/cgi-bin/token?"
        results = requests.get(url, params=data)
        results_json = results.json()
        if results_json is 40013:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        data_code = {
            "scene":tacitid,
            "page":"pages/replyTacit/replyTacit",
            "width":280,
            "is_hyaline":True
        }
        url_code = "https://api.weixin.qq.com/wxa/getwxacodeunlimit?access_token="+results_json.get("access_token")
        header = {
            "content-Type":"application/json;charset=UTF-8"
        }
        results_code = requests.post(url_code,data=json.dumps(data_code),headers=header)
        base64_result = base64.b64encode(results_code.content)
        return Response({"base64_buffer":base64_result},status=status.HTTP_200_OK)
