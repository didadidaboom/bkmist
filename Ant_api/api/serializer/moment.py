import datetime
from math import floor, ceil
import collections

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from django.forms.models import model_to_dict
from django.conf import settings

from api.models import Moment,MomentDetail,MomentFavorRecord,TopicCitedRecord
from api import models
from api.serializer.MomentDetail import MomentDetailSerializer
from utils.randomName import getNameAvatarlist,getMosaic,getRandomName,getRandomAvatar

class MomentSerializer(ModelSerializer):
    """瞬间发布的序列化器"""
    imageList = MomentDetailSerializer(many=True)

    class Meta:
        model = Moment
        fields = '__all__'
        extra_kwargs = {
            'user':{'required':True},
            'content':{'required':True}
        }

    def create(self, validated_data):
        imageList_data = validated_data.pop("imageList")
        moment = Moment.objects.create(**validated_data)
        data_list = MomentDetail.objects.bulk_create([MomentDetail(**info,moment=moment) for info in imageList_data])

        moment.imageList = data_list
        return moment


class GetMomentModelSerializer(ModelSerializer):
    '''首页第一次加载时 瞬间的序列化器'''
    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    imageList = serializers.SerializerMethodField()
    #create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    create_date = serializers.SerializerMethodField()
    is_favor = serializers.SerializerMethodField(read_only=True)
    address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Moment
        fields="__all__"
        #fields = ["id","content","topic","address","user","create_date","imageList"]

    def get_address(self,obj):
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
        return {"id":address_obj.address.id,"name":address}

    def get_user(self,obj):
        if obj.if_status:
            nickName = getRandomName()
            avatarUrl = getMosaic()
            if_status_name ='条'
            user_id = None
            if obj.favor_count > settings.MAX_FAVOR_COUNT_IF_STATUS:
                user_id = obj.user.id
                if_status_name = "裂"
            return {"id":user_id,"nickName":nickName,"avatarUrl":avatarUrl,"if_status_name":if_status_name}
        return {"id":obj.user.id,"nickName":obj.user.nickName,"avatarUrl":obj.user.avatarUrl,"if_status_name":None}

    def get_topic(self,obj):
        exist = TopicCitedRecord.objects.filter(moment=obj).exists()
        if not exist:
            return {}
        topic_obj = TopicCitedRecord.objects.filter(moment=obj).all()
        return [model_to_dict(row.topic,fields=['id','title']) for row in topic_obj]

    def get_imageList(self,obj):
        query_details = MomentDetail.objects.filter(moment = obj)
        return [model_to_dict(row, fields=["id","path","path_key"]) for row in query_details]

    def get_is_favor(self,obj):
        request = self.context.get("request")
        if not request.user:
            return False
        momentfavor_object = models.MomentFavorRecord.objects.filter(user=request.user,moment=obj)
        exists = momentfavor_object.exists()
        if exists:
            return True
        return False
    def get_create_date(self,obj):
        create_date = obj.create_date
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
            return str(day) + "天前"
        else:
            if (hour_ori > 1):
                return str(hour_ceil) + "小时前"
            else:
                if (minute_ori > 1):
                    return str(minute_ceil) + "分钟前"
                else:
                    return str(second) + "秒前"

