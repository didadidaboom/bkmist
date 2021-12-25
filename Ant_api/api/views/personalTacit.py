from rest_framework.generics import ListAPIView,UpdateAPIView,DestroyAPIView
from rest_framework.response import Response

from api import models
from api.serializer.personalTacit import PersonalTacitModelSerializer
from api.serializer.personalTacit import UpdatePersonalTacitModelSerializer
from api.serializer.personalTacit import PersonalTacitReplyModelSerializer

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