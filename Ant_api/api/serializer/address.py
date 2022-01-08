import datetime
from math import floor, ceil
import collections
from django.conf import settings

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models
from utils.randomName import getNameAvatarlist,getMosaic,getRandomName,getRandomAvatar

class GetAddressDetailModelSerializer(ModelSerializer):
    is_focused = serializers.SerializerMethodField()

    class Meta:
        model = models.Address
        fields = ["id","address","addressName","is_focused"]

    def get_is_focused(self,obj):
        request = self.context.get("request")
        if not request.user:
            return False
        addressfavor_object = models.AddressFocusRecord.objects.filter(user=request.user,address=obj)
        exists = addressfavor_object.exists()
        if exists:
            return True
        return False

class FocusAddressModelSerializer(ModelSerializer):
    class Meta:
        model = models.AddressFocusRecord
        fields = ["address"]

class GetAddressMomentModelSerializer(ModelSerializer):
    moment_list = serializers.SerializerMethodField()

    class Meta:
        model = models.AddressGeohash
        fields=["moment_list"]

    def get_moment_list(self,obj):
        address_query = models.Address.objects.filter(addressGeo=obj).order_by('-id')
        address_query = address_query.values(
            "moment_id",
            "moment__user",
            "moment__user__nickName",
            "moment__user__avatarUrl",
            "moment__create_date",
            "moment__content",
            "moment__favor_count",
            "moment__viewer_count",
            "moment__comment_count",
            "moment__share_count",
            "moment__if_status",
            "moment__moment_status"
        )
        request = self.context.get("request")
        moment = {}
        moment_list = collections.OrderedDict()
        for item in address_query:
            moment["id"] = item["moment_id"]
            #user
            '''
            if item["moment__if_status"]:
                nickName = getRandomName()
                avatarUrl = getMosaic()
                if_status_name = '条'
                user_id = None
                if obj.favor_count > settings.MAX_FAVOR_COUNT_IF_STATUS:
                    user_id = item["moment__user"]
                    if_status_name = "裂"
                if obj.comment_count > settings.MAX_COMMENT_COUNT_IF_STATUS:
                    user_id = item["moment__user"]
                    if_status_name = "裂"
                moment["user"]={"id": user_id, "nickName": nickName, "avatarUrl": avatarUrl, "if_status_name": if_status_name}
            else:
                moment["user"]={"id": item["moment__user"], "nickName": item["moment__user__nickName"], "avatarUrl": item["moment__user__avatarUrl"],
                    "if_status_name": None}
            '''
            moment["user"] = item["moment__user"]
            moment["create_date"]=item["moment__create_date"]
            moment["content"]=item["moment__content"]
            moment["favor_count"] = item["moment__favor_count"]
            moment["viewer_count"] = item["moment__viewer_count"]
            moment["comment_count"] = item["moment__comment_count"]
            moment["share_count"] = item["moment__share_count"]
            moment["if_status"] = item["moment__if_status"]
            moment["moment_status"] = item["moment__moment_status"]
            moment_list[item["moment_id"]]=moment
        return moment_list.values()

