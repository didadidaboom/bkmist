
from django.conf.urls import url
from api import views
from api.views import autho
from api.views import topic
from api.views import publish
from api.views import moment
from api.views import comment
from api.views import login
from api.views import personalMoment,personalTacit
from api.views import personal,other,otherTacit
from api.views import tacit

urlpatterns = [
    url(r'^login/$', autho.LoginView.as_view()),
    url(r'^credential/$', autho.CredentialView.as_view()),
    url(r'^messageCode/$', autho.MessageCodeView.as_view()), #验证码

    #openID 登陆
    url(r'^loginOpenid/$', login.LoginOpenidView.as_view()),
    url(r'^getAccessToken/$', login.getAccessView.as_view()),

    #话题相关
    url(r'^topic/$', topic.TopicView.as_view()),

    #发布瞬间
    url(r'^publish/$', publish.PublishView.as_view()),
    #获取瞬间
    url(r'^moment/$', moment.MomentView.as_view()),
    url(r'^momentDetail/(?P<pk>\d+)/$', moment.MomentDetailView.as_view()),
    #url(r'^momentDetail/$', views.MomentDetailView.as_view()),
    url(r'^momentFavor/$', moment.MomentFavorView.as_view()),

    #评论记录
    url(r'^submitComment/$', comment.CreateCommentView.as_view()),
    url(r'^updateComment/$', comment.CommentView.as_view()),
    url(r'^commentFavor/$', comment.CommentFavorView.as_view()),

    #获取个人主页资料
    url(r'^personalInfo/$', personal.PersonalInfoView.as_view()),
    url(r'^updateNamePersonal/$', personal.UpdateNamePersonalView.as_view()),
    url(r'^updateAvatarPersonal/$', personal.UpdateAvatarPersonalView.as_view()),
    url(r'^deletePersonal/$', personal.DeletePersonalView.as_view()),
    url(r'^personalViewerPage1/$', personal.PersonalViewerPage1View.as_view()),
    url(r'^personalViewerPage2/$', personal.PersonalViewerPage2View.as_view()),
    url(r'^personalViewerPage3/$', personal.PersonalViewerPage3View.as_view()),
    url(r'^personalViewerPage3Scan/$', personal.PersonalViewerPage3ScanView.as_view()),
    url(r'^personalViewerPage3Submit/$', personal.PersonalViewerPage3SubmitView.as_view()),
    url(r'^personalMomentViewer/$', personal.PersonalMomentViewerView.as_view()),
    url(r'^personalFocusList/$', personal.PersonalFocusListView.as_view()),
    url(r'^personalFocusedList/$', personal.PersonalFocusedListView.as_view()),
    #获取个人主页瞬间
    url(r'^personalMoment/$', personalMoment.PersonalMomentView.as_view()),
    url(r'^updatePersonalMoment/(?P<pk>\d+)/$', personalMoment.UpdatePersonalMomentView.as_view()),
    url(r'^delPersonalMoment/(?P<pk>\d+)/$', personalMoment.DelPersonalMomentView.as_view()),
    url(r'^personalTacit/$', personalTacit.PersonalTacitView.as_view()),
    url(r'^updatePersonalTacit/(?P<pk>\d+)/$', personalTacit.UpdatePersonalTacitView.as_view()),
    url(r'^delPersonalTacit/(?P<pk>\d+)/$', personalTacit.DelPersonalTacitView.as_view()),
    url(r'^personalTacitReply/$', personalTacit.PersonalTacitReplyView.as_view()),

    #获取他人主页资料
    url(r'^otherDetails/(?P<pk>\d+)/$', other.OtherDetailsView.as_view()),
    url(r'^otherMoments/$', other.OtherMomentsView.as_view()),
    url(r'^focusUser/$', other.FocusUserView.as_view()),
    url(r'^otherTacits/$', otherTacit.OtherTacitsView.as_view()),
    url(r'^otherTacitsReply/$', otherTacit.OtherTacitsReplyView.as_view()),

    #好友默契测试
    url(r'^tacit/$', tacit.TacitView.as_view()),
    url(r'^tacitSave/$', tacit.TacitSaveView.as_view()),
    url(r'^tacitRandomOne/$', tacit.TacitRandomOneView.as_view()),
    url(r'^replyTacit/(?P<pk>\d+)/$', tacit.ReplyTacitView.as_view()),
    url(r'^replyTacitSave/$', tacit.ReplyTacitSaveView.as_view()),
]
