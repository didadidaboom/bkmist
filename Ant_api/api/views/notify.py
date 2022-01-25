from rest_framework.generics import ListAPIView,UpdateAPIView,RetrieveAPIView

from api import models
from api.serializer import notify

from utils import pagination,filter,auth

class NotificationFlagView(ListAPIView):
    serializer_class = notify.GetNotificationFlagModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.UserAuthentication, ]

    def get_queryset(self):
        queryset = models.Notification.objects.filter(toUser=self.request.user,userHasChecked=True).all().order_by('-id')
        return queryset

class NotificationPage1View(ListAPIView):
    serializer_class = notify.GetNotificationModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]
    authentication_classes = [auth.UserAuthentication,]

    def get_queryset(self):
        queryset = models.Notification.objects.filter(toUser=self.request.user).all().order_by('-id')
        return queryset

class NotificationStatusView(UpdateAPIView):
    queryset = models.Notification.objects
    serializer_class = notify.GetNotificationFlagModelSerializer
    authentication_classes = [auth.UserAuthentication, ]

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class SystemNotificationFlagView(ListAPIView):
    serializer_class = notify.GetSystemNotificationFlagModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        if not self.request.user:
            queryset = models.PreSystem.objects.filter(type__lt=20000).all().order_by('-id')
        else:
            queryset = models.SystemNotification.objects.filter(userHasChecked=True).all().order_by('id')
        return queryset



class SystemNotificationView(ListAPIView):
    serializer_class = notify.GetSystemNotificationModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        if not self.request.user:
            queryset = models.PreSystem.objects.filter(type__lt=20000).all().order_by('-id')
        else:
            queryset = models.SystemNotification.objects.filter(type__gt=20000).all().order_by("-id")
        return queryset





