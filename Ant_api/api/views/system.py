from rest_framework.generics import UpdateAPIView,CreateAPIView
from rest_framework.views import APIView

from api import models
from api.serializer import system

class SystemmessageView(CreateAPIView):
    queryset = models.PreSystem.objects
    serializer_class = system.SystemmessageModelSerializer
