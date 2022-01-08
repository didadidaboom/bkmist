import datetime

from django.db import models
from utils.geo import GeohashField, GeoManager

'''
CASCADE: When the referenced object is deleted, also delete the objects that have references to it
PROTECT: Forbid the deletion of the referenced object
SET NULL: Set the reference to NULL
'''

'''用户'''
class UserInfo(models.Model):
    nickName = models.CharField(verbose_name="用户昵称",max_length=255)
    real_nickName = models.CharField(verbose_name="用户昵称", max_length=255,null=True,blank=True)
    avatarUrl = models.CharField(verbose_name="用户头像",max_length=255)
    real_avatarUrl = models.CharField(verbose_name="微信用户头像", max_length=255,null=True,blank=True)
    gender_choice = (
        (0, "女"),
        (1, "男"),
    )
    gender = models.SmallIntegerField(verbose_name="性别", default=0, choices=gender_choice)
    openID = models.CharField(verbose_name="openID",max_length=255,unique=True)
    phone = models.CharField(verbose_name="手机号", max_length=11,null=True,blank=True)
    token = models.CharField(verbose_name="用户TOKEN", max_length=64, null=True, blank=True)
    create_date=models.DateTimeField(verbose_name="用户注册时间",auto_now_add=True)
    focus_count = models.PositiveIntegerField(verbose_name="关注次数", default=0)
    focused_count = models.PositiveIntegerField(verbose_name="被关注次数", default=0)
    viewer_count = models.PositiveIntegerField(verbose_name="被看次数", default=0)
    viewer_count_page2 = models.PositiveIntegerField(verbose_name="我的独白被看次数", default=0)
    viewer_count_page3 = models.PositiveIntegerField(verbose_name="朋友眼中的我被看次数", default=0)
    tacit_viewer_count = models.PositiveIntegerField(verbose_name="好友测试扫码次数", default=0)
    tacit_write_count = models.PositiveIntegerField(verbose_name="好友测试填写次数", default=0)

    class Meta:
        db_table = "userinfo"
        verbose_name = "话题"
        verbose_name_plural = verbose_name

class UserFocusRecord(models.Model):
    user = models.ForeignKey(verbose_name="被关注的用户",to="UserInfo",related_name="user_focus",on_delete=models.CASCADE)
    focus_user = models.ForeignKey(verbose_name="关注的用户",to="UserInfo",related_name="focus_user_focus",on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="用户被关在的时间",auto_now_add=True)
    class Meta:
        db_table = "user_focus_record"
        verbose_name = "用户关注记录"
        verbose_name_plural = verbose_name

class UserBlacklistRecord(models.Model):
    user = models.ForeignKey(verbose_name="被拉黑的用户", to="UserInfo", related_name="user_blacklist",on_delete=models.CASCADE)
    reject_user = models.ForeignKey(verbose_name="拉黑的用户", to="UserInfo", related_name="reject_user_blacklist", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="用户拉黑的时间", auto_now_add=True)

    class Meta:
        db_table = "user_blacklist_record"
        verbose_name = "用户拉黑记录"
        verbose_name_plural = verbose_name

class UserViewerRecord(models.Model):
    user = models.ForeignKey(verbose_name="被浏览的用户", to="UserInfo", related_name="user_viewer",null=True,blank=True,on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="浏览的用户", to="UserInfo", related_name="viewer_user_viewer",null=True,blank=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="用户浏览的时间",auto_now_add=True)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览次数", default=0)

    class Meta:
        db_table = "user_viewer_record"
        verbose_name = "用户浏览记录"
        verbose_name_plural = verbose_name

class UserViewerRecordPage2(models.Model):
    user = models.ForeignKey(verbose_name="被浏览的用户", to="UserInfo", related_name="user_viewer_page2",null=True,blank=True,on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="浏览的用户", to="UserInfo", related_name="viewer_user_viewer_page2",null=True,blank=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="用户浏览的时间",auto_now_add=True)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览次数", default=0)
    class Meta:
        db_table = "user_viewer_record_page2"
        verbose_name = "我的独白浏览记录"
        verbose_name_plural = verbose_name

