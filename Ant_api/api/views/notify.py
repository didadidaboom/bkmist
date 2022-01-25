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

class PreSystemNotificationFlagView(ListAPIView):
    serializer_class = notify.GetPreSystemNotificationFlagModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        queryset = models.PreSystem.objects.filter(type__lt=20000).all().order_by('id')
        return queryset

class SystemNotificationFlagView(ListAPIView):
    serializer_class = notify.GetSystemNotificationFlagModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.UserAuthentication, ]

    def get_queryset(self):
        if self.request.user:
            pre_obj_ori = models.PreSystem.objects.filter(type__gt=20000)
            exist = pre_obj_ori.exists()
            if exist:
                obj = models.SystemNotification.objects.filter(toUser=self.request.user)
                exist1 = obj.exists()
                if exist1:
                    queryset = obj.filter(userHasChecked=True).all().order_by('id')
                else:
                    pre_obj = pre_obj_ori.all()
                    for pre in pre_obj:
                        models.SystemNotification.objects.create(toUser=self.request.user,preSystem=pre,userHasChecked=True)
                    queryset = models.SystemNotification.objects.filter(toUser=self.request.user,userHasChecked=True).all().order_by('id')
            else:
                queryset = None
        else:
            queryset = None
        return queryset

class PreSystemNotificationView(ListAPIView):
    serializer_class = notify.GetPreSystemNotificationModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        queryset = models.PreSystem.objects.filter(type__lt=20000).all().order_by("-id")
        return queryset

class SystemNotificationView(ListAPIView):
    serializer_class = notify.GetSystemNotificationModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.UserAuthentication, ]

    def get_queryset(self):
        queryset = models.SystemNotification.objects.filter(toUser=self.request.user).all().order_by("-id")
        return queryset





