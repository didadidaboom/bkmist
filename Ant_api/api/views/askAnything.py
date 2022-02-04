from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status

from api.serializer import askAnything
from api import models
from utils.auth import UserAuthentication,GeneralAuthentication
from utils.randomName import getNameAvatarlist,getMosaic,getRandomName,getRandomAvatar
from utils import pagination,filter

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
        if (int(self.request.data.get("comment_status")) == 1):
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
            serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
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
            serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
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

class AskMeAnythingCommentView(ListAPIView):
    queryset = models.AskAnythingRecord.objects.all().order_by('-id')
    serializer_class = askAnything.AskMeAnythingCommentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinCommentFilterBackend, filter.MaxCommentFilterBackend]

    def get_queryset(self):
        tacitrecord_id = self.request.query_params.get("tacitrecord")
        queryset = models.AskAnythingRecord.objects.filter(tacitrecord_id=int(tacitrecord_id),depth=1).all().order_by("-id")
        # queryset = models.AskAnythingRecord.objects.all().order_by("-id")
        return queryset

class AskAnythingFavorView(APIView):
    '''
    评论点赞更新
    '''
    def get_authenticators(self):
        if self.request.method =="POST":
            return [UserAuthentication(),]
        return [GeneralAuthentication(),]

    def post(self,request,*args,**kwargs):
        '''
        1.验证评论ID是否存在
        2.获取评论ID
        3.查看被赞评论记录是否存在当前用户记录
        4.如果存在 删除；如果不存在 创建
        '''
        ser = askAnything.AskAnythingFavorModelSerializer(data=request.data)
        if not ser.is_valid():
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        askAnythingRecord_object = ser.validated_data.get("askAnythingRecord")
        if askAnythingRecord_object.user.id is request.user.id:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        askAnythingRecord_object = models.AskAnythingFavorRecord.objects.filter(user=request.user,askAnythingRecord=askAnythingRecord_object)
        exist = askAnythingRecord_object.exists()
        if exist:
            askAnythingRecord_object.delete()
            com_obj = models.AskAnythingRecord.objects.filter(id = askAnythingRecord_object.id)
            com_obj.update(favor_count=F('favor_count')-1)
            return Response({}, status=status.HTTP_200_OK)
        askAnythingRecord_object.create(user=request.user,askAnythingRecord=askAnythingRecord_object)
        com_obj = models.AskAnythingRecord.objects.filter(id=askAnythingRecord_object.id)
        com_obj.update(favor_count=F('favor_count') + 1)
        return Response({}, status=status.HTTP_201_CREATED)