class UserViewerRecordPage3(models.Model):
    user = models.ForeignKey(verbose_name="被浏览的用户", to="UserInfo", related_name="user_viewer_page3",null=True,blank=True,on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="浏览的用户", to="UserInfo", related_name="viewer_user_viewer_page3",null=True,blank=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="用户浏览的时间",auto_now_add=True)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览次数", default=0)
    class Meta:
        db_table = "user_viewer_record_page3"
        verbose_name = "朋友眼中的我浏览记录"
        verbose_name_plural = verbose_name

'''话题'''
class TopicInfo(models.Model):
    title = models.CharField(max_length=100,verbose_name="话题名",help_text="提示文本:账号不能为空！",unique=True)
    user = models.ForeignKey(verbose_name="话题创建用户",to="UserInfo",null=True,blank=True,on_delete=models.SET_NULL)
    description = models.CharField(max_length=255,verbose_name="描述")
    focus_count = models.PositiveIntegerField(verbose_name="话题关注次数",default=0)
    viewer_count = models.PositiveIntegerField(verbose_name="话题浏览次数", default=0)
    cited_count = models.PositiveIntegerField(verbose_name="话题引用次数", default=0)
    create_date = models.DateTimeField(verbose_name="话题创建时间",auto_now_add=True)

    class Meta:
        db_table = "topicinfo"
        verbose_name = "话题"
        verbose_name_plural = verbose_name

class TopicViewerRecord(models.Model):
    topic = models.ForeignKey(verbose_name="话题", to="TopicInfo",on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="话题浏览的时间", auto_now_add=True)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览次数", default=0)

    class Meta:
        db_table = "topic_viewer_record"
        verbose_name = "话题浏览记录"
        verbose_name_plural = verbose_name

class TopicFocusRecord(models.Model):
    topic = models.ForeignKey(verbose_name="话题", to="TopicInfo",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="话题浏览的时间", auto_now_add=True)

    class Meta:
        db_table = "topic_focus_record"
        verbose_name = "话题关注记录"
        verbose_name_plural = verbose_name

class TopicCitedRecord(models.Model):
    topic = models.ForeignKey(verbose_name="话题", to="TopicInfo",on_delete=models.CASCADE)
    #user = models.ForeignKey(verbose_name="用户", to="UserInfo",on_delete=models.CASCADE)
    moment = models.ForeignKey(verbose_name="瞬间", to="Moment",on_delete=models.CASCADE)
    #create_time = models.DateTimeField(verbose_name="话题应用的时间", auto_now_add=True)

    class Meta:
        db_table = "topic_cited_record"
        verbose_name = "话题引用记录"
        verbose_name_plural = verbose_name

class AddressFocusRecord(models.Model):
    address = models.ForeignKey(verbose_name="位置", to="Address",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="用户", to="UserInfo", on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="关注的时间", auto_now_add=True)

    class Meta:
        db_table = "address_focus_record"
        verbose_name = "位置关注记录"
        verbose_name_plural = verbose_name

class Address(models.Model):
    '''
    位置
    '''
    address = models.CharField(verbose_name="瞬间发布的位置", max_length=100, null=True, blank=True)
    addressName = models.CharField(verbose_name="瞬间发布的位置名称", max_length=100, null=True, blank=True)
    latitude = models.CharField(verbose_name="纬度", max_length=100, null=True, blank=True)
    longitude = models.CharField(verbose_name="经度", max_length=100, null=True, blank=True)
    #addressGeohash = models.ForeignKey(verbose_name="Geohash",to="AddressGeohash",related_name="addressGeo",on_delete=models.CASCADE)
    moment = models.ForeignKey(verbose_name="瞬间的ID", to="Moment", related_name="address",
                               on_delete=models.CASCADE)

    class Meta:
        db_table = "moment_address"
        verbose_name="位置"
        verbose_name_plural=verbose_name



