from rest_framework.filters import BaseFilterBackend

class MinFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get("min_id")
        if min_id:
            queryset = queryset.filter(id__lt=min_id)
        return queryset
class MaxFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get("max_id")
        if max_id:
            queryset=queryset.filter(id__gt=max_id)
        return queryset

class MinCommentFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get("min_id")
        moment_id = request.query_params.get("moment_id")
        if min_id:
            queryset = queryset.filter(id__lt=min_id,moment_id=moment_id)
        return queryset
class MaxCommentFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get("max_id")
        moment_id = request.query_params.get("moment_id")
        if max_id:
            queryset=queryset.filter(id__gt=max_id,moment_id=moment_id)
        return queryset

class MinOtherFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        min_id = request.query_params.get("min_id")
        moment_id = request.query_params.get("user_id")
        if min_id:
            queryset = queryset.filter(id__lt=min_id,user_id=moment_id)
        return queryset
class MaxOtherFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        max_id = request.query_params.get("max_id")
        moment_id = request.query_params.get("user_id")
        if max_id:
            queryset=queryset.filter(id__gt=max_id,user_id=moment_id)
        return queryset