from rest_framework import serializers
from .models import Camera, Lens

class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = "__all__"

class LensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lens
        fields = "__all__"