from django.utils import timezone

from rest_framework.generics import RetrieveAPIView,UpdateAPIView
from rest_framework.generics import ListAPIView,DestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api import models
from api.serializer.personal import PersonalInfoModelSerializer,UpdateNamePersonalModelSerializer
from api.serializer.personal import UpdateAvatarPersonalModelSerializer
from api.serializer.personal import PersonalViewerPage1ModelSerializer,PersonalViewerPage2ModelSerializer
from api.serializer.personal import PersonalViewerPage3ModelSerializer,PersonalViewerPage3ScanModelSerializer
from api.serializer.personal import PersonalViewerPage3SubmitModelSerializer,PersonalMomentViewerViewModelSerializer
from api.serializer.personal import PersonalFocusListModelSerializer,PersonalFocusedListModelSerializer
from utils.auth import UserAuthentication
from utils.randomName import getRegisterAvatar_female,getRegisterAvatar_male

class PersonalInfoView(RetrieveAPIView):
    queryset = models.UserInfo.objects
    serializer_class = PersonalInfoModelSerializer
    authentication_classes = [UserAuthentication,]

    def get_object(self):
        obj = models.UserInfo.objects.filter(id=self.request.user.id)
        obj.update(last_login=timezone.now())
        return obj.first()

class UpdateNamePersonalView(UpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = UpdateNamePersonalModelSerializer
    authentication_classes = [UserAuthentication,]
    def get_object(self):
        return models.UserInfo.objects.get(id=self.request.user.id)
    def put(self, request, *args, **kwargs):
        if self.get_object().nickName == request.data.get("nickName"):
            return Response({},status=status.HTTP_226_IM_USED)
        return self.partial_update(request, *args, **kwargs)

class UpdateAvatarPersonalView(UpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = UpdateAvatarPersonalModelSerializer
    authentication_classes = [UserAuthentication,]
    def get_object(self):
        return models.UserInfo.objects.get(id=self.request.user.id)
    def put(self, request, *args, **kwargs):
        if self.get_object().gender == int(request.data.get("gender")):
            return Response({},status=status.HTTP_226_IM_USED)
        if int(request.data.get("gender")) is 0:
            avatarUrl = getRegisterAvatar_female()
        else:
            avatarUrl = getRegisterAvatar_male()
        request.data["avatarUrl"]=avatarUrl
        return self.partial_update(request, *args, **kwargs)

class DeletePersonalView(DestroyAPIView):
    queryset = models.UserInfo.objects
    authentication_classes = [UserAuthentication, ]
    def get_object(self):
        print(123)
        return models.UserInfo.objects.get(id=self.request.user.id)

class PersonalViewerPage1View(ListAPIView):
    serializer_class = PersonalViewerPage1ModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        models.ViewerNotification.objects.filter(toUser=self.request.user).update(viewer_count_page1=0)
        queryset = models.UserViewerRecord.objects.filter(user=self.request.user).order_by("-create_time")[0:10]
        return queryset

class PersonalViewerPage2View(ListAPIView):
    serializer_class = PersonalViewerPage2ModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        models.ViewerNotification.objects.filter(toUser=self.request.user).update(viewer_count_page2=0)
        queryset = models.UserViewerRecordPage2.objects.filter(user=self.request.user).order_by("-create_time")[0:10]
        return queryset

class PersonalViewerPage3View(ListAPIView):
    serializer_class = PersonalViewerPage3ModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        models.ViewerNotification.objects.filter(toUser=self.request.user).update(viewer_count_page3=0)
        queryset = models.UserViewerRecordPage3.objects.filter(user=self.request.user).order_by("-create_time")[0:10]
        return queryset

class PersonalViewerPage3ScanView(ListAPIView):
    serializer_class = PersonalViewerPage3ScanModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        models.ViewerNotification.objects.filter(toUser=self.request.user).update(tacit_viewer_count=0)
        queryset = models.TacitReplyViewer.objects.filter(user=self.request.user).order_by("-create_time")[0:10]
        return queryset

class PersonalViewerPage3SubmitView(ListAPIView):
    serializer_class = PersonalViewerPage3SubmitModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        models.ViewerNotification.objects.filter(toUser=self.request.user).update(tacit_write_count=0)
        queryset = models.TacitReplyWrite.objects.filter(user=self.request.user).order_by("-create_time")[0:10]
        return queryset

class PersonalMomentViewerView(ListAPIView):
    serializer_class = PersonalMomentViewerViewModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        moment_id = self.request.query_params.get('moment_id')
        models.MomentViewerNotification.objects.filter(moment_id=moment_id).update(momentviewer_count=0)
        queryset = models.MomentViewerRecord.objects.filter(moment=int(moment_id)).order_by("-create_time")[0:10]
        return queryset

class PersonalFocusListView(ListAPIView):
    serializer_class = PersonalFocusListModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        queryset = models.UserFocusRecord.objects.filter(focus_user=self.request.user).order_by("-create_time")[0:10]
        return queryset

class PersonalFocusedListView(ListAPIView):
    serializer_class = PersonalFocusedListModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        models.ViewerNotification.objects.filter(toUser=self.request.user).update(focused_count=0)
        queryset = models.UserFocusRecord.objects.filter(user=self.request.user,).order_by("-create_time")[0:10]
        return queryset

class PersonalFriendListView(ListAPIView):
    serializer_class = PersonalFocusedListModelSerializer
    authentication_classes = [UserAuthentication]
    def get_queryset(self):
        queryset = models.UserFocusRecord.objects.filter(
            user=self.request.user
        ).filter(
            focus_user__user_focus__focus_user=self.request.user
        ).order_by("-create_time")
        return queryset
