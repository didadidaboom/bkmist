from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from api import models
from api.models import TopicInfo

class TopicSerializer(ModelSerializer):
    """话题数据序列化器"""
    class Meta:
        model = TopicInfo
        fields=["id","title","description"]
        #fields = '__all__'
        extra_kwargs = {
            'title':{'required':True}
        }

class GetTopicDetailModelSerializer(ModelSerializer):
    #user = serializers.SerializerMethodField()
    is_focused = serializers.SerializerMethodField()

    class Meta:
        model = TopicInfo
        fields = ["id","title","focus_count","viewer_count","cited_count","create_date","is_focused"]

    # def get_user(self,obj):
    #     return {"id":obj.user.id,"nickName":obj.user.nickName,"avatarUrl":obj.user.avatarUrl}

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

class FocusMomentTopicModelSerializer(serializers.ModelSerializer):
    topic_id = serializers.SerializerMethodField(read_only=True)
    topic_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.TopicFocusRecord
        fields = ["topic_id","topic_title"]
    def get_topic_id(self,obj):
        return obj.topic.id
    def get_topic_title(self,obj):
        return obj.topic.title

