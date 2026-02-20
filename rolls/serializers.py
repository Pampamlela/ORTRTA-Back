from rest_framework import serializers
from .models import Roll, UrlPhoto
from equipment.models import Camera, Lens

class UrlPhotoSerializer(serializers.ModelSerializer):
    roll = serializers.PrimaryKeyRelatedField(queryset=Roll.objects.all())

    class Meta:
        model = UrlPhoto
        fields = "__all__"
        read_only_fields = ("created_at", "updated_at")

    def validate(self, data):
        user = self.context["request"].user
        roll = data.get("roll")

        if roll.user != user:
            raise serializers.ValidationError(
                "You cannot add a photo to a roll that is not yours."
            )
        
        return data

class RollSerializer(serializers.ModelSerializer):
    photos = UrlPhotoSerializer(many=True, read_only=True)
    user = serializers.ReadOnlyField(source="user.id")
    camera_name = serializers.ReadOnlyField(source="camera.model")
    lens_name = serializers.ReadOnlyField(source="lens.model")
    
    class Meta:
        model = Roll
        fields = "__all__"
        read_only_fields = (
            "user",
            "slug",
            "created_at",
            "updated_at",
        )
    
    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)
    
    def validate(self, data):
        user = self.context["request"].user

        camera = data.get("camera")
        lens = data.get("lens")

        if camera and camera.user != user:
            raise serializers.ValidationError(
            "You cannot use a camera that is not yours."
        )

        if lens and lens.user != user:
            raise serializers.ValidationError(
            "You cannot use a lens that is not yours."
        )

        return data