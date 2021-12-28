from django.db.models import F
from django.utils import timezone
from django.forms.models import model_to_dict

from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from api.models import TopicInfo,UserInfo
from api import models
from api.serializer.topic import TopicSerializer
from api.serializer import moment

from utils.auth import UserAuthentication,GeneralAuthentication
from utils import pagination,filter


'''话题模块'''
class TopicView(ListAPIView,CreateAPIView):
    #queryset = TopicInfo.objects.all().order_by("-id")
    queryset = TopicInfo.objects
    serializer_class = TopicSerializer
    def get_queryset(self):
        queryset_ori = TopicInfo.objects.all()
        queryset = queryset_ori
        title = self.request.query_params.get('title')
        if title is not None:
            queryset = queryset_ori.filter(title__contains=title).order_by("-cited_count")
        else:
            queryset = queryset.order_by("-cited_count")[0:10]
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

'''
class TopicMomentView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        print(topic_id)
        cited_obj = models.TopicCitedRecord.objects.filter(topic_id=int(topic_id)).all()
        moment_list = [obj.moment_id for obj in cited_obj]
        print(moment_list)
        queryset = models.Moment.objects.filter(moment_status=0,id__in=moment_list).all().order_by('-id')
        return queryset

class TopicDetailView(RetrieveAPIView):
    queryset = models.TopicInfo.objects
    authentication_classes = [GeneralAuthentication,]
    serializer_class = moment.GetMomentDetailModelSerializer
    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        #验证用户是否登入：登陆增加浏览记录，未登录不进行操作
        #获取AUTHORIZATION
        if not request.user:
            return response
        topic_object = self.get_object()
        if int(topic_object.user.id) is int(request.user.id):
            return response
        viewer_object=models.TopicViewerRecord.objects.filter(topic=topic_object,viewer_user=request.user)
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count")+1,create_time=timezone.now())
            models.Moment.objects.filter(id=moment_object.id).update(viewer_count=F("viewer_count") + 1)
            return response
        viewer_object.create(viewer_user=request.user,moment=moment_object,create_time=timezone.now(),viewer_count=1)
        models.Moment.objects.filter(id=moment_object.id).update(viewer_count=1)
        return response
'''