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
        address_query = models.Address.objects.filter(addressGeo=obj).order_by('-id')
        address_query = address_query.values(
            "momentciteaddressrecord__moment_id",
            "momentciteaddressrecord__moment__user_id",
            "momentciteaddressrecord__moment__create_date",
            "momentciteaddressrecord__moment__content",
            "momentciteaddressrecord__moment__favor_count",
            "momentciteaddressrecord__moment__viewer_count",
            "momentciteaddressrecord__moment__comment_count",
            "momentciteaddressrecord__moment__share_count",
            "momentciteaddressrecord__moment__if_status",
            "momentciteaddressrecord__moment__moment_status",
        )
        request = self.context.get("request")
        moment = {}
        moment_list = collections.OrderedDict()
        for item in address_query:
            moment["id"] = item["momentciteaddressrecord__moment_id"]
            #user
            if item["momentciteaddressrecord__moment__if_status"]:
                nickName = getRandomName()
                avatarUrl = getMosaic()
                if_status_name = '条'
                user_id = None
                if item["momentciteaddressrecord__moment__favor_count"] > settings.MAX_FAVOR_COUNT_IF_STATUS:
                    user_id = item["momentciteaddressrecord__moment__user_id"]
                    if_status_name = "裂"
                moment["user"]={"id": user_id, "nickName": nickName, "avatarUrl": avatarUrl, "if_status_name": if_status_name}
            else:
                
                moment["user"]={"id": item["momentciteaddressrecord__moment__user_id"],
                                "nickName": item["momentciteaddressrecord__moment__user__nickName"],
                                "avatarUrl": item["momentciteaddressrecord__moment__user__avatarUrl"],
                                "if_status_name": None}
            #topic
            topic_cite_obj_ori = models.TopicCitedRecord.objects.filter(moment=item["momentciteaddressrecord__moment_id"])
            exist = topic_cite_obj_ori.exists()
            if not exist:
                moment["topic"] = {}
            else:
                topic_obj = topic_cite_obj_ori.all()
                moment["topic"] = [model_to_dict(row.topic, fields=['id', 'title']) for row in topic_obj]

            #imagelist
            query_details = models.MomentDetail.objects.filter(moment=item["momentciteaddressrecord__moment_id"])
            moment["imageList"] = [model_to_dict(row, fields=["id", "path", "path_key"]) for row in query_details]

            #create date
            create_date = item["momentciteaddressrecord__moment__create_date"]
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
                momentfavor_object = models.MomentFavorRecord.objects.filter(user=request.user, moment=item["momentciteaddressrecord__moment_id"])
                exists = momentfavor_object.exists()
                if exists:
                    moment["is_favor"] = True
                else:
                    moment["is_favor"] = False

            #address
            m_a_obj_ori = models.MomentCiteAddressRecord.objects.filter(moment=item["momentciteaddressrecord__moment_id"])
            exist = m_a_obj_ori.exists()
            if not exist:
                moment["address"] = None
            else:
                m_a_obj = m_a_obj_ori.first()
                if m_a_obj.address.addressName:
                    address = m_a_obj.address.addressName
                    moment["address"] = {"id": m_a_obj.address.id, "name": address}
                elif m_a_obj.address.address:
                    address = m_a_obj.address.address
                    moment["address"] = {"id": m_a_obj.address.id, "name": address}
                else:
                    address = None
                    moment["address"] =  None

            moment["content"]=item["momentciteaddressrecord__moment__content"]
            moment["favor_count"] = item["momentciteaddressrecord__moment__favor_count"]
            moment["viewer_count"] = item["momentciteaddressrecord__moment__viewer_count"]
            moment["comment_count"] = item["momentciteaddressrecord__moment__comment_count"]
            moment["share_count"] = item["momentciteaddressrecord__moment__share_count"]
            moment["if_status"] = item["momentciteaddressrecord__moment__if_status"]
            moment["moment_status"] = item["momentciteaddressrecord__moment__moment_status"]
            moment_list[item["momentciteaddressrecord__moment_id"]]=moment
        return moment_list.values()

