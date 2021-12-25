from rest_framework.generics import ListAPIView,UpdateAPIView,DestroyAPIView

from api import models
from api.serializer.personalMoment import PersonalMomentModelSerializer
from api.serializer.personalMoment import UpdatePersonalMomentModelSerializer
from utils.pagination import Pagination
from utils.filter import MaxFilterBackend,MinFilterBackend
from utils.auth import UserAuthentication


class PersonalMomentView(ListAPIView):
    '''
    更新个人空间瞬间数据
    '''
    serializer_class = PersonalMomentModelSerializer
    authentication_classes = [UserAuthentication,]
    pagination_class = Pagination
    filter_backends = [MinFilterBackend,MaxFilterBackend]

    def get_queryset(self):
        queryset = models.Moment.objects.filter(user = self.request.user).order_by("-id").all()
        return queryset

class UpdatePersonalMomentView(UpdateAPIView):
    queryset = models.Moment.objects
    serializer_class = UpdatePersonalMomentModelSerializer
    authentication_classes = [UserAuthentication,]
    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

class DelPersonalMomentView(DestroyAPIView):
    queryset = models.Moment.objects
    authentication_classes = [UserAuthentication,]