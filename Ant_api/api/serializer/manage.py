from rest_framework.serializers import ModelSerializer

from api import models

class getAllOpenidUsedListModelSerializer(ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields=["id","real_nickName","openID"]

class UpdateopenidModelSerializer(ModelSerializer):
    class Meta:
        model = models.UserInfo
        fields=["openID"]