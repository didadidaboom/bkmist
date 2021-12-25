from rest_framework.serializers import ModelSerializer
from api.models import TopicInfo

class TopicSerializer(ModelSerializer):
    """话题数据序列化器"""
    class Meta:
        model = TopicInfo
        fields = '__all__'
        extra_kwargs = {
            'title':{'required':True}
        }