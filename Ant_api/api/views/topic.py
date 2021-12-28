from django.db.models import F
from django.utils import timezone
from django.forms.models import model_to_dict

from rest_framework.views import APIView
from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from api.models import TopicInfo,UserInfo
from api import models
from api.serializer.topic import TopicSerializer,FocusTopicModelSerializer
from api.serializer import moment,topic

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


class TopicMomentTimeView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        cited_obj = models.TopicCitedRecord.objects.filter(topic_id=int(topic_id)).all()
        moment_list = [obj.moment_id for obj in cited_obj]
        queryset = models.Moment.objects.filter(moment_status=0,id__in=moment_list).all().order_by('-id')
        return queryset

class TopicMomentHotViewView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        cited_obj = models.TopicCitedRecord.objects.filter(topic_id=int(topic_id)).all()
        moment_list = [obj.moment_id for obj in cited_obj]
        queryset = models.Moment.objects.filter(moment_status=0,id__in=moment_list).all().order_by('-viewer_count')
        return queryset

class TopicMomentHotCommentView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        cited_obj = models.TopicCitedRecord.objects.filter(topic_id=int(topic_id)).all()
        moment_list = [obj.moment_id for obj in cited_obj]
        queryset = models.Moment.objects.filter(moment_status=0,id__in=moment_list).all().order_by('-comment_count')
        return queryset

class TopicMomentHotFavorView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

    def get_queryset(self):
        topic_id = self.request.query_params.get("topic_id")
        cited_obj = models.TopicCitedRecord.objects.filter(topic_id=int(topic_id)).all()
        moment_list = [obj.moment_id for obj in cited_obj]
        queryset = models.Moment.objects.filter(moment_status=0,id__in=moment_list).all().order_by('-favor_count')
        return queryset

class TopicDetailView(RetrieveAPIView):
    queryset = models.TopicInfo.objects
    authentication_classes = [GeneralAuthentication,]
    serializer_class = topic.GetTopicDetailModelSerializer
    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        if not request.user:
            return response
        topic_object = self.get_object()
        if int(topic_object.user.id) is int(request.user.id):
            return response
        viewer_object=models.TopicViewerRecord.objects.filter(topic=topic_object,viewer_user=request.user)
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count")+1,create_time=timezone.now())
            models.TopicInfo.objects.filter(id=topic_object.id).update(viewer_count=F("viewer_count") + 1)
            return response
        viewer_object.create(viewer_user=request.user,topic=topic_object,create_time=timezone.now(),viewer_count=1)
        models.TopicInfo.objects.filter(id=topic_object.id).update(viewer_count=1)
        return response

class FocusTopicView(APIView):
    authentication_classes = [UserAuthentication,]
    def post(self, request, *args, **kwargs):
        '''
        1.判断关注的用户是否是本人
        2.验证数据
        3.判断是否存在：存在 删除；不存在 保存
        '''
        serializer = FocusTopicModelSerializer(data=request.data)
        ser = serializer.is_valid()
        if not ser:
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        obj = models.TopicFocusRecord.objects.filter(
            topic = int(request.data.get("topic")),
            user = self.request.user.id
        )
        topic_obj = models.TopicInfo.objects
        exists = obj.exists()
        if not exists:
            serializer.save(user=self.request.user)
            topic_obj.filter(id=int(request.data.get("topic"))).update(focus_count=F("focus_count")+1)
            return Response({},status=status.HTTP_201_CREATED)
        topic_obj.filter(id=int(request.data.get("topic"))).update(focus_count=F("focus_count")-1)
        obj.delete()
        return Response({}, status=status.HTTP_200_OK)
