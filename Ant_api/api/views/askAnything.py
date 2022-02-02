from rest_framework.generics import CreateAPIView

from api.serializer import askAnything
from utils.auth import UserAuthentication

class CreateAskAnythingView(CreateAPIView):
    serializer_class = askAnything.CreateAskAnythingModelSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user)
        return obj
