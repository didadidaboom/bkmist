from rest_framework.serializers import ModelSerializer

from api import models

class SystemmessageModelSerializer(ModelSerializer):
    class Meta:
        model = models.PreSystem
        fields=["type","content"]

    def create(self, validated_data):
        type = validated_data.get('type', None)
        content = validated_data.get("content",None)
        obj_ori = models.PreSystem.objects.filter(type=type)
        if obj_ori.exists():
            obj = obj_ori.update(content=content)
            return obj
        else:
            obj = obj_ori.create(type=type,content=content)
            return obj