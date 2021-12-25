from django.db.models import F

from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from api.models import TopicInfo,UserInfo
from api import models
from api.serializer.topic import TopicSerializer


'''话题模块'''
class TopicView(ListAPIView,CreateAPIView):
    #queryset = TopicInfo.objects.all().order_by("-id")
    queryset = TopicInfo.objects
    serializer_class = TopicSerializer
    def get_queryset(self):
        queryset_ori = TopicInfo.objects.all().order_by("-cited_count")
        queryset = queryset_ori
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset_ori.filter(title__contains=title)
        else:
            queryset = queryset[0:10]
        return queryset


    def perform_create(self, serializer):
        serializer.save(user = self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        ser = serializer.is_valid(raise_exception=True)
        if not ser:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data,status=status.HTTP_201_CREATED,headers=headers)