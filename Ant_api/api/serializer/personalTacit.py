import datetime
from math import ceil,floor

from rest_framework import serializers
from rest_framework.response import Response
from django.forms.models import model_to_dict
from django.conf import settings

from api import models
from utils.randomName import getNameAvatarlist,getMosaic,getRandomName,getRandomAvatar

class PersonalTacitModelSerializer(serializers.ModelSerializer):
    tacitDataList = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    class Meta:
        model = models.TacitRecord
        #fields = "__all__"
        fields = ["id", "create_date", "avatarUrlFlag", "tacit_status","tacitDataList","type"]
    def get_tacitDataList(self,obj):
        if int(obj.type) == 10001:
            obj_list = models.TacitCitedRecord.objects.filter(tacitRecord=obj).all()
            #results = [model_to_dict(
            #    row.tacitTestDatabase, ["title", "answer1", "answer2", "answer3", "answer4", "answer5"]) for row in
            #    obj_list]
            results = [{
                "title":row.tacitTestDatabase.title,
                "answer1":row.tacitTestDatabase.answer1,
                "answer2":row.tacitTestDatabase.answer2,
                "answer3":row.tacitTestDatabase.answer3,
                "answer4":row.tacitTestDatabase.answer4,
                "answer5":row.tacitTestDatabase.answer5,
                "selected_answer":row.selected_answer
            } for row in obj_list]
            return results
        elif int(obj.type) == 20001:
            request = self.context.get("request")
            obj_list = models.AskAnythingRecord.objects.filter(tacitrecord=obj,depth=1).order_by('-id').all()
            results = []
            for row in obj_list:
                result = {
                    "content": row.content,
                    "comment_status": row.comment_status,
                    "favor_count":row.favor_count
                }
                if row.comment_status:
                    nickName = getRandomName()
                    avatarUrl = getMosaic()
                    if_status_name = '条'
                    user_id = None
                    if row.favor_count > settings.TACITREPLY_MAX_FAVOR_COUNT_IF_STATUS:
                        user_id = row.user.id
                        if_status_name = "裂"
                else:
                    if row.avatarUrlFlag:
                        user_id = row.user_id
                        nickName = row.user.real_nickName
                        avatarUrl = row.user.real_avatarUrl
                        if_status_name = None
                    else:
                        user_id = row.user_id
                        nickName = row.user.real_nickName
                        avatarUrl = row.user.real_avatarUrl
                        if_status_name = None
                result["nickName"] = nickName
                result["avatarUrl"] = avatarUrl
                result["if_status_name"] = if_status_name
                result["user_id"] = user_id
                # is_favor
                if not request.user:
                    result["is_favor"] = False
                else:
                    result["is_favor"] = False
                    askmyanythingfavor_object = models.AskAnythingFavorRecord.objects.filter(user=request.user,
                                                                                         askAnythingRecord=row)
                    exists = askmyanythingfavor_object.exists()
                    if exists:
                        result["is_favor"] = True
                # time
                a = row.create_date
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
                        create_date = str(hour_floor) + "小时前"
                    else:
                        if (minute_ori > 1):
                            create_date = str(minute_floor) + "分钟前"
                        else:
                            create_date = str(second) + "秒前"
                result["create_date"] = create_date
                results.append(result)
            return results
        else:
            return None
class UpdatePersonalTacitModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TacitRecord
        fields = "__all__"

class example_PersonalTacitReplyModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    match_count = serializers.SerializerMethodField()
    tacitDataList = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    class Meta:
        model = models.TacitReplyRecord
        #fields = "__all__"
        fields = ["id","tacitRecord","user", "match_count", "create_date", "if_status","tacitDataList"]
    def get_user(self,obj):
        if obj.if_status:
            nickName = getRandomName()
            avatarUrl = getMosaic()
            if_status_name = '条'
            user_id = None
            if obj.favor_count > settings.TACITREPLY_MAX_FAVOR_COUNT_IF_STATUS:
                user_id = obj.user.id
                if_status_name = "裂"
            return {"id": user_id, "nickName": nickName, "avatarUrl": avatarUrl, "if_status_name": if_status_name}
        else:
            if obj.avatarUrlFlag:
                return {"id": obj.user.id, "nickName": obj.user.real_nickName, "avatarUrl": obj.user.real_avatarUrl,
                        "if_status_name": None}
            else:
                return {"id": obj.user.id, "nickName": obj.user.nickName, "avatarUrl": obj.user.avatarUrl,
                    "if_status_name": None}

    def get_match_count(self,obj):
        match_count = obj.match_count/10*100
        return match_count


class PersonalTacitReplyModelSerializer(serializers.ModelSerializer):
    tacitDataList = serializers.SerializerMethodField()
    replyList = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    class Meta:
        model = models.TacitRecord
        #fields = "__all__"
        fields = ["id","tacit_reply_status","tacitDataList","replyList","create_date"]
    def get_tacitDataList(self,obj):
        obj_list = models.TacitCitedRecord.objects.filter(tacitRecord=obj).all()
        #results = [model_to_dict(
        #    row.tacitTestDatabase, ["title", "answer1", "answer2", "answer3", "answer4", "answer5"]) for row in
        #    obj_list]
        results = [{
            "title":row.tacitTestDatabase.title,
            "answer1":row.tacitTestDatabase.answer1,
            "answer2":row.tacitTestDatabase.answer2,
            "answer3":row.tacitTestDatabase.answer3,
            "answer4":row.tacitTestDatabase.answer4,
            "answer5":row.tacitTestDatabase.answer5,
        } for row in obj_list]
        return results
    def get_replyList(self,obj):
        request = self.context.get("request")
        obj_cited_list = models.TacitReplyRecord.objects.filter(tacitRecord=obj).order_by('-id').all()
        results = []
        for row in obj_cited_list:
            result = {
                "id": row.id,
                "if_status": row.if_status,
            }
            result["self_label"] = None
            if request.user == row.user:
                exist = models.TacitReplyRecord.objects.filter(tacitRecord=row.tacitRecord, user=request.user).exists()
                if exist:
                    result["self_label"] = "我"
            if row.if_status:
                nickName = getRandomName()
                avatarUrl = getMosaic()
                if_status_name = '条'
                user_id = None
                if row.favor_count > settings.TACITREPLY_MAX_FAVOR_COUNT_IF_STATUS:
                    user_id = row.user.id
                    if_status_name = "裂"
            else:
                if row.avatarUrlFlag:
                    user_id = row.user_id
                    nickName = row.user.real_nickName
                    avatarUrl = row.user.real_avatarUrl
                    if_status_name = None
                else:
                    user_id = row.user_id
                    nickName = row.user.nickName
                    avatarUrl = row.user.avatarUrl
                    if_status_name = None
            result["nickName"] = nickName
            result["avatarUrl"] = avatarUrl
            result["if_status_name"] = if_status_name
            result["user_id"] = user_id
            result["match_count"] = (row.match_count)/10.*100
            cited_obj = models.TacitReplyCitedRecord.objects.filter(tacitReplyRecord=row).all()
            answer = [model_to_dict(cited_row, ["selected_answer"] ) for cited_row in cited_obj]
            result["answer"]=answer
            #is_favor
            if not request.user:
                result["is_favor"] = False
            else:
                result["is_favor"] = False
                tacitreplyfavor_object = models.TacitReplyFavorRecord.objects.filter(user=request.user, tacitReplyRecord=row)
                exists = tacitreplyfavor_object.exists()
                if exists:
                    result["is_favor"] = True
            results.append(result)
        return results

class PersonalTacitRelyFavorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TacitReplyFavorRecord
        exclude = ["user"]