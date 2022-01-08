from rest_framework import serializers
from django.forms.models import model_to_dict

from api import models
from api.serializer.MomentDetail import MomentDetailSerializer

class PersonalMomentModelSerializer(serializers.ModelSerializer):
    imageList = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    address = serializers.SerializerMethodField()
    class Meta:
        model = models.Moment
        fields = ["id","content","create_date","imageList","address","topic","if_status","moment_status"]

    def get_address(self, obj):
        exist = models.Address.objects.filter(moment=obj).exists()
        if not exist:
            return None
        address_obj = models.Address.objects.filter(moment=obj).first()
        if address_obj.addressName:
            address = address_obj.addressName
        elif address_obj.address:
            address = address_obj.address
        else:
            address = None
            return None
        return {"id": address_obj.id, "name": address}

    def get_topic(self,obj):
        exist = models.TopicCitedRecord.objects.filter(moment=obj).exists()
        if not exist:
            return {}
        topic_obj = models.TopicCitedRecord.objects.filter(moment=obj).all()
        return [model_to_dict(row.topic,fields=['id','title']) for row in topic_obj]

    def get_imageList(self,obj):
        current_obj = models.MomentDetail.objects.filter(moment=obj).all()
        return [model_to_dict(row,["id","path"]) for row in current_obj]

class UpdatePersonalMomentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Moment
        fields = "__all__"

