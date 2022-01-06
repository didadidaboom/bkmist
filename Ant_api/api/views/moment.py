from django.utils import timezone
from django.conf import settings

from rest_framework.generics import ListAPIView,CreateAPIView,RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q,F

from api.serializer import moment,topic
from api.models import Moment
from api import models
from utils import filter,pagination
from utils.auth import GeneralAuthentication,UserAuthentication

'''瞬间模块'''
class MomentCreatView(CreateAPIView):
    '''
    瞬间发布创建
    '''
    serializer_class = moment.MomentSerializer
    def perform_create(self, serializer):
        new_object = serializer.save(user_id=3)
        return new_object

'''
class MomentView(APIView):
    def get(self,requests,*args,**kwargs):
        min_id = requests.query_params.get("min_id")
        max_id = requests.query_params.get("max_id")
        if min_id:
            queryset = Moment.objects.filter(id__lt=min_id).order_by('-id')[0:10]
        elif max_id:
            queryset = Moment.objects.filter(id__gt=max_id).order_by('id')[0:10]
        else:
            queryset = Moment.objects.all().order_by('-id')[0:10]
        ser = GetMomentModelSerializer(instance=queryset,many=True)
        return Response(ser.data)

'''

class MomentView(ListAPIView):
    '''
    首页更新瞬间
    '''
    queryset = Moment.objects.filter(moment_status=0).all().order_by('-id')
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]

class FocusMomentView(ListAPIView):
    serializer_class = moment.GetMomentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend,filter.MaxFilterBackend]
    authentication_classes = [UserAuthentication,]
    def get_queryset(self):
        topic_obj = models.TopicFocusRecord.objects.filter(user=self.request.user).all()
        queryset = models.Moment.objects.filter(
            moment_status=0
        ).filter(Q(if_status=0)|Q(
            Q(favor_count__gt = settings.MAX_FAVOR_COUNT_IF_STATUS)|
            Q(comment_count__gt = settings.MAX_COMMENT_COUNT_IF_STATUS))
        ).filter(
            ~Q(user_id=self.request.user.id)
        ).filter(
            Q(user__user_focus__focus_user_id=self.request.user.id)
        ).all().distinct().order_by('-id')
        return queryset

class FocusMomentTopicView(ListAPIView):
    serializer_class = topic.FocusMomentTopicModelSerializer
    authentication_classes = [UserAuthentication,]
    def get_queryset(self):
        queryset = models.TopicFocusRecord.objects.filter(user=self.request.user).all().order_by("-id")
        return queryset


#Q(user__topicfocusrecord__topic_id__in = [22,])
class MomentDetailView(RetrieveAPIView):
    '''
    获取单条瞬间详细
    '''
    queryset = Moment.objects
    authentication_classes = [GeneralAuthentication,]
    serializer_class = moment.GetMomentDetailModelSerializer
    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        #验证用户是否登入：登陆增加浏览记录，未登录不进行操作
        #获取AUTHORIZATION
        if not request.user:
            return response
        moment_object = self.get_object()
        if int(moment_object.user.id) is int(request.user.id):
            return response
        viewer_object=models.MomentViewerRecord.objects.filter(moment=moment_object,viewer_user=request.user)
        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count")+1,create_time=timezone.now())
            models.Moment.objects.filter(id=moment_object.id).update(viewer_count=F("viewer_count") + 1)
            return response
        viewer_object.create(viewer_user=request.user,moment=moment_object,create_time=timezone.now(),viewer_count=1)
        models.Moment.objects.filter(id=moment_object.id).update(viewer_count=1)
        return response

class MomentFavorView(APIView):
    '''
    瞬间喜欢数更新
    '''
    authentication_classes = [UserAuthentication,]
    def post(self, request, *args, **kwargs):
        '''
        1.验证数据
        2.判断是否存在:如果存在 删除；如果不存在 保存
        '''
        serializer = moment.MomentFavorSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        moment_object = serializer.validated_data.get("moment")
        if moment_object.user.id is request.user.id:
            return Response({},status=status.HTTP_204_NO_CONTENT)
        momentfavor_object= models.MomentFavorRecord.objects.filter(user = request.user,moment=moment_object)
        exists = momentfavor_object.exists()
        if exists:
            momentfavor_object.delete()
            models.Moment.objects.filter(id=moment_object.id).update(favor_count=F("favor_count") - 1)
            return Response({},status=status.HTTP_200_OK)
        models.MomentFavorRecord.objects.create(user = request.user,moment=moment_object)
        models.Moment.objects.filter(id=moment_object.id).update(favor_count = F("favor_count")+1)
        return Response({},status=status.HTTP_201_CREATED)