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
    last_login = models.DateTimeField(verbose_name="最近登陆",auto_now=True)
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

class AddressGeohash(models.Model):
    address = models.ForeignKey(verbose_name="address",to="Address",related_name="addressGeo",on_delete=models.CASCADE)
    location = GeohashField(null=True)
    objects = GeoManager()

    class Meta:
        db_table = "address_geohash"
        verbose_name = "位置geohash"
        verbose_name_plural = verbose_name

class Address(models.Model):
    address = models.CharField(verbose_name="瞬间发布的位置", max_length=100, null=True, blank=True)
    addressName = models.CharField(verbose_name="瞬间发布的位置名称", max_length=100, null=True, blank=True)
    latitude = models.CharField(verbose_name="纬度", max_length=100, null=True, blank=True)
    longitude = models.CharField(verbose_name="经度", max_length=100, null=True, blank=True)

    class Meta:
        db_table = "address"
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

class MomentCiteAddressRecord(models.Model):
    address = models.ForeignKey(verbose_name="位置", to="Address",on_delete=models.CASCADE)
    moment = models.ForeignKey(verbose_name="瞬间", to="Moment",on_delete=models.CASCADE)

    class Meta:
        db_table = "moment_cite_address_record"
        verbose_name = "瞬间引用坐标记录"
        verbose_name_plural = verbose_name

class MomentViewerRecord(models.Model):
    '''
    瞬间浏览记录
    '''
    moment = models.ForeignKey(verbose_name="浏览的瞬间",to="Moment",on_delete=models.CASCADE)
    viewer_user = models.ForeignKey(verbose_name="浏览用户",to="UserInfo",on_delete=models.CASCADE)
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
    user = models.ForeignKey(verbose_name="喜欢瞬间的用户", to="UserInfo", on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="瞬间喜欢时间",auto_now_add=True)

    class Meta:
        db_table = "moment_favor_record"
        verbose_name = "瞬间喜欢记录"
        verbose_name_plural = verbose_name

class MomentShareRecord(models.Model):
    moment = models.ForeignKey(verbose_name="被分享的瞬间",to="Moment",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="分享瞬间的用户", to="UserInfo",on_delete=models.CASCADE)
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
    user = models.ForeignKey(verbose_name="赞评论的用户", to="UserInfo", on_delete=models.CASCADE)

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
    #10001 好友测试问答; 20001 坦白局
    type = models.IntegerField(null=True,blank=True)
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

class AskAnythingRecord(models.Model):
    '''
    坦白局记录
    '''
    tacitrecord = models.ForeignKey(verbose_name="我的独白记录",to="TacitRecord",on_delete=models.CASCADE)
    content = models.CharField(verbose_name="提问内容",max_length=255)
    user = models.ForeignKey(verbose_name="提问用户",to="UserInfo",null=True,blank=True,on_delete=models.CASCADE)
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
        db_table = "ask_anything_record"
        verbose_name = "坦白局"
        verbose_name_plural = verbose_name

class AskAnythingFavorRecord(models.Model):
    askAnythingRecord = models.ForeignKey(verbose_name="被赞的评论", to="AskAnythingRecord", on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="评论被赞的时间", auto_now_add=True)
    user = models.ForeignKey(verbose_name="赞评论的用户", to="UserInfo", on_delete=models.CASCADE)

    class Meta:
        db_table = "ask_anything_favor_record"
        verbose_name = "被赞坦白局评论的记录"
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

class TacitReplyFavorRecord(models.Model):
    '''
    瞬间的喜欢记录
    '''
    tacitReplyRecord = models.ForeignKey(verbose_name="回复默契测试记录",to="TacitReplyRecord",on_delete=models.CASCADE)
    user = models.ForeignKey(verbose_name="喜欢好友回复评论的用户", to="UserInfo",on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name="瞬间喜欢时间",auto_now_add=True)

    class Meta:
        db_table = "tacit_reply_favor_record"
        verbose_name = "好友默契回复被喜欢的记录"
        verbose_name_plural = verbose_name

class TacitReplyViewer(models.Model):
    tacitRecord = models.ForeignKey(verbose_name="默契测试", to="TacitRecord",on_delete=models.CASCADE)
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
    tacitRecord = models.ForeignKey(verbose_name="默契测试", to="TacitRecord",on_delete=models.CASCADE)
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

class Notification(models.Model):
    # 11 like moment, 12 like comment, 13 like tacit reply
    # 21 comment reply, 22 comment root, 23 comment moment
    # 31 follow you, 32 cancel follow
    # 41 reply tacit, 42 reply askme, 43 comment reply of askme
    # 51 invite publish moment, 52 invite publish tacit
    # 61 cancel like moment, 62 cancel like comment, 63 cancel like tacit
    notificationType = models.IntegerField()
    toUser = models.ForeignKey(verbose_name="to user",to="UserInfo",related_name="notification_to",null=True,on_delete=models.CASCADE)
    fromUser = models.ForeignKey(verbose_name="from user",to="UserInfo",related_name="notification_from",null=True,on_delete=models.CASCADE)
    moment = models.ForeignKey(verbose_name="瞬间的一级评论",to="Moment",related_name="+",null=True,blank=True,on_delete=models.CASCADE)
    comment = models.ForeignKey(verbose_name="回复评论",to="CommentRecord",related_name="+",null=True,blank=True,on_delete=models.CASCADE)
    tacit = models.ForeignKey(verbose_name="回复默契测试",to="TacitRecord",related_name="+",null=True,blank=True,on_delete=models.CASCADE)
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    userHasChecked = models.BooleanField(default=False)

    class Meta:
        db_table = "notification"
        verbose_name = "消息通知"
        verbose_name_plural = verbose_name

