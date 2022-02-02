from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models

class CreateAskAnythingModelSerializer(ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.TacitRecord
        fields = ["id","type","avatarUrlFlag","user"]