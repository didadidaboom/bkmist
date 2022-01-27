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
        # collect data for data analysis
        from django.utils import timezone
        from django.db.models import F
        obj = models.PersonalData.objects.filter(curUser=self.request.user, type=2001)
        if obj.exists():
            obj.update(count=F("count") + 1, latest_time=timezone.now())
        else:
            obj.create(curUser=self.request.user, type=2001, count=F("count") + 1, latest_time=timezone.now())

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
        # collect data for data analysis
        from django.utils import timezone
        from django.db.models import F
        obj = models.PersonalData.objects.filter(curUser=self.request.user, type=3001)
        if obj.exists():
            obj.update(count=F("count") + 1, latest_time=timezone.now())
        else:
            obj.create(curUser=self.request.user, type=3001, count=F("count") + 1, latest_time=timezone.now())
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
        serializer = PersonalTacitRelyFavorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        tacitReplyRecord_object = serializer.validated_data.get("tacitReplyRecord")
        if tacitReplyRecord_object.user.id is request.user.id:
            return Response({},status=status.HTTP_204_NO_CONTENT)
        tacitReplyRecordfavor_object= models.TacitReplyFavorRecord.objects.filter(user = request.user,tacitReplyRecord=tacitReplyRecord_object)
        exists = tacitReplyRecordfavor_object.exists()
        if exists:
            tacitReplyRecordfavor_object.delete()
            tacitreply_obj = models.TacitReplyRecord.objects.filter(id=tacitReplyRecord_object.id)
            tacitreply_obj.update(favor_count=F("favor_count") - 1)
            tacitreply_obj = tacitreply_obj.first()
            notify_obj = models.Notification.objects.filter(notificationType=13, fromUser=self.request.user,
                                                            toUser=tacitreply_obj.user,
                                                            tacit=tacitreply_obj.tacitRecord, userHasChecked=True)
            if notify_obj.exists():
                notify_obj.delete()
            else:
                models.Notification.objects.create(notificationType=63, fromUser=self.request.user,
                                                   toUser=tacitreply_obj.user,
                                                   tacit=tacitreply_obj.tacitRecord, userHasChecked=True)
            return Response({},status=status.HTTP_200_OK)
        models.TacitReplyFavorRecord.objects.create(user = request.user,tacitReplyRecord=tacitReplyRecord_object)
        tacitreply_obj = models.TacitReplyRecord.objects.filter(id=tacitReplyRecord_object.id)
        tacitreply_obj.update(favor_count = F("favor_count")+1)
        tacitreply_obj = tacitreply_obj.filter()
        models.Notification.objects.create(notificationType=13, fromUser=self.request.user,
                                           toUser=tacitreply_obj.user,
                                           tacit=tacitreply_obj.tacitRecord, userHasChecked=True)
        return Response({},status=status.HTTP_201_CREATED)