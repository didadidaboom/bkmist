from django.db.models import F
from django.utils import timezone
from django.forms.models import model_to_dict

from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView,ListAPIView
from rest_framework.response import Response
from rest_framework import status

from api import models
from api.serializer import moment,address

from utils.auth import GeneralAuthentication,UserAuthentication
from utils import pagination,filter

class AddressDetailView(RetrieveAPIView):
    queryset = models.Address.objects
    authentication_classes = [GeneralAuthentication,]
    serializer_class = address.GetAddressDetailModelSerializer

class AddressMomentDistanceView(ListAPIView):
    serializer_class = address.GetAddressMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        address_id = self.request.query_params.get("address_id")
        address_obj = models.Address.objects.get(id=address_id)
        queryset = models.AddressGeohash.objects.filter(
            location__distance_lt=((float(address_obj.latitude), float(address_obj.longitude)), 10.0)
        ).order_by_distance()
        return queryset

class AddressMomentTimeView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        address_id = self.request.query_params.get("address_id")
        address_obj = models.Address.objects.get(id=address_id)
        address_geohash_obj = models.AddressGeohash.objects.filter(
            location__distance_lt=((float(address_obj.latitude),float(address_obj.longitude)),10.0)
        )
        queryset = models.Moment.objects.filter(moment_status=0,
                                                address__addressGeohash__in=address_geohash_obj
                                                ).all().order_by('-id')
        return queryset


class FocusAddressView(APIView):
    authentication_classes = [UserAuthentication,]
    def post(self, request, *args, **kwargs):
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
