from rest_framework.authentication import BaseAuthentication
from rest_framework import status
from rest_framework import exceptions
from api import models
from rest_framework.request import Request


class GeneralAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.META.get('HTTP_AUTHORIZATION', b'')
        if not token:
            return None
        user_object = models.UserInfo.objects.filter(token=token).first()
        if not user_object:
            return None
        return (user_object,token)

class UserAuthentication(BaseAuthentication):
    def authenticate(self, request):
        """
        Authenticate the request and return a two-tuple of (user, token).
        """
        token = request.META.get('HTTP_AUTHORIZATION', b'')
        if not token:
            raise exceptions.AuthenticationFailed
        user_object = models.UserInfo.objects.filter(token=token).first()
        if not user_object:
            raise exceptions.AuthenticationFailed
        return (user_object,token)
