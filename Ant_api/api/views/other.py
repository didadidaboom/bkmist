from rest_framework.generics import RetrieveAPIView,ListAPIView,CreateAPIView,UpdateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.db.models import Q,F
from django.utils import timezone

from api import models
from api.serializer.personalMoment import PersonalMomentModelSerializer
from api.serializer.other import OtherDetailsModelSerializer,FocusUserModelSerializer
from utils.auth import UserAuthentication
from utils.filter import MinFilterBackend,MaxFilterBackend
from utils.pagination import Pagination

class OtherDetailsView(RetrieveAPIView):
    queryset = models.UserInfo.objects
    serializer_class = OtherDetailsModelSerializer
    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        #判断用户是否登陆，如果登陆，增减浏览量，如果没有登陆，不影响浏览量
        if not request.user:
            return response
        user_object = self.get_object()
        if int(user_object.id) is int(request.user.id):
            return response
        viewer_object=models.UserViewerRecord.objects.filter(user=user_object,viewer_user=request.user)
        #viewer notify
        viewernotify_obj = models.ViewerNotification.objects.filter(toUser=user_object)
        if viewernotify_obj.exists():
            viewernotify_obj.update(viewer_count_page1=F("viewer_count_page1")+1)
        else:
            viewernotify_obj.create(toUser=user_object,viewer_count_page1=1)
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count")+1,create_time=timezone.now())
            models.UserInfo.objects.filter(id=user_object.id).update(viewer_count=F("viewer_count") + 1)
            return response
        viewer_object.create(user=user_object,viewer_user=request.user,viewer_count=1,create_time=timezone.now())
        models.UserInfo.objects.filter(id=user_object.id).update(viewer_count=F("viewer_count")+1)
        return response

class OtherMomentsView(ListAPIView):
    serializer_class = PersonalMomentModelSerializer
    pagination_class = Pagination
    filter_backends = [MinFilterBackend,MaxFilterBackend]

    def get_queryset(self):
        queryset = models.Moment.objects.filter(
            user_id=self.request.query_params.get("user_id"),
            moment_status__in=[0, 1]).filter(Q(if_status=0)|Q(
            Q(favor_count__gt = settings.MAX_FAVOR_COUNT_IF_STATUS)|
            Q(comment_count__gt = settings.MAX_COMMENT_COUNT_IF_STATUS))
        ).order_by('-id')
        return queryset

class FocusUserView(APIView):
    authentication_classes = [UserAuthentication,]
    def post(self, request, *args, **kwargs):
        '''
        1.判断关注的用户是否是本人
        2.验证数据
        3.判断是否存在：存在 删除；不存在 保存
        '''
        serializer = FocusUserModelSerializer(data=request.data)
        if request.data.get("user") == self.request.user.id:
            return Response({},status=status.HTTP_204_NO_CONTENT)
        ser = serializer.is_valid()
        if not ser:
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        obj = models.UserFocusRecord.objects.filter(
            user = request.data.get("user"),
            focus_user = self.request.user
        )
        user_obj = models.UserInfo.objects
        # viewer notify
        viewernotify_obj = models.ViewerNotification.objects.filter(toUser=user_obj.first())
        if viewernotify_obj.exists():
            viewernotify_obj.update(focused_count=F("focused_count") + 1)
        else:
            viewernotify_obj.create(toUser=user_obj.first(), focused_count=1)

        exists = obj.exists()
        if not exists:
            serializer.save(focus_user=self.request.user)
            user_obj.filter(id=serializer.validated_data.get("user").id).update(focused_count=F("focused_count")+1)
            user_obj.filter(id=self.request.user.id).update(focus_count=F("focus_count")+1)
            models.Notification.objects.create(notificationType=31, fromUser=self.request.user,
                                               toUser_id=serializer.validated_data.get("user").id, userHasChecked=True)
            return Response({},status=status.HTTP_201_CREATED)
        user_obj.filter(id=request.data.get("user")).update(focused_count=F("focused_count")-1)
        user_obj.filter(id=self.request.user.id).update(focus_count=F("focus_count")-1)
        obj.delete()
        notify_obj = models.Notification.objects.filter(notificationType=31, fromUser=self.request.user,
                                           toUser_id=request.data.get("user"), userHasChecked=True)
        if notify_obj.exists():
            notify_obj.delete()
        else:
            models.Notification.objects.create(notificationType=32, fromUser=self.request.user,
                                               toUser_id=serializer.validated_data.get("user").id, userHasChecked=True)
        return Response({}, status=status.HTTP_200_OK)

