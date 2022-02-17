from django.utils import timezone
import datetime
from rest_framework.generics import ListAPIView,RetrieveAPIView
from django.db.models import Q,F,Count

from api.serializer import manageUserRecord
from api import models

from utils import filter,pagination,auth

class getAllDayOpenidUsedListView(ListAPIView):
    serializer_class = manageUserRecord.getDayOpenidUsedListModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        day = self.request.query_params.get("day")
        day = int(day)
        # if not day:
        #     day = 0
        cur_date = datetime.datetime.today()
        start_year = cur_date.year
        start_month = cur_date.month
        start_day = cur_date.day-day
        start_date = datetime.date(start_year, start_month, start_day)
        end_year = cur_date.year
        end_month = cur_date.month
        end_day = cur_date.day - day +1
        end_date = datetime.date(end_year, end_month, end_day)

        queryset = models.UserInfo.objects \
            .filter(~Q(openID__startswith ="oCKHr4gWMcH8ql0MPh7eE74llRpc")) \
            .filter(~Q(openID__istartswith="oCKHr4nB-yw3eAapHjGUFxGmEzj4")) \
            .filter(~Q(openID__istartswith="olwGA5IMdGhdv2FD0n7GvEBo7_iY")) \
            .filter(~Q(openID__istartswith="olwGA5KXfu6-WpOLTsrwnu_0Q1kw")) \
            .filter(last_login__gte=start_date) \
            .filter(last_login__lte=end_date).all().order_by("-id")

        # queryset = models.UserInfo.objects\
        #     .filter(openID__istartswith="oCKHr4gWMcH8ql0MPh7eE74llRpc")\
        #     .filter(openID__istartswith="oCKHr4nB-yw3eAapHjGUFxGmEzj4")\
        #     .filter(openID__istartswith="olwGA5IMdGhdv2FD0n7GvEBo7_iY")\
        #     .filter(openID__istartswith="olwGA5KXfu6-WpOLTsrwnu_0Q1kw")\
        #     .filter(last_login__gte = start_date)\
        #     .filter(last_login__lte= timezone.now()).all().order_by("-id")
        return queryset


class getAllNDaysOpenidUsedListView(ListAPIView):
    serializer_class = manageUserRecord.getDayOpenidUsedListModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        day = self.request.query_params.get("ndays")
        day = int(day)
        cur_date = datetime.datetime.today()
        start_year = cur_date.year
        start_month = cur_date.month
        start_day = cur_date.day-day
        start_date = datetime.date(start_year, start_month, start_day)

        queryset = models.UserInfo.objects \
            .filter(~Q(openID__startswith="oCKHr4gWMcH8ql0MPh7eE74llRpc")) \
            .filter(~Q(openID__istartswith="oCKHr4nB-yw3eAapHjGUFxGmEzj4")) \
            .filter(~Q(openID__istartswith="olwGA5IMdGhdv2FD0n7GvEBo7_iY")) \
            .filter(~Q(openID__istartswith="olwGA5KXfu6-WpOLTsrwnu_0Q1kw")) \
            .filter(last_login__gte=start_date) \
            .filter(last_login__lte=timezone.now()).all().order_by("-id")

        return queryset

class getPersonalDataView(ListAPIView):
    '''
    获取单条瞬间详细
    '''
    queryset = models.PersonalData.objects
    authentication_classes = [auth.GeneralAuthentication,]
    serializer_class = manageUserRecord.getPersonalDataModelSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        queryset = models.PersonalData.objects.filter(curUser_id=int(user_id))
        return queryset

class getPageDataView(ListAPIView):
    '''
    获取单条瞬间详细
    '''
    queryset = models.PagesData.objects
    authentication_classes = [auth.GeneralAuthentication,]
    serializer_class = manageUserRecord.getPageDataViewModelSerializer
    def get_queryset(self):
        user_id = self.request.query_params.get("user_id")
        queryset = models.PagesData.objects.filter(curUser_id=int(user_id))
        return queryset