class Moment(models.Model):
    '''
    瞬间
    '''
    content = models.CharField(verbose_name="瞬间内容",max_length=255)
    #topic = models.ForeignKey(verbose_name="话题",to="TopicInfo", null=True,blank=True,on_delete=models.SET_NULL)
    #address = models.CharField(verbose_name="瞬间发布的位置",max_length=100,null=True,blank=True)
    #addressName = models.CharField(verbose_name="瞬间发布的位置名称", max_length=100, null=True, blank=True)
    #latitude = models.CharField(verbose_name="纬度", max_length=100, null=True, blank=True)
    #longitude = models.CharField(verbose_name="经度", max_length=100, null=True, blank=True)
    user = models.ForeignKey(verbose_name="用户",to="UserInfo",related_name="user_moment",null=True,blank=True,on_delete=models.CASCADE)

    favor_count = models.PositiveIntegerField(verbose_name="点赞数",default=0)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览量",default=0)
    comment_count = models.PositiveIntegerField(verbose_name="评论量",default=0)
    share_count = models.PositiveIntegerField(verbose_name="分享量", default=0)
    create_date = models.DateTimeField(verbose_name="瞬间发布日期",auto_now_add=True)
    #create_date = models.DateTimeField(verbose_name="瞬间发布日期", default=timezone.now)
    if_status_choice = (
        (0,"显示"),
        (1,"条件隐身"),
    )
    if_status = models.SmallIntegerField(verbose_name="显示状态",default=0,choices=if_status_choice)
    moment_status_choice = (
        (0, "广场可见"),
        (1, "主页可见"),
        (2, "个人可见"),
    )
    moment_status = models.SmallIntegerField(verbose_name="控制状态",default=0, choices=moment_status_choice)

    class Meta:
        db_table = "moment"
        verbose_name = "瞬间"
        verbose_name_plural = verbose_name

class MomentDetail(models.Model):
    '''
    瞬间相应的图片
    '''
    path = models.CharField(verbose_name="URL地址",max_length=1000,null=True,blank=True)
    path_key = models.CharField(verbose_name="图片名",max_length=1000,null=True,blank=True)
    moment = models.ForeignKey(verbose_name="瞬间的ID",to="Moment",related_name="moment_detail",on_delete=models.CASCADE)

    class Meta:
        db_table = "moment_detail"
        verbose_name="瞬间图片"
        verbose_name_plural=verbose_name

class MomentViewerRecord(models.Model):
    '''
    瞬间浏览记录
    '''
    moment = models.ForeignKey(verbose_name="浏览的瞬间",to="Moment",on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="浏览用户",to="UserInfo",null= True,blank=True,on_delete=models.SET_NULL)
    create_time = models.DateTimeField(verbose_name="最近浏览日期", auto_now=True)
    viewer_count = models.PositiveIntegerField(verbose_name="浏览次数", default=0)

    class Meta:
        db_table = "moment_viewer_record"
        verbose_name = "瞬间浏览记录"
        verbose_name_plural = verbose_name

