import datetime
from math import floor, ceil
import collections
from django.conf import settings
from django.forms.models import model_to_dict

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

class FocusMomentAddressModelSerializer(ModelSerializer):
    address_id = serializers.SerializerMethodField(read_only=True)
    address_title = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.AddressFocusRecord
        fields = ["address_id","address_title"]
    def get_address_id(self,obj):
        return obj.address.id
    def get_address_title(self,obj):
        address = None
        if obj.address.addressName:
            address = obj.address.addressName
        elif obj.address.address:
            address = obj.address.address
        return address

class GetAddressMomentModelSerializer(ModelSerializer):
    moment_list = serializers.SerializerMethodField()

    class Meta:
        model = models.AddressGeohash
        fields=["moment_list"]

    def get_moment_list(self,obj):
        address_query = models.MomentCiteAddressRecord.objects.filter(address__addressGeo=obj).all().order_by("-id")
        address_query = address_query.values(
            "id",
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
            "moment__moment_status",
            "address_id",
            "address__address",
            "address__addressName"
        )
        request = self.context.get("request")
        moment_list = collections.OrderedDict()
        for item in address_query:
            moment = {}
            moment["id"] = item["moment_id"]
            #user
            if item["moment__if_status"]:
                nickName = getRandomName()
                avatarUrl = getMosaic()
                if_status_name = '条'
                user_id = None
                if item["moment__favor_count"] > settings.MAX_FAVOR_COUNT_IF_STATUS:
                    user_id = item["moment__user"]
                    if_status_name = "裂"
                moment["user"]={"id": user_id, "nickName": nickName, "avatarUrl": avatarUrl, "if_status_name": if_status_name}
            else:
                moment["user"]={"id": item["moment__user"],
                                "nickName": item["moment__user__nickName"],
                                "avatarUrl": item["moment__user__avatarUrl"],
                                "if_status_name": None}
            #topic
            topic_cite_obj_ori = models.TopicCitedRecord.objects.filter(moment=item["moment_id"])
            exist = topic_cite_obj_ori.exists()
            if not exist:
                moment["topic"] = {}
            else:
                topic_obj = topic_cite_obj_ori.all()
                moment["topic"] = [model_to_dict(row.topic, fields=['id', 'title']) for row in topic_obj]

            #imagelist
            query_details = models.MomentDetail.objects.filter(moment=item["moment_id"])
            moment["imageList"] = [model_to_dict(row, fields=["id", "path", "path_key"]) for row in query_details]

            #create date
            create_date = item["moment__create_date"]
            a = create_date
            b = create_date.now()
            delta = b - a
            second = delta.seconds
            minute_ori = second / 60
            minute_ceil = ceil(minute_ori)
            minute_floor = floor(minute_ori)
            hour_ori = minute_ori / 60
            hour_ceil = ceil(hour_ori)
            hour_floor = floor(hour_ori)
            day_ori = delta.days
            day = day_ori + 1
            if (day_ori):
                moment["create_date"] = str(day) + "天前"
            else:
                if (hour_ori > 1):
                    moment["create_date"] = str(hour_ceil) + "小时前"
                else:
                    if (minute_ori > 1):
                        moment["create_date"] = str(minute_ceil) + "分钟前"
                    else:
                        moment["create_date"] = str(second) + "秒前"

            #is_favor
            request = self.context.get("request")
            if not request.user:
                moment["is_favor"] = False
            else:
                momentfavor_object = models.MomentFavorRecord.objects.filter(user=request.user, moment=item["moment_id"])
                exists = momentfavor_object.exists()
                if exists:
                    moment["is_favor"] = True
                else:
                    moment["is_favor"] = False

            #address
            if item["address__addressName"]:
                address = item["address__addressName"]
                moment["address"] = {"id": item["address_id"], "name": address}
            elif item["address__address"]:
                address = item["address__address"]
                moment["address"] = {"id": item["address_id"], "name": address}
            else:
                address = None
                moment["address"] =  None

            moment["content"]=item["moment__content"]
            moment["favor_count"] = item["moment__favor_count"]
            moment["viewer_count"] = item["moment__viewer_count"]
            moment["comment_count"] = item["moment__comment_count"]
            moment["share_count"] = item["moment__share_count"]
            moment["if_status"] = item["moment__if_status"]
            moment["moment_status"] = item["moment__moment_status"]
            moment_list[item["moment_id"]]=moment
        return moment_list.values()

