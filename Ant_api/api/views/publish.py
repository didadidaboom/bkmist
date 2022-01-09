from django.db.models import F

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from api.models import Moment,UserInfo,TopicInfo,TopicCitedRecord
from api.serializer import publish
from api import models
from utils.auth import GeneralAuthentication,UserAuthentication

class PublishView(CreateAPIView):
    serializer_class = publish.PublishSerializer
    authentication_classes = [UserAuthentication,]
    def get_serializer_class(self):
        #if not self.request.data.get("imageList"):
        #    del self.request.data["imageList"]
        #    return publish.PublishSerializerWithoutFig
        return self.serializer_class

    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        #if request.data.get("address"):
        #    serializer.save(address=request.data.get("address"))
        #if request.data.get("addressName"):
        #    serializer.save(addressName=request.data.get("addressName"))
        #if request.data.get("latitude"):
        #    serializer.save(latitude=request.data.get("latitude"))
        #if request.data.get("longitude"):
        #    serializer.save(longitude=request.data.get("longitude"))
        moment_obj = self.perform_create(serializer)

        addressList = request.data.get("addressList")
        address = addressList.get("address")
        addressName = addressList.get("addressName")
        latitude = addressList.get("latitude")
        longitude = addressList.get("longitude")
        if (latitude is not None) and (longitude is not None):
            address_obj_ori = models.Address.objects.filter(latitude=latitude,longitude=longitude)
            address_obj = address_obj_ori.first()
            exist = address_obj_ori.exists()
            if not exist:
                if address:
                    if addressName:
                        address_obj = address_obj_ori.create(address=address,addressName=addressName,
                                                      latitude=latitude,longitude=longitude)
                        models.AddressGeohash.objects.create(address=address_obj,location=(float(latitude), float(longitude)))
                    else:
                        address_obj = address_obj_ori.create(address=address, latitude=latitude,
                                                      longitude=longitude)
                        models.AddressGeohash.objects.create(address=address_obj,
                                                             location=(float(latitude), float(longitude)))
                else:
                    if addressName:
                        address_obj = address_obj_ori.create(addressName=addressName,latitude=latitude,
                                                      longitude=longitude)
                        models.AddressGeohash.objects.create(address=address_obj,
                                                             location=(float(latitude), float(longitude)))
                    else:
                        address_obj = address_obj_ori.create(latitude=latitude, longitude=longitude)
                        models.AddressGeohash.objects.create(address=address_obj,
                                                             location=(float(latitude), float(longitude)))
            models.MomentCiteAddressRecord.objects.create(address=address_obj,moment=moment_obj)
        if request.data.get("topic"):
            for topic in request.data.get("topic"):
                TopicCitedRecord.objects.create(
                    topic_id=topic,
                    moment=moment_obj,
                )
                models.TopicInfo.objects.filter(id=topic).update(cited_count=F('cited_count') + 1)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)