class MomentFavorRecord(models.Model):
    '''
    瞬间的喜欢记录
    '''
    moment = models.ForeignKey(verbose_name="被喜欢的瞬间",to="Moment",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="喜欢瞬间的用户", to="UserInfo", null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(verbose_name="瞬间喜欢时间",auto_now_add=True)

    class Meta:
        db_table = "moment_favor_record"
        verbose_name = "瞬间喜欢记录"
        verbose_name_plural = verbose_name

class MomentShareRecord(models.Model):
    moment = models.ForeignKey(verbose_name="被分享的瞬间",to="Moment",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="分享瞬间的用户", to="UserInfo", null=True, blank=True, on_delete=models.SET_NULL)
    create_date = models.DateTimeField(verbose_name="瞬间喜欢时间",auto_now_add=True)

    class Meta:
        db_table = "moment_share_record"
        verbose_name = "瞬间分享记录"
        verbose_name_plural = verbose_name

class CommentRecord(models.Model):
    '''
    用户评论记录
    '''
    moment = models.ForeignKey(verbose_name="评论的瞬间",to="Moment",on_delete=models.CASCADE)
    content = models.CharField(verbose_name="评论内容",max_length=255)
    user = models.ForeignKey(verbose_name="评论用户",to="UserInfo",null=True,blank=True,on_delete=models.CASCADE)
    nickName = models.CharField(verbose_name="随机名字",max_length=255,null=True,blank=True)
    avatarUrl = models.CharField(verbose_name="随机头像", max_length=1000,null=True,blank=True)
    reply = models.ForeignKey(verbose_name="回复评论ID",to="self",null=True,blank=True,related_name="replys",on_delete=models.CASCADE)
    depth = models.PositiveIntegerField(verbose_name="评论深度",default=1)
    root = models.ForeignKey(verbose_name="评论根ID",to="self",null=True,blank=True,related_name="roots",on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="评论时间", auto_now_add=True)
    comment_status_choice = (
        (0, "显示"),
        (1, "条件隐身")
    )
    comment_status = models.SmallIntegerField(verbose_name="评论状态",default=0,choices=comment_status_choice)
    favor_count = models.PositiveIntegerField(verbose_name="评论赞数",default=0)

    class Meta:
        db_table = "comment_record"
        verbose_name = "瞬间评论"
        verbose_name_plural = verbose_name

class CommentFavorRecord(models.Model):
    commentRecord = models.ForeignKey(verbose_name="被赞的评论", to="CommentRecord", on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="评论被赞的时间", auto_now_add=True)
    user = models.ForeignKey(verbose_name="赞评论的用户", to="UserInfo", null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        db_table = "comment_favor_record"
        verbose_name = "被赞评论的记录"
        verbose_name_plural = verbose_name

class TacitTestDatabase(models.Model):
    title = models.CharField(verbose_name="题目", max_length=255)
    answer1 = models.CharField(verbose_name="回答1", max_length=255)
    answer2 = models.CharField(verbose_name="回答2", max_length=255, null=True, blank=True)
    answer3 = models.CharField(verbose_name="回答3", max_length=255, null=True, blank=True)
    answer4 = models.CharField(verbose_name="回答4", max_length=255, null=True, blank=True)
    answer5 = models.CharField(verbose_name="回答5", max_length=255, null=True, blank=True)
    create_date = models.DateTimeField(verbose_name="默契测试创建日期", auto_now_add=True)

    class Meta:
        db_table = "tacit_test"
        verbose_name = "默契测试"
        verbose_name_plural = verbose_name

class TacitRecord(models.Model):
    user = models.ForeignKey(verbose_name="好友测试创建者", to="UserInfo",on_delete=models.CASCADE)
    comment_count = models.PositiveIntegerField(verbose_name="评论次数", default=0)
    bonus_choice = (
        (0, "无"),
        (1, "随机")
    )
    bonus = models.SmallIntegerField(verbose_name="奖励",default=0,choices=bonus_choice)
    correct_count = models.PositiveIntegerField(verbose_name="给定答对可获得奖励的数量",default=0)
    avatar_choice = (
        (0, "随机头像"),
        (1, "微信头像")
    )
    avatarUrlFlag = models.SmallIntegerField(verbose_name="头像类型",default=0,choices=avatar_choice)
    tacit_status_choice = (
        (0, "广场可见"),
        (1, "主页可见"),
        (2, "个人可见"),
    )
    tacit_status = models.SmallIntegerField(verbose_name="控制状态", default=0, choices=tacit_status_choice)
    tacit_reply_status_choice = (
        (0, "广场可见"),
        (1, "主页可见"),
        (2, "个人可见"),
    )
    tacit_reply_status = models.SmallIntegerField(verbose_name="回复控制状态", default=0, choices=tacit_reply_status_choice)
    create_date = models.DateTimeField(verbose_name="使用日期", auto_now_add=True)

    class Meta:
        db_table = "tacit_record"
        verbose_name = "默契记录"
        verbose_name_plural = verbose_name

class TacitCitedRecord(models.Model):
    tacitRecord = models.ForeignKey(verbose_name="默契测试记录",to="TacitRecord",on_delete=models.CASCADE)
    tacitTestDatabase = models.ForeignKey(verbose_name="默契测试题库",to="TacitTestDatabase",on_delete=models.CASCADE)
    selected_answer = models.CharField(verbose_name="创建者设定的答案", max_length=255,null=True,blank=True)

    class Meta:
        db_table = "tacit_cited_record"
        verbose_name = "默契引用记录"
        verbose_name_plural = verbose_name

class TacitReplyRecord(models.Model):
    tacitRecord = models.ForeignKey(verbose_name="默契测试",to="TacitRecord",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="默契测试回复者", to="UserInfo",on_delete=models.CASCADE)
    bonus = models.CharField(verbose_name="奖励", max_length=255, null=True, blank=True)
    avatar_choice = (
        (0, "随机头像"),
        (1, "微信头像")
    )
    avatarUrlFlag = models.SmallIntegerField(verbose_name="头像类型",default=0,choices=avatar_choice)
    match_count = models.PositiveIntegerField(verbose_name="匹配数", default=0)
    if_status_choice = (
        (0, "显示"),
        (1, "条件隐身"),
    )
    if_status = models.SmallIntegerField(verbose_name="条件隐身状态", default=0, choices=if_status_choice)
    favor_count = models.PositiveIntegerField(verbose_name="被点赞次数", default=0)
    create_date = models.DateTimeField(verbose_name="使用日期", auto_now_add=True)

    class Meta:
        db_table = "tacit_reply_record"
        verbose_name = "默契回复记录"
        verbose_name_plural = verbose_name

class TacitReplyViewer(models.Model):
    user = models.ForeignKey(verbose_name="被浏览的用户", to="UserInfo", related_name="tacit_reply_viewer",null=True,blank=True,on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="浏览的用户", to="UserInfo", related_name="viewer_tacit_reply_viewer",null=True,blank=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="用户浏览的时间",auto_now_add=True)
    viewer_count = models.PositiveIntegerField(verbose_name="填写次数", default=0)
    source = models.CharField(max_length=100, verbose_name="来源",null=True,blank=True)

    class Meta:
        db_table = "tacit_reply_viewer"
        verbose_name = "好友默契回复扫码记录"
        verbose_name_plural = verbose_name

class TacitReplyWrite(models.Model):
    user = models.ForeignKey(verbose_name="被浏览的用户", to="UserInfo", related_name="tacit_reply_write",null=True,blank=True,on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="浏览的用户", to="UserInfo", related_name="viewer_tacit_reply_write",null=True,blank=True, on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="用户浏览的时间",auto_now_add=True)
    write_count = models.PositiveIntegerField(verbose_name="填写次数", default=0)
    source = models.CharField(max_length=100, verbose_name="来源",null=True,blank=True)

    class Meta:
        db_table = "tacit_reply_write"
        verbose_name = "好友默契回复填写完成记录"
        verbose_name_plural = verbose_name

class TacitReplyCitedRecord(models.Model):
    tacitReplyRecord = models.ForeignKey(verbose_name="回复默契测试记录",to="TacitReplyRecord",on_delete=models.CASCADE)
    selected_answer = models.CharField(verbose_name="回复设定的答案", max_length=255,null=True,blank=True)

    class Meta:
        db_table = "tacit_reply_cited_record"
        verbose_name = "回复默契引用记录"
        verbose_name_plural = verbose_name