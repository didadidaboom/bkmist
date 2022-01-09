from rest_framework.generics import ListAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q,F

from api import models
from api.serializer.personalTacit import PersonalTacitModelSerializer
from api.serializer.personalTacit import UpdatePersonalTacitModelSerializer
from api.serializer.personalTacit import PersonalTacitReplyModelSerializer
from api.serializer.personalTacit import PersonalTacitRelyFavorSerializer

from utils.pagination import Pagination
from utils.filter import MaxFilterBackend,MinFilterBackend
from utils.auth import UserAuthentication

class PersonalTacitView(ListAPIView):
    '''
        更新个人空间好友测试数据
        '''
    serializer_class = PersonalTacitModelSerializer
    authentication_classes = [UserAuthentication, ]
    pagination_class = Pagination
    filter_backends = [MinFilterBackend, MaxFilterBackend]

    def get_queryset(self):
        queryset = models.TacitRecord.objects.filter(user=self.request.user).order_by("-id").all()
        return queryset

class UpdatePersonalTacitView(UpdateAPIView):
    queryset = models.TacitRecord.objects
    serializer_class = UpdatePersonalTacitModelSerializer
    authentication_classes = [UserAuthentication, ]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class DelPersonalTacitView(DestroyAPIView):
    queryset = models.TacitRecord.objects
    authentication_classes = [UserAuthentication, ]

class example_PersonalTacitReplyView(ListAPIView):
    '''
        更新别人眼里个人空间好友测试数据
        '''
    serializer_class = PersonalTacitReplyModelSerializer
    authentication_classes = [UserAuthentication, ]
    pagination_class = Pagination
    filter_backends = [MinFilterBackend, MaxFilterBackend]

    def get_queryset(self):
        queryset = models.TacitReplyCitedRecord.objects.filter(tacitReplyRecord__tacitRecord__user_id=self.request.user).order_by("-id").annotate()
        return queryset

class PersonalTacitReplyView(ListAPIView):
    '''
        更新个人空间好友测试数据
        '''
    serializer_class = PersonalTacitReplyModelSerializer
    authentication_classes = [UserAuthentication, ]
    pagination_class = Pagination
    filter_backends = [MinFilterBackend, MaxFilterBackend]

    def get_queryset(self):
        queryset = models.TacitRecord.objects.filter(user=self.request.user).order_by("-id").all()
        return queryset

class personalTacitReplyFavorView(APIView):
    '''
    好友默契回复的被点赞数更新
    '''
    authentication_classes = [UserAuthentication,]
    def post(self, request, *args, **kwargs):
        '''
        1.验证数据
        2.判断是否存在:如果存在 删除；如果不存在 保存
        '''
        tacitReplyRecord_id= request.data.get("tacitReplyRecord")
        tacitReplyRecord_object = models.TacitReplyRecord.objects.get(id=tacitReplyRecord_id)
        if tacitReplyRecord_object.user_id is request.user.id:
            return Response({},status=status.HTTP_204_NO_CONTENT)
        tacitReplyRecordfavor_object= models.TacitReplyFavorRecord.objects.filter(user = request.user,tacitReplyRecord=tacitReplyRecord_object)
        exists = tacitReplyRecordfavor_object.exists()
        if exists:
            tacitReplyRecordfavor_object.delete()
            models.TacitReplyRecord.objects.filter(id=tacitReplyRecord_object.id).update(favor_count=F("favor_count") - 1)
            return Response({},status=status.HTTP_200_OK)
        models.TacitReplyFavorRecord.objects.create(user = request.user,tacitReplyRecord=tacitReplyRecord_object)
        models.TacitReplyRecord.objects.filter(id=tacitReplyRecord_object.id).update(favor_count = F("favor_count")+1)
        return Response({},status=status.HTTP_201_CREATED)