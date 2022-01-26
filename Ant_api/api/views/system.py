from rest_framework.generics import DestroyAPIView,CreateAPIView,ListAPIView
from rest_framework.views import APIView

from api import models
from api.serializer import system

from utils import pagination,filter,auth

class SystemmessageView(CreateAPIView):
    queryset = models.PreSystem.objects
    serializer_class = system.SystemmessageModelSerializer


class PreSystemListView(ListAPIView):
    serializer_class = system.GetPreSystemListModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        queryset = models.PreSystem.objects.all().order_by("-id")
        return queryset

class DelPreSystemView(DestroyAPIView):
    queryset = models.PreSystem.objects
    authentication_classes = [auth.GeneralAuthentication,]