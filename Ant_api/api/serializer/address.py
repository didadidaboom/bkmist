import datetime
from math import floor, ceil
import collections

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models

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
        #if not request.user:
        #    #moment_list = collections.OrderedDict()
        #    #for item in address_query:
        address_query["is_favor"] = False
        return address_query

