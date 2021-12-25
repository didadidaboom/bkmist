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
        if not self.request.data.get("imageList"):
            del self.request.data["imageList"]
            return publish.PublishSerializerWithoutFig
        return self.serializer_class

    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user)
        return obj

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.data.get("address"):
            serializer.save(address=request.data.get("address"))
        if request.data.get("addressName"):
            serializer.save(addressName=request.data.get("addressName"))
        if request.data.get("latitude"):
            serializer.save(latitude=request.data.get("latitude"))
        if request.data.get("longitude"):
            serializer.save(longitude=request.data.get("longitude"))
        moment_obj = self.perform_create(serializer)
        if request.data.get("topic"):
            for topic in request.data.get("topic"):
                TopicCitedRecord.objects.create(
                    topic_id=topic,
                    moment=moment_obj,
                )
                models.TopicInfo.objects.filter(id=topic).update(cited_count=F('cited_count') + 1)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)