class ViewerNotification(models.Model):
    toUser = models.ForeignKey(verbose_name="to user", to="UserInfo", related_name="viewernotification_to", null=True,blank=True,on_delete=models.CASCADE)
    focused_count = models.PositiveIntegerField(verbose_name="自己被关注次数", default=0)
    viewer_count_page1 = models.PositiveIntegerField(verbose_name="个人瞬间页被看次数", default=0)
    viewer_count_page2 = models.PositiveIntegerField(verbose_name="我的独白被看次数", default=0)
    viewer_count_page3 = models.PositiveIntegerField(verbose_name="朋友眼中的我被看次数", default=0)
    tacit_viewer_count = models.PositiveIntegerField(verbose_name="好友测试扫码次数", default=0)
    tacit_write_count = models.PositiveIntegerField(verbose_name="好友测试填写次数", default=0)

    class Meta:
        db_table = "viewernotification"
        verbose_name = "个人浏览通知"
        verbose_name_plural = verbose_name

class MomentViewerNotification(models.Model):
    moment = models.ForeignKey(verbose_name="瞬间的一级评论", to="Moment", related_name="+", null=True, blank=True,on_delete=models.CASCADE)
    momentviewer_count = models.PositiveIntegerField(verbose_name="瞬间浏览量", default=0)

    class Meta:
        db_table = "momentviewernotification"
        verbose_name = "瞬间浏览通知"
        verbose_name_plural = verbose_name

class PreSystem(models.Model):
    # 10001: 没登陆的时候的系统消息
    # 20001: 登陆后的第一条系统消息
    # 30001: 自由
    type = models.IntegerField()
    content = models.CharField(verbose_name="通知内容",max_length=350)
    class Meta:
        db_table = "presystem"
        verbose_name = "系统消息"
        verbose_name_plural = verbose_name

class SystemNotification(models.Model):
    toUser = models.ForeignKey(verbose_name="to user", to="UserInfo", related_name="system_notification_to", null=True, on_delete=models.CASCADE)
    preSystem = models.ForeignKey(verbose_name="系统消息",to="PreSystem",null=True,on_delete=models.CASCADE)
    userHasChecked = models.BooleanField(default=False)
    create_time = models.DateTimeField(verbose_name="创建时间", auto_now_add=True)

    class Meta:
        db_table = "systemnotification"
        verbose_name = "系统消息通知"
        verbose_name_plural = verbose_name

class PersonalData(models.Model):
    #p-page1:1001; p-viewer1:1002; p-focus:1003; p-focused:1004; p-moment:1005; p-setting:1006; p-friend:1007; p-focuspage:1008
    #p-page2:2001; p-viewer2:2002
    #p-page3:3001; p-viewer3:3002; p-scan:3003; p-submit:3004;
    #p-mail1:4001; p-mail2:4002; p-mail3:4003
    curUser = models.ForeignKey(verbose_name="current user", to="UserInfo", null=True, on_delete=models.CASCADE)
    type = models.IntegerField()
    count = models.PositiveIntegerField(verbose_name="次数", default=0)
    latest_time = models.DateTimeField(verbose_name="最近时间", auto_now_add=True)

    class Meta:
        db_table = "personaldata"
        verbose_name = "个人页数据"
        verbose_name_plural = verbose_name


class PagesData(models.Model):
    #o-index:5001; o-publish:5002; o-play:5003; o-tacit:5004; o-askanything:5005
    #o-topic1:6001; o-topic2:6002; o-topic3:6003; o-topic4:6004
    #o-addr1:7001; o-addr2:7002
    #o-otherpage1:8001; o-otherpage2:8002; o-otherpage3:8003; o-otherinvite:8004
    #o-tacit-reply:9001; o-askanything-detail: 9002; 0-askanything-scan:9003
    curUser = models.ForeignKey(verbose_name="current user", to="UserInfo", null=True, on_delete=models.CASCADE)
    type = models.IntegerField()
    count = models.PositiveIntegerField(verbose_name="次数", default=0)
    latest_time = models.DateTimeField(verbose_name="最近时间", auto_now_add=True)

    class Meta:
        db_table = "pagesdata"
        verbose_name = "不同页数据"
        verbose_name_plural = verbose_name

class GateData(models.Model):
    curUser = models.ForeignKey(verbose_name="current user", to="UserInfo", null=True, on_delete=models.CASCADE)
    type = models.PositiveIntegerField(verbose_name="第一次登陆1", default=0)

    class Meta:
        db_table = "gatedata"
        verbose_name = "第一次数据"
        verbose_name_plural = verbose_name

