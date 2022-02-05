from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView,RetrieveAPIView,ListAPIView
from django.db.models import F
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone

from api.serializer import askAnything
from api import models
from utils.auth import UserAuthentication,GeneralAuthentication
from utils.randomName import getNameAvatarlist,getMosaic,getRandomName,getRandomAvatar
from utils import pagination,filter

class CreateAskAnythingView(CreateAPIView):
    serializer_class = askAnything.CreateAskAnythingModelSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        obj=serializer.save(user=self.request.user)
        return obj

class ScanAskAnythingView(RetrieveAPIView):
    queryset = models.TacitRecord
    serializer_class = askAnything.ScanAskAnythingModelSerializer
    authentication_classes = [GeneralAuthentication, ]

    def get(self, request, *args, **kwargs):
        object = self.get_object()
        if int(object.user.id) is int(request.user.id):
            return self.retrieve(request, *args, **kwargs)
        viewer_object = models.TacitReplyViewer.objects.filter(user=object.user, viewer_user=self.request.user,
                                                               tacitRecord=object)
        # viewer notify
        viewernotify_obj = models.ViewerNotification.objects.filter(toUser=object.user)
        if viewernotify_obj.exists():
            viewernotify_obj.update(tacit_viewer_count=F("tacit_viewer_count") + 1)
        else:
            viewernotify_obj.create(toUser=object.user, tacit_viewer_count=1)

        exists = viewer_object.exists()
        if exists:
            viewer_object.update(viewer_count=F("viewer_count") + 1, create_time=timezone.now())
            models.UserInfo.objects.filter(id=object.user.id).update(tacit_viewer_count=F("tacit_viewer_count") + 1)
            return self.retrieve(request, *args, **kwargs)
        viewer_object.create(user=object.user, viewer_user=self.request.user, tacitRecord=object, viewer_count=1,
                             create_time=timezone.now(), source="坦白局")
        models.UserInfo.objects.filter(id=object.user.id).update(tacit_viewer_count=F("tacit_viewer_count") + 1)
        return self.retrieve(request, *args, **kwargs)

class ReplyAskAnythingView(CreateAPIView):
    '''保存评论 同时更新瞬间里面的评论数'''
    serializer_class = askAnything.SubmitAskAnythingModelSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        '''
        1.判断匿名 给定avatar
        2.
        '''
        # 通过公开状态保存合适的名字
        if (int(self.request.data.get("comment_status")) == 1):
            obj_1 = models.AskAnythingRecord.objects.filter(
                user=self.request.user,
                tacitrecord_id=self.request.data.get("tacitrecord"),
                comment_status=1
            ).order_by("id")
            if obj_1.exists():
                obj_1 = obj_1.first()
                nickName=obj_1.nickName
                avatarUrl=obj_1.avatarUrl
            else:
                nickName = getRandomName()
                avatarUrl = getMosaic()
            obj = serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            #提问数量
            tacitrecord_id = serializer.data.get("tacitrecord")
            models.TacitRecord.objects.filter(id=tacitrecord_id).update(comment_count=F('comment_count') + 1)

        else:
            obj_0 = models.AskAnythingRecord.objects.filter(
                user=self.request.user,
                tacitrecord_id=self.request.data.get("tacitrecord"),
                comment_status=0
            ).order_by("id")
            if obj_0.exists():
                obj_0_0 = obj_0.first()
                nickName=obj_0_0.nickName
                avatarUrl=obj_0_0.avatarUrl
            else:
                moment_obj = models.TacitRecord.objects.filter(id=self.request.data.get("tacitrecord")).first()
                if self.request.user.id == moment_obj.user.id:
                    nickName = moment_obj.user.real_nickName
                    avatarUrl = moment_obj.user.real_avatarUrl
                else:
                    nickName, avatarUrl = getNameAvatarlist()
            obj = serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            #提问数量
            tacitrecord_id = serializer.data.get("tacitrecord")
            models.TacitRecord.objects.filter(id=tacitrecord_id).update(comment_count=F('comment_count') + 1)
        #统计浏览记录
        viewer_object = models.TacitReplyWrite.objects.filter(user=obj.tacitrecord.user, viewer_user=self.request.user,
                                                              tacitRecord=obj.tacitrecord)
        # viewer notify
        viewernotify_obj = models.ViewerNotification.objects.filter(toUser=obj.tacitrecord.user)
        if viewernotify_obj.exists():
            viewernotify_obj.update(tacit_write_count=F("tacit_write_count") + 1)
        else:
            viewernotify_obj.create(toUser=obj.tacitrecord.user, tacit_write_count=1)

        exists = viewer_object.exists()
        if exists:
            viewer_object.update(write_count=F("write_count") + 1, create_time=timezone.now())
            models.UserInfo.objects.filter(id=obj.tacitrecord.user_id).update(tacit_write_count=F("tacit_write_count") + 1)
            models.Notification.objects.create(notificationType=42, fromUser=self.request.user,
                                               toUser=obj.tacitrecord.user, tacit=obj.tacitrecord, userHasChecked=True)
        else:
            viewer_object.create(user=obj.tacitrecord.user, viewer_user=self.request.user, tacitRecord=obj.tacitrecord,
                             write_count=1, create_time=timezone.now(), source="坦白局")
            models.UserInfo.objects.filter(id=obj.tacitrecord.user_id).update(tacit_write_count=F("tacit_write_count") + 1)
            models.Notification.objects.create(notificationType=42, fromUser=self.request.user,
                                           toUser=obj.tacitrecord.user, tacit=obj.tacitrecord, userHasChecked=True)

