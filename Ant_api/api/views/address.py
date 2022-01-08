from django.db.models import F
from django.utils import timezone
from django.forms.models import model_to_dict

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import status

from api import models
from api.serializer import moment
from api.serializer import address

from utils.auth import GeneralAuthentication,UserAuthentication
from utils import pagination,filter

class AddressDetailView(RetrieveAPIView):
    queryset = models.Address.objects
    authentication_classes = [GeneralAuthentication,]
    serializer_class = address.GetAddressDetailModelSerializer

class AddressMomentDistanceView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        address_id = self.request.query_params.get("address_id")
        queryset = models.Moment.objects.filter(moment_status=0, address =int(address_id)).all().order_by('-id')
        return queryset

class FocusAddressView(APIView):
    authentication_classes = [UserAuthentication,]
    def post(self, request, *args, **kwargs):
        '''
        1.判断关注的用户是否是本人
        2.验证数据
        3.判断是否存在：存在 删除；不存在 保存
        '''
        serializer = address.FocusAddressModelSerializer(data=request.data)
        ser = serializer.is_valid()
        if not ser:
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        obj = models.AddressFocusRecord.objects.filter(
            address = int(request.data.get("address")),
            user = self.request.user.id
        )
        exists = obj.exists()
        if not exists:
            serializer.save(user=self.request.user)
            return Response({},status=status.HTTP_201_CREATED)
        obj.delete()
        return Response({}, status=status.HTTP_200_OK)