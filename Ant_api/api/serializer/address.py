from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from api import models
'''
class GetAddressDetailModelSerializer(ModelSerializer):
    is_focused = serializers.SerializerMethodField()

    class Meta:
        model = models.Address
        fields = ["id","address","addressName","is_focused"]

    def get_is_focused(self,obj):
        request = self.context.get("request")
        if not request.user:
            return False
        addressfavor_object = models.AddressFocusRecord.objects.filter(user=request.user,address=obj)
        exists = addressfavor_object.exists()
        if exists:
            return True
        return False

class FocusAddressModelSerializer(ModelSerializer):
    class Meta:
        model = models.AddressFocusRecord
        fields = ["address"]
'''