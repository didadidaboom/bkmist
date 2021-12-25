from rest_framework import serializers
from api import models

from utils.randomBonus import getRandomBonus

class TacitModelSerializer(serializers.ModelSerializer):
    selected_answer = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.TacitTestDatabase
        #fields = "__all__",
        fields = ["id","title","answer1","answer2","answer3","answer4","answer5","selected_answer"]

    def get_selected_answer(self,obj):
        return None

class TacitCitedRecordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TacitCitedRecord
        fields = ["tacitTestDatabase","selected_answer"]

class TacitRecordModelSerializer(serializers.ModelSerializer):
    tacitList = TacitCitedRecordModelSerializer(many=True)
    id = serializers.CharField(read_only=True)

    class Meta:
        model = models.TacitRecord
        fields = ["id","avatarUrlFlag","bonus","correct_count","tacitList"]

    def create(self, validated_data):
        bonus = getRandomBonus()
        tacitList_data = validated_data.pop("tacitList")
        tacitRecord = models.TacitRecord.objects.create(**validated_data)
        data_list = models.TacitCitedRecord.objects.bulk_create([models.TacitCitedRecord(**info,tacitRecord=tacitRecord) for info in tacitList_data])
        tacitRecord.tacitList = data_list
        return tacitRecord

class ReplyTacitModelSerializer(serializers.ModelSerializer):
    '''
    序列化 获取我的独白内容
    '''
    tacitDataList = serializers.SerializerMethodField()
    avatarUrl = serializers.SerializerMethodField()
    nickName = serializers.SerializerMethodField()
    create_date = serializers.DateTimeField(format=("%Y-%m-%d %H:%M:%S"))
    class Meta:
        model = models.TacitRecord
        #fields = "__all__"
        fields = ["id", "create_date", "user","avatarUrl", "nickName", "bonus", "tacit_status","tacitDataList"]
    def get_tacitDataList(self,obj):
        obj_list = models.TacitCitedRecord.objects.filter(tacitRecord=obj).all()
        #results = [model_to_dict(
        #    row.tacitTestDatabase, ["title", "answer1", "answer2", "answer3", "answer4", "answer5"]) for row in
        #    obj_list]
        results = [{
            "id":row.tacitTestDatabase.id,
            "title":row.tacitTestDatabase.title,
            "answer1":row.tacitTestDatabase.answer1,
            "answer2":row.tacitTestDatabase.answer2,
            "answer3":row.tacitTestDatabase.answer3,
            "answer4":row.tacitTestDatabase.answer4,
            "answer5":row.tacitTestDatabase.answer5,
            "selected_answer":None,
            "selected_answer_ref": row.selected_answer
        } for row in obj_list]
        return results

    def get_avatarUrl(self,obj):
        if obj.avatarUrlFlag == 0:
            avatarUrl = obj.user.avatarUrl
        if obj.avatarUrlFlag == 1:
            avatarUrl = obj.user.real_avatarUrl
        return avatarUrl

    def get_nickName(self,obj):
        if obj.avatarUrlFlag == 0:
            nickName = obj.user.nickName
        if obj.avatarUrlFlag == 1:
            nickName = obj.user.real_nickName
        return nickName

class TacitReplyCitedRecordModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TacitReplyCitedRecord
        fields = ["selected_answer"]

class TacitReplyRecordModelSerializer(serializers.ModelSerializer):
    tacitList = TacitReplyCitedRecordModelSerializer(many=True)
    '''
    保存用户默契测试评论
    '''

    class Meta:
        model = models.TacitReplyRecord
        fields = ["tacitRecord","avatarUrlFlag","bonus", "match_count", "if_status", "tacitList"]

    def create(self, validated_data):
        if int(validated_data.get("bonus")) is 0:
            validated_data["bonus"] = "无"
        else:
            bonus = getRandomBonus()
            validated_data["bonus"] = bonus
        tacitList_data = validated_data.pop("tacitList")
        tacitReplyRecord = models.TacitReplyRecord.objects.create(**validated_data)
        data_list = models.TacitReplyCitedRecord.objects.bulk_create(
            [models.TacitReplyCitedRecord(**info, tacitReplyRecord=tacitReplyRecord) for info in tacitList_data])
        tacitReplyRecord.tacitList = data_list
        return tacitReplyRecord


