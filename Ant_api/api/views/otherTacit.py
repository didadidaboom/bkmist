from django.utils import timezone
from django.db.models import Q,F

from rest_framework.generics import ListAPIView

from api import models
from api.serializer.personalTacit import PersonalTacitModelSerializer
from api.serializer.personalTacit import PersonalTacitReplyModelSerializer

from utils.auth import UserAuthentication
from utils.filter import MinFilterBackend,MaxFilterBackend
from utils.pagination import Pagination

class OtherTacitsView(ListAPIView):
    serializer_class = PersonalTacitModelSerializer
    pagination_class = Pagination
    filter_backends = [MinFilterBackend, MaxFilterBackend]

    def get_queryset(self):
        queryset = models.TacitRecord.objects.filter(
            user_id=self.request.query_params.get("user_id"),
            tacit_status__in=[0, 1]).order_by('-id')
        return queryset
    def get(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user_id")
        if not request.user:
            return self.list(request, *args, **kwargs)
        if int(user_id) is int(request.user.id):
            return self.list(request, *args, **kwargs)
        viewer_object = models.UserViewerRecordPage2.objects.filter(user_id=user_id, viewer_user=request.user)
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count") + 1, create_time=timezone.now())
            models.UserInfo.objects.filter(id=user_id).update(viewer_count_page2=F("viewer_count_page2") + 1)
            return self.list(request, *args, **kwargs)
        viewer_object.create(user_id=user_id, viewer_user=request.user, viewer_count=1, create_time=timezone.now())
        models.UserInfo.objects.filter(id=user_id).update(viewer_count_page2=F("viewer_count_page2") + 1)
        return self.list(request, *args, **kwargs)

class OtherTacitsReplyView(ListAPIView):
    serializer_class = PersonalTacitReplyModelSerializer
    pagination_class = Pagination
    filter_backends = [MinFilterBackend, MaxFilterBackend]

    def get_queryset(self):
        queryset = models.TacitRecord.objects.filter(
            user_id=self.request.query_params.get("user_id"),
            tacit_reply_status__in=[0, 1]).order_by('-id')
        return queryset

    def get(self, request, *args, **kwargs):
        user_id = self.request.query_params.get("user_id")
        if not request.user:
            return self.list(request, *args, **kwargs)
        if int(user_id) is int(request.user.id):
            print(2222)
            return self.list(request, *args, **kwargs)
        viewer_object = models.UserViewerRecordPage3.objects.filter(user_id=user_id, viewer_user=request.user)
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count") + 1, create_time=timezone.now())
            models.UserInfo.objects.filter(id=user_id).update(viewer_count_page3=F("viewer_count_page3") + 1)
            return self.list(request, *args, **kwargs)
        viewer_object.create(user_id=user_id, viewer_user=request.user, viewer_count=1, create_time=timezone.now())
        models.UserInfo.objects.filter(id=user_id).update(viewer_count_page3=F("viewer_count_page3") + 1)
        return self.list(request, *args, **kwargs)