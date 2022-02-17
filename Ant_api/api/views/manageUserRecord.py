from django.utils import timezone
import datetime
from rest_framework.generics import ListAPIView

from api.serializer import manage
from api import models

from utils import filter,pagination,auth

class getAllDayOpenidUsedListView(ListAPIView):
    serializer_class = manage.getAllOpenidUsedListModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        day = self.request.query_params.get("day")
        if not day:
            day = 0
        cur_date = datetime.datetime.today()
        start_year = cur_date.year
        start_month = cur_date.month
        start_day = cur_date.day-day
        start_date = datetime.date(start_year, start_month, start_day)

        queryset = models.UserInfo.objects \
            .filter(openID__istartswith="olwGA5IMdGhdv2FD0n7GvEBo7_iY")\
            .filter(openID__istartswith="olwGA5KXfu6-WpOLTsrwnu_0Q1kw")\
            .filter(last_login__gte=start_date) \
            .filter(last_login__lte=timezone.now()).all().order_by("-id")

        # queryset = models.UserInfo.objects\
        #     .filter(openID__istartswith="oCKHr4gWMcH8ql0MPh7eE74llRpc")\
        #     .filter(openID__istartswith="oCKHr4nB-yw3eAapHjGUFxGmEzj4")\
        #     .filter(openID__istartswith="olwGA5IMdGhdv2FD0n7GvEBo7_iY")\
        #     .filter(openID__istartswith="olwGA5KXfu6-WpOLTsrwnu_0Q1kw")\
        #     .filter(last_login__gte = start_date)\
        #     .filter(last_login__lte= timezone.now()).all().order_by("-id")
        return queryset


class getAllNDaysOpenidUsedListView(ListAPIView):
    serializer_class = manage.getAllOpenidUsedListModelSerializer
    pagination_class = pagination.Pagination
    filter_backends = [filter.MinFilterBackend, filter.MaxFilterBackend]
    authentication_classes = [auth.GeneralAuthentication, ]

    def get_queryset(self):
        day = self.request.query_params.get("day")
        if not day:
            day = 1
        cur_date = datetime.datetime.today()
        start_year = cur_date.year
        start_month = cur_date.month
        start_day = cur_date.day-day
        start_date = datetime.date(start_year, start_month, start_day)

        queryset = models.UserInfo.objects\
            .filter(openID__istartswith="oCKHr4gWMcH8ql0MPh7eE74llRpc")\
            .filter(openID__istartswith="oCKHr4nB-yw3eAapHjGUFxGmEzj4")\
            .filter(openID__istartswith="olwGA5IMdGhdv2FD0n7GvEBo7_iY")\
            .filter(openID__istartswith="olwGA5KXfu6-WpOLTsrwnu_0Q1kw")\
            .filter(last_login__gte = start_date)\
            .filter(last_login__lte= timezone.now()).all().order_by("-id")
        return queryset


