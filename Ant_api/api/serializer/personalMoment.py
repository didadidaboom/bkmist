from rest_framework import serializers
from django.forms.models import model_to_dict

from api import models
from api.serializer.MomentDetail import MomentDetailSerializer

class PersonalMomentModelSerializer(serializers.ModelSerializer):
    imageList = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    address = serializers.SerializerMethodField()
    new_momentviewers = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Moment
        fields = ["id","content","create_date","imageList","address","topic","if_status","moment_status","new_momentviewers"]

    def get_address(self, obj):
        address_obj_ori = models.MomentCiteAddressRecord.objects.filter(moment=obj)
        exist = address_obj_ori.exists()
        if not exist:
            return None
        address_obj = address_obj_ori.first()
        if address_obj.address.addressName:
            address = address_obj.address.addressName
        elif address_obj.address.address:
            address = address_obj.address.address
        else:
            address = None
            return None
        return {"id": address_obj.address.id, "name": address}

    def get_topic(self,obj):
        exist = models.TopicCitedRecord.objects.filter(moment=obj).exists()
        if not exist:
            return {}
        topic_obj = models.TopicCitedRecord.objects.filter(moment=obj).all()
        return [model_to_dict(row.topic,fields=['id','title']) for row in topic_obj]

    def get_imageList(self,obj):
        current_obj = models.MomentDetail.objects.filter(moment=obj).all()
        return [model_to_dict(row,["id","path"]) for row in current_obj]

    def get_new_momentviewers(self,obj):
        momentviewer_obj = models.MomentViewerNotification.objects.filter(moment=obj).first()
        return momentviewer_obj.momentviewer_count

class UpdatePersonalMomentModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Moment
        fields = "__all__"