class GetMomentDetailModelSerializer(MomentSerializer):
    user = serializers.SerializerMethodField()
    topic = serializers.SerializerMethodField()
    imageList = serializers.SerializerMethodField()
    #create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    create_date = serializers.SerializerMethodField()
    #viewer = serializers.SerializerMethodField()
    comment = serializers.SerializerMethodField()
    is_favor = serializers.SerializerMethodField()
    address = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Moment
        fields = "__all__"

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

    def get_user(self,obj):
        #判断是否已经被关注
        request = self.context.get("request")
        is_focused = False
        if request.user:
            userfocus_object = models.UserFocusRecord.objects.filter(user=obj.user,focus_user= request.user)
            exists = userfocus_object.exists()
            if exists:
                is_focused = True
        #判断条件隐身
        if obj.if_status:
            nickName = getRandomName()
            avatarUrl = getMosaic()
            user_id = None
            if_status_name = '条'
            if obj.favor_count > settings.MAX_FAVOR_COUNT_IF_STATUS:
                user_id = obj.user.id
                if_status_name = "裂"
            if obj.user.id is request.user.id:
                nickName = nickName+"(我)"
            return {"id":user_id,"nickName":nickName,"avatarUrl":avatarUrl,"if_status_name":if_status_name,"is_focused":is_focused}
        nickName = obj.user.nickName
        avatarUrl = obj.user.avatarUrl
        if obj.user.id is request.user.id:
            nickName = nickName + "(我)"
        return {"id": obj.user.id, "nickName": nickName, "avatarUrl": avatarUrl,"if_status_name": None,"is_focused":is_focused}
        #return model_to_dict(obj.user, fields=['id', 'nickName', 'avatarUrl'])

    def get_topic(self,obj):
        exist = TopicCitedRecord.objects.filter(moment=obj).exists()
        if not exist:
            return {}
        topic_obj = TopicCitedRecord.objects.filter(moment=obj).all()
        return [model_to_dict(row.topic, fields=['id', 'title']) for row in topic_obj]

    def get_imageList(self,obj):
        query_details = MomentDetail.objects.filter(moment = obj)
        #return [row.path for row in query_details]
        return [model_to_dict(row, fields=["id","path","path_key"]) for row in query_details]
    # def get_viewer(self,obj):
    #     viewer_count = models.MomentViewerRecord.objects.filter(moment=obj).count()
    #     viewer_query = models.MomentViewerRecord.objects.filter(moment=obj).order_by('-id')[0:5]
    #
    #     context = {
    #         "count": viewer_count,
    #         "viewerRecord": [model_to_dict(item.viewer_user,["nickName","avatarUrl"]) for item in viewer_query]
    #     }
    #     return context
    def get_comment(self,obj):
        #check user
        request = self.context.get("request")
        if not request.user:
            '''if the user dose not exist, the is_favor is set to false by default'''
            # process comment
            comment_query = models.CommentRecord.objects.filter(moment=obj).order_by('-id')
            comment_count = comment_query.count()
            comment_query = comment_query[0:10].values(
                "id",
                "moment_id",
                "content",
                "user_id",
                "nickName",
                "avatarUrl",
                "reply_id",
                "reply__user_id",
                "reply__nickName",
                "depth",
                "root_id",
                "create_date",
                "favor_count",
                "comment_status"
            )

            comment_list = collections.OrderedDict()
            for item in comment_query:
                item['is_favor'] = False
                # -------------------------
                if item["user_id"] != obj.user.id:
                    item["status"] = {
                        "comment_status_user_id": item["user_id"],
                        "comment_status_name": None
                    }
                    if item["comment_status"] == 1:
                        item["status"] = {
                            "comment_status_user_id": None,
                            "comment_status_name": "条"
                        }
                        if item["favor_count"] > settings.MAX_FAVOR_COUNT_IF_STATUS_COMMENT:
                            item["status"] = {
                                "comment_status_user_id": item["user_id"],
                                "comment_status_name": "裂"
                            }
                else:
                    if obj.if_status == 0:
                        item["status"] = {
                            "comment_status_user_id": item["user_id"],
                            "comment_status_name": None
                        }
                        if item["comment_status"] == 1:
                            item["status"] = {
                                "comment_status_user_id": None,
                                "comment_status_name": "条"
                            }
                            if item["favor_count"] > settings.MAX_FAVOR_COUNT_IF_STATUS_COMMENT:
                                item["status"] = {
                                    "comment_status_user_id": item["user_id"],
                                    "comment_status_name": "裂"
                                }
                    else:
                        if obj.favor_count > settings.MAX_FAVOR_COUNT_IF_STATUS:
                            item["status"] = {
                                "comment_status_user_id": item["user_id"],
                                "comment_status_name": "裂"
                            }
                        item["status"] = {
                            "comment_status_user_id": None,
                            "comment_status_name": "条"
                        }
                #item["create_date"] = item["create_date"].strftime("%Y-%m-%d %H:%M:%S")
                #时间处理 开始
                a = item["create_date"]
                b = datetime.datetime.now()
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
                    create_date = str(day) + "天前"
                else:
                    if (hour_ori > 1):
                        create_date = str(hour_ceil) + "小时前"
                    else:
                        if (minute_ori > 1):
                            create_date = str(minute_ceil) + "分钟前"
                        else:
                            create_date = str(second) + "秒前"
                item["create_date"] = create_date
                #时间处理 结束
                comment_list[item["id"]] = item
            context = {
                "count": comment_count,
                "commentRecord": comment_list.values()
            }
            return context
        '''if the user exists'''
        #process comment
        comment_query = models.CommentRecord.objects.filter(moment=obj).order_by('-id')
        comment_count = comment_query.count()
        comment_query = comment_query[0:10].values(
            "id",
            "moment_id",
            "content",
            "user_id",
            "nickName",
            "avatarUrl",
            "reply_id",
            "reply__user_id",
            "reply__nickName",
            "depth",
            "root_id",
            "create_date",
            "favor_count",
            "comment_status"
        )

        comment_list = collections.OrderedDict()
        for item in comment_query:
            #check whether comment was favored
            temp_id = item["id"]
            commentfavor_object = models.CommentFavorRecord.objects.filter(user=request.user, commentRecord_id=temp_id)
            exists = commentfavor_object.exists()
            if exists:
                item['is_favor']=True
            else:
                item['is_favor'] = False
            #显示自己身份
            if item["user_id"] == request.user.id:
                item['nickName'] = item['nickName']+'(我)'
            if item['reply__user_id'] ==request.user.id:
                item['reply__nickName'] = item['reply__nickName']+'(我)'
            #-------------------------
            if item["user_id"] != obj.user.id:
                item["status"] = {
                    "comment_status_user_id": item["user_id"],
                    "comment_status_name": None
                }
                if item["comment_status"] == 1:
                    item["status"] = {
                        "comment_status_user_id": None,
                        "comment_status_name": "条"
                    }
                    if item["favor_count"] > settings.MAX_FAVOR_COUNT_IF_STATUS_COMMENT:
                        item["status"] = {
                            "comment_status_user_id": item["user_id"],
                            "comment_status_name": "裂"
                        }
            else:
                if obj.if_status == 0:
                    item["status"] = {
                        "comment_status_user_id": item["user_id"],
                        "comment_status_name": None
                    }
                    if item["comment_status"] == 1:
                        item["status"] = {
                            "comment_status_user_id": None,
                            "comment_status_name": "条"
                        }
                        if item["favor_count"] > settings.MAX_FAVOR_COUNT_IF_STATUS_COMMENT:
                            item["status"] = {
                                "comment_status_user_id": item["user_id"],
                                "comment_status_name": "裂"
                            }
                else:
                    if obj.favor_count > settings.MAX_FAVOR_COUNT_IF_STATUS:
                        item["status"] = {
                            "comment_status_user_id": item["user_id"],
                            "comment_status_name": "裂"
                        }
                    item["status"] = {
                        "comment_status_user_id": None,
                        "comment_status_name": "条"
                    }
            #item["create_date"] = item["create_date"].strftime("%Y-%m-%d %H:%M:%S")
            # 时间处理 开始
            a = item["create_date"]
            b = datetime.datetime.now()
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
                create_date = str(day) + "天前"
            else:
                if (hour_ori > 1):
                    create_date = str(hour_ceil) + "小时前"
                else:
                    if (minute_ori > 1):
                        create_date = str(minute_ceil) + "分钟前"
                    else:
                        create_date = str(second) + "秒前"
            item["create_date"] = create_date
            # 时间处理 结束
            comment_list[item["id"]]=item
        context={
            "count": comment_count,
            "commentRecord": comment_list.values()
        }
        return context
    def get_is_favor(self,obj):
        request = self.context.get("request")
        if not request.user:
            return False
        momentfavor_object = models.MomentFavorRecord.objects.filter(user=request.user,moment=obj)
        exists = momentfavor_object.exists()
        if exists:
            return True
        return False
    def get_create_date(self,obj):
        create_date = obj.create_date
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
            return str(day) + "天前"
        else:
            if (hour_ori > 1):
                return str(hour_ceil) + "小时前"
            else:
                if (minute_ori > 1):
                    return str(minute_ceil) + "分钟前"
                else:
                    return str(second) + "秒前"

class MomentFavorSerializer(ModelSerializer):
    class Meta:
        model = MomentFavorRecord
        exclude = ["user"]