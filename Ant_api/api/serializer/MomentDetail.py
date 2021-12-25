from rest_framework import serializers

class MomentDetailSerializer(serializers.Serializer):
    '''
    瞬间发的图片序列化器
    '''
    path = serializers.CharField()
    path_key = serializers.CharField()