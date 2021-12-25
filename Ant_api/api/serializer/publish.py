from rest_framework import serializers

from api.models import MomentDetail,Moment
from api.serializer.MomentDetail import MomentDetailSerializer

class PublishSerializer(serializers.ModelSerializer):
    """瞬间发布的序列化器"""
    imageList = MomentDetailSerializer(many=True)


    class Meta:
        model = Moment
        fields = ["id","address","addressName","latitude","longitude","content","if_status","moment_status","imageList"]
        extra_kwargs = {
            'content':{'required':True}
        }

    def create(self, validated_data):
        imageList_data = validated_data.pop("imageList")
        moment = Moment.objects.create(**validated_data)
        data_list = MomentDetail.objects.bulk_create([MomentDetail(**info,moment=moment) for info in imageList_data])
        moment.imageList = data_list
        return moment

class PublishSerializerWithoutFig(serializers.ModelSerializer):
    """瞬间发布的序列化器"""
    class Meta:
        model = Moment
        fields = ["id","content","if_status","moment_status"]
        extra_kwargs = {
            'content':{'required':True}
        }