class SubmitAskAnythingView(CreateAPIView):
    '''保存评论 同时更新瞬间里面的评论数'''
    serializer_class = askAnything.SubmitAskAnythingModelSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        '''
        1.判断匿名 给定avatar
        2.
        '''
        if (int(self.request.data.get("comment_status")) == 1):
            obj_1 = models.AskAnythingRecord.objects.filter(
                user=self.request.user,
                tacitrecord_id=self.request.data.get("tacitrecord"),
                comment_status=1
            ).order_by("id")
            if obj_1.exists():
                obj_1 = obj_1.first()
                nickName=obj_1.nickName
                avatarUrl=obj_1.avatarUrl
            else:
                nickName = getRandomName()
                avatarUrl = getMosaic()
            obj = serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            tacitrecord_id = serializer.data.get("tacitrecord")
            models.TacitRecord.objects.filter(id=tacitrecord_id).update(comment_count=F('comment_count') + 1)
        else:
            obj_0 = models.AskAnythingRecord.objects.filter(
                user=self.request.user,
                tacitrecord_id=self.request.data.get("tacitrecord"),
                comment_status=0
            ).order_by("id")
            if obj_0.exists():
                obj_0_0 = obj_0.first()
                nickName=obj_0_0.nickName
                avatarUrl=obj_0_0.avatarUrl
            else:
                moment_obj = models.TacitRecord.objects.filter(id=self.request.data.get("tacitrecord")).first()
                if self.request.user.id == moment_obj.user.id:
                    nickName = moment_obj.user.real_nickName
                    avatarUrl = moment_obj.user.real_avatarUrl
                else:
                    nickName, avatarUrl = getNameAvatarlist()
            obj=serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            tacitrecord_id = serializer.data.get("tacitrecord")
            models.TacitRecord.objects.filter(id=tacitrecord_id).update(comment_count=F('comment_count') + 1)
        # 统计浏览记录
        ask_obj = models.AskAnythingRecord.objects.get(id=self.request.data.get("root")).first()
        models.Notification.objects.create(notificationType=43, fromUser=self.request.user,toUser=ask_obj.user, tacit=obj.tacitrecord, userHasChecked=True)

class AskMeAnythingDetailView(RetrieveAPIView):
    '''
    获取单条瞬间详细
    '''
    queryset = models.TacitRecord.objects
    authentication_classes = [GeneralAuthentication,]
    serializer_class = askAnything.AskMeAnythingDetailModelSerializer

    def get(self, request, *args, **kwargs):
        response = super().get(self, request, *args, **kwargs)
        #验证用户是否登入：登陆增加浏览记录，未登录不进行操作
        #获取AUTHORIZATION
        if not request.user:
            return response
        moment_object = self.get_object()
        if int(moment_object.user.id) is int(request.user.id):
            return response
        return response

class AskMeAnythingCommentView(ListAPIView):
    queryset = models.AskAnythingRecord.objects.all().order_by('-id')
    serializer_class = askAnything.AskMeAnythingCommentModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinCommentFilterBackend, filter.MaxCommentFilterBackend]

    def get_queryset(self):
        tacitrecord_id = self.request.query_params.get("tacitrecord")
        queryset = models.AskAnythingRecord.objects.filter(tacitrecord_id=int(tacitrecord_id),depth=1).all().order_by("-id")
        # queryset = models.AskAnythingRecord.objects.all().order_by("-id")
        return queryset

class AskAnythingFavorView(APIView):
    '''
    评论点赞更新
    '''
    def get_authenticators(self):
        if self.request.method =="POST":
            return [UserAuthentication(),]
        return [GeneralAuthentication(),]

    def post(self,request,*args,**kwargs):
        '''
        1.验证评论ID是否存在
        2.获取评论ID
        3.查看被赞评论记录是否存在当前用户记录
        4.如果存在 删除；如果不存在 创建
        '''
        ser = askAnything.AskAnythingFavorModelSerializer(data=request.data)
        if not ser.is_valid():
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        askAnythingRecord_object = ser.validated_data.get("askAnythingRecord")
        if askAnythingRecord_object.user.id is request.user.id:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        askAnythingRecord_obj = models.AskAnythingFavorRecord.objects.filter(user=request.user,askAnythingRecord=askAnythingRecord_object)
        exist = askAnythingRecord_obj.exists()
        if exist:
            askAnythingRecord_obj.delete()
            com_obj = models.AskAnythingRecord.objects.filter(id = askAnythingRecord_object.id)
            com_obj.update(favor_count=F('favor_count')-1)
            return Response({}, status=status.HTTP_200_OK)
        askAnythingRecord_obj.create(user=request.user,askAnythingRecord=askAnythingRecord_object)
        com_obj = models.AskAnythingRecord.objects.filter(id=askAnythingRecord_object.id)
        com_obj.update(favor_count=F('favor_count') + 1)
        return Response({}, status=status.HTTP_201_CREATED)

