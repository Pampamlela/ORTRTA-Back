from rest_framework import serializers
from .models import Roll, UrlPhoto

class UrlPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UrlPhoto
        fields = "__all__"
        read_only_fields = ["roll"] # roll jamais modifiable via UrlPhotoSerializer, uniquement via RollSerializercd  

class RollSerializer(serializers.ModelSerializer):
    photos = UrlPhotoSerializer(many=True, read_only=True)
    
    class Meta:
        model = Roll
        fields = "__all__"
        read_only_fields = ["user"]