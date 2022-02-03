from rest_framework.generics import CreateAPIView,RetrieveAPIView
from django.db.models import F

from api.serializer import askAnything
from api import models
from utils.auth import UserAuthentication,GeneralAuthentication
from utils.randomName import getNameAvatarlist,getMosaic,getRandomName,getRandomAvatar

class CreateAskAnythingView(CreateAPIView):
    serializer_class = askAnything.CreateAskAnythingModelSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user)
        return obj

class SubmitAskAnythingView(CreateAPIView):
    '''保存评论 同时更新瞬间里面的评论数'''
    serializer_class = askAnything.SubmitAskAnythingModelSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        '''
        1.判断匿名 给定avatar
        2.
        '''
        if (self.request.data.get("comment_status") == 1):
            obj_1 = models.AskAnythingRecord.objects.filter(
                user=self.request.user,
                tacitrecord_id=self.request.data.get("tacitrecord"),
                comment_status=1
            ).order_by("id")
            if obj_1.exists():
                obj_1 = obj_1.first()
                nickName=obj_1.nickName
                avatarUrl=obj_1.avatarUrl
            else:
                nickName = getRandomName()
                avatarUrl = getMosaic()
            com_obj = serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            tacitrecord_id = serializer.data.get("tacitrecord")
            models.TacitRecord.objects.filter(id=tacitrecord_id).update(comment_count=F('comment_count') + 1)
        else:
            obj_0 = models.AskAnythingRecord.objects.filter(
                user=self.request.user,
                tacitrecord_id=self.request.data.get("tacitrecord"),
                comment_status=0
            ).order_by("id")
            if obj_0.exists():
                obj_0_0 = obj_0.first()
                nickName=obj_0_0.nickName
                avatarUrl=obj_0_0.avatarUrl
            else:
                moment_obj = models.TacitRecord.objects.filter(id=self.request.data.get("tacitrecord")).first()
                if self.request.user.id == moment_obj.user.id:
                    nickName = moment_obj.user.real_nickName
                    avatarUrl = moment_obj.user.real_avatarUrl
                else:
                    nickName, avatarUrl = getNameAvatarlist()
            com_obj = serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            tacitrecord_id = serializer.data.get("tacitrecord")
            models.TacitRecord.objects.filter(id=tacitrecord_id).update(comment_count=F('comment_count') + 1)

class AskMeAnythingDetailView(RetrieveAPIView):
    '''
    获取单条瞬间详细
    '''
    queryset = models.TacitRecord.objects
    authentication_classes = [GeneralAuthentication,]
    serializer_class = askAnything.AskMeAnythingDetailModelSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        #验证用户是否登入：登陆增加浏览记录，未登录不进行操作
        #获取AUTHORIZATION
        if not request.user:
            return response
        moment_object = self.get_object()
        if int(moment_object.user.id) is int(request.user.id):
            return response
        return response

