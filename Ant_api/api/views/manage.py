from rest_framework.generics import UpdateAPIView,ListAPIView

from api import models
from api.serializer import manage

from utils import pagination,filter,auth

class getAllChongOpenidUsedListView(ListAPIView):
    serializer_class = manage.getAllOpenidUsedListModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        queryset = models.UserInfo.objects.filter(openID__startswith="oCKHr4gWMcH8ql0MPh7eE74llRpc").all().order_by("-id")
        return queryset

class getAllCHOpenidUsedListView(ListAPIView):
    serializer_class = manage.getAllOpenidUsedListModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        queryset = models.UserInfo.objects.filter(openID__startswith="oCKHr4nB-yw3eAapHjGUFxGmEzj4").all().order_by("-id")
        return queryset


class UpdateOpenidView(UpdateAPIView):
    queryset = models.UserInfo.objects
    serializer_class = manage.UpdateopenidModelSerializer

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

