from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination

class Pagination(LimitOffsetPagination):
    '''
    进行切片处理，【0，limit】
    '''
    default_limit = 10
    max_limit = 20
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    def get_offset(self, request):
        return 0
    def get_paginated_response(self, data):
        return Response(data)