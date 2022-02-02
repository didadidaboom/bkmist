from rest_framework.generics import CreateAPIView

from utils.auth import UserAuthentication

class CreateAskAnythingView(CreateAPIView):
    serializer_class =
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user,type=10001)
        return obj
