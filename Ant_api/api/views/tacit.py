import random
from django.db.models import Q,F
from django.utils import timezone

from rest_framework.generics import ListAPIView,CreateAPIView,UpdateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.serializer.tacit import TacitModelSerializer,TacitRecordModelSerializer
from api.serializer.tacit import ReplyTacitModelSerializer,TacitReplyRecordModelSerializer
from api import models

from utils.pagination import Pagination
from utils.auth import UserAuthentication,GeneralAuthentication


class TacitView(ListAPIView,CreateAPIView):
    queryset = models.TacitTestDatabase.objects.all().order_by("-id")
    serializer_class = TacitModelSerializer
    pagination_class = Pagination
    authentication_classes = [GeneralAuthentication,]

    def post(self, request, *args, **kwargs):
        del request.data["id"]
        del request.data["selected_answer"]
        if not request.data.get("title"):
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        exist = models.TacitTestDatabase.objects.filter(**request.data).exists()
        if exist:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)

class TacitSaveView(CreateAPIView):
    '''
    创建好友默契答案（作者）
    '''
    serializer_class = TacitRecordModelSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user)
        return obj

class TacitRandomOneView(RetrieveAPIView):
    serializer_class = TacitModelSerializer
    authentication_classes = [GeneralAuthentication]

    def get_object(self):
        usedId = self.request.query_params.get("usedId")
        min_id = self.request.query_params.get("min_id")
        pk = random.randint(1,int(min_id)-1)
        flag = True
        while flag:
            if str(pk) in usedId:
                flag = True
                pk = random.randint(1, int(min_id) - 1)
            else:
                exist = models.TacitTestDatabase.objects.filter(id=pk).exists()
                if not exist:
                    flag = True
                    usedId.append(pk)
                    pk = random.randint(1, int(min_id) - 1)
                else:
                    flag = False
        obj = models.TacitTestDatabase.objects.get(id=pk)
        return obj

class ReplyTacitView(RetrieveAPIView):
    queryset = models.TacitRecord
    serializer_class = ReplyTacitModelSerializer
    authentication_classes = [GeneralAuthentication,]
    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if int(object.user.id) is int(request.user.id):
            return self.retrieve(request, *args, **kwargs)
        viewer_object = models.TacitReplyViewer.objects.filter(user=object.user, viewer_user=self.request.user,source="默契测试")
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count") + 1, create_time=timezone.now())
            models.UserInfo.objects.filter(id=object.user.id).update(tacit_viewer_count=F("tacit_viewer_count") + 1)
            return self.retrieve(request, *args, **kwargs)
        viewer_object.create(user=object.user, viewer_user=self.request.user, viewer_count=1, create_time=timezone.now())
        models.UserInfo.objects.filter(id=object.user.id).update(tacit_viewer_count=F("tacit_viewer_count") + 1)
        return self.retrieve(request, *args, **kwargs)

class ReplyTacitSaveView(CreateAPIView):
    '''
        创建好友默契答案（回复者）
        '''
    serializer_class = TacitReplyRecordModelSerializer
    authentication_classes = [UserAuthentication, ]
    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user)
        viewer_object = models.TacitReplyWrite.objects.filter(user=obj.tacitRecord.user, viewer_user=self.request.user,source="默契测试")
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(write_count=F("write_count") + 1, create_time=timezone.now())
            models.UserInfo.objects.filter(id=obj.tacitRecord.user_id).update(tacit_write_count=F("tacit_write_count") + 1)
            return obj
        viewer_object.create(user=obj.tacitRecord.user, viewer_user=self.request.user, write_count=1, create_time=timezone.now())
        models.UserInfo.objects.filter(id=obj.tacitRecord.user_id).update(tacit_write_count=F("tacit_write_count") + 1)
        return obj
    def post(self, request, *args, **kwargs):
        tacitRecord = request.data.get("tacitRecord")
        obj = models.TacitRecord.objects.get(id=tacitRecord)
        if int(obj.user_id) is int(request.user.id):
            return Response({},status=status.HTTP_204_NO_CONTENT)
        object = models.TacitReplyRecord.objects.filter(tacitRecord=tacitRecord,user=request.user)
        exist = object.exists()
        if exist:
            return Response({},status=status.HTTP_226_IM_USED)
        return self.create(request, *args, **kwargs)




