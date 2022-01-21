from rest_framework.generics import ListAPIView,CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import F

from api.serializer import comment
from api import models

from utils import filter,pagination
from utils.auth import GeneralAuthentication,UserAuthentication
from utils.randomName import getNameAvatarlist,getMosaic,getRandomName,getRandomAvatar

'''评论模块'''
class CreateCommentView(CreateAPIView):
    '''保存评论 同时更新瞬间里面的评论数'''
    serializer_class = comment.CreateCommentSerializer
    authentication_classes = [UserAuthentication,]

    def perform_create(self, serializer):
        '''
        1.判断匿名 给定avatar
        2.
        '''
        if (self.request.data.get("comment_status") == 1):
            obj_1 = models.CommentRecord.objects.filter(
                user=self.request.user,
                moment_id=self.request.data.get("moment"),
                comment_status=1
            ).order_by("id")
            if obj_1.exists():
                obj_1 = obj_1.first()
                nickName=obj_1.nickName
                avatarUrl=obj_1.avatarUrl
            else:
                nickName = getRandomName()
                avatarUrl = getMosaic()
            com_obj = serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            moment_id = serializer.data.get("moment")
            models.Moment.objects.filter(id=moment_id).update(comment_count=F('comment_count') + 1)
        else:
            obj_0 = models.CommentRecord.objects.filter(
                user=self.request.user,
                moment_id=self.request.data.get("moment"),
                comment_status=0
            ).order_by("id")
            if obj_0.exists():
                obj_0_0 = obj_0.first()
                nickName=obj_0_0.nickName
                avatarUrl=obj_0_0.avatarUrl
            else:
                moment_obj = models.Moment.objects.filter(id=self.request.data.get("moment")).first()
                if self.request.user.id == moment_obj.user.id:
                    nickName = "楼主"
                    avatarUrl = moment_obj.user.avatarUrl
                else:
                    nickName, avatarUrl = getNameAvatarlist()
            com_obj = serializer.save(user=self.request.user, nickName=nickName, avatarUrl=avatarUrl)
            moment_id = serializer.data.get("moment")
            models.Moment.objects.filter(id=moment_id).update(comment_count=F('comment_count') + 1)
        #如果存在回复的人，通知回复的人；同时通知这一层楼主
        if com_obj.reply:
            if self.request.user.id is not com_obj.reply.user.id:
                models.Notification.objects.create(notificationType=21,fromUser=self.request.user,toUser=com_obj.reply.user,
                                               moment=com_obj.moment,comment=com_obj,userHasChecked=True)
            if com_obj.depth > 2:
                if self.request.user.id is not com_obj.root.user.id and com_obj.root.user.id is not com_obj.reply.user.id:
                    models.Notification.objects.create(notificationType=22, fromUser=self.request.user,
                                                   toUser=com_obj.root.user,
                                                   moment=com_obj.moment, comment=com_obj,userHasChecked=True)
            if self.request.user.id is not com_obj.moment.user.id:
                if com_obj.moment.user.id is not com_obj.reply.user.id and com_obj.moment.user.id is not com_obj.root.user.id:
                    models.Notification.objects.create(notificationType=23, fromUser=self.request.user,
                                                       toUser=com_obj.moment.user,
                                                       moment=com_obj.moment, comment=com_obj,userHasChecked=True)

        else:
            # 通知发瞬间的楼主
            if self.request.user.id is not com_obj.moment.user.id:
                models.Notification.objects.create(notificationType=23, fromUser=self.request.user,
                                                toUser=com_obj.moment.user,
                                                moment=com_obj.moment, comment=com_obj,userHasChecked=True)

class exampleCreateCommentView(APIView):
    def post(self, request, *args, **kwargs):
        '''
        1.验证
        2.存入数据库
        3.返回最新数据
        '''
        ser = comment.CreateCommentSerializer(data=request.data)
        if(ser.is_valid()):
            ser.save(user_id=1)
            new_object = ser.data.get("moment")
            models.Moment.objects.filter(id=new_object).update(comment_count=F('comment_count')+1)
            return Response(ser.data)
        return Response(ser.errors)


class CommentView(ListAPIView):
    '''
    评论下滑更新
    '''
    queryset = models.CommentRecord.objects.all().order_by('-id')
    serializer_class = comment.GetCommentSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinCommentFilterBackend,filter.MaxCommentFilterBackend]

class CommentFavorView(APIView):
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
        ser = comment.CommentFavorSerializer(data=request.data)
        if not ser.is_valid():
            return Response({},status=status.HTTP_400_BAD_REQUEST)
        commentRecord_object = ser.validated_data.get("commentRecord")
        if commentRecord_object.user.id is request.user.id:
            return Response({}, status=status.HTTP_204_NO_CONTENT)
        commentFavorRecord_object = models.CommentFavorRecord.objects.filter(user=request.user,commentRecord=commentRecord_object)
        exist = commentFavorRecord_object.exists()
        if exist:
            commentFavorRecord_object.delete()
            com_obj = models.CommentRecord.objects.filter(id = commentRecord_object.id)
            com_obj.update(favor_count=F('favor_count')-1)
            com_obj = com_obj.first()
            models.Notification.objects.filter(notificationType=12, fromUser=self.request.user,
                                               toUser=com_obj.user,
                                               moment=com_obj.moment,comment=com_obj, userHasChecked=True).delete()
            return Response({}, status=status.HTTP_200_OK)
        commentFavorRecord_object.create(user=request.user,commentRecord=commentRecord_object)
        com_obj = models.CommentRecord.objects.filter(id=commentRecord_object.id)
        com_obj.update(favor_count=F('favor_count') + 1)
        com_obj = com_obj.first()
        models.Notification.objects.create(notificationType=12, fromUser=self.request.user,
                                           toUser=com_obj.user,
                                           moment=com_obj.moment,comment=com_obj, userHasChecked=True)
        return Response({}, status=status.HTTP_201_CREATED)
'''
    def put(self,request,pk):
        queryset =models.CommentRecord.objects.get(pk=pk)
        ser = comment.CommentFavorSerializer(instance=queryset,data=request.data)
        ser.is_valid(raise_exception=True)
        instance = ser.save()
        comment.CommentFavorSerializer(instance=instance)
        return Response(ser.data, status=status.HTTP_201_CREATED)
'''
