from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api import models
from api.models import TopicInfo

class TopicSerializer(ModelSerializer):
    """话题数据序列化器"""
    class Meta:
        model = TopicInfo
        fields = '__all__'
        extra_kwargs = {
            'title':{'required':True}
        }

class GetTopicDetailModelSerializer(ModelSerializer):
    user = serializers.SerializerMethodField()
    is_focused = serializers.SerializerMethodField()

    class Meta:
        model = TopicInfo
        fields = '__all__'

    def get_user(self,obj):
        return {"id":obj.user.id,"nickName":obj.user.nickName,"avatarUrl":obj.user.avatarUrl}

    def get_is_focused(self,obj):
        request = self.context.get("request")
        if not request.user:
            return False
        topicfavor_object = models.TopicFocusRecord.objects.filter(user=request.user,topic=obj)
        exists = topicfavor_object.exists()
        if exists:
            return True
        return False

class FocusTopicModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TopicFocusRecord
        fields = ["topic"]
