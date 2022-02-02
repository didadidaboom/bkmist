from rest_framework.serializers import ModelSerializer

from api import models

class CreateAskAnythingModelSerializer(ModelSerializer):

    class Meta:
        model = models.TacitRecord
        fields = ["id","type","avatarUrlFlag","user"]