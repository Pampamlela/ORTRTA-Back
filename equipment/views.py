from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Camera, Lens
from .serializers import CameraSerializer, LensSerializer
# Create your views here.

class CameraViewSet(viewsets.ModelViewSet):
    serializer_class = CameraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Camera.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class LensViewSet(viewsets.ModelViewSet):
    serializer_class = LensSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Lens.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)