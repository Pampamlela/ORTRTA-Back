from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Roll, UrlPhoto
from .serializers import RollSerializer, UrlPhotoSerializer
from.permissions import IsOwner, IsRollOwner
# Create your views here.

class RollViewSet(viewsets.ModelViewSet):
    serializer_class = RollSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Roll.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UrlPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UrlPhotoSerializer
    permission_classes = [IsAuthenticated, IsRollOwner]

    def get_queryset(self):
        return UrlPhoto.objects.filter(roll__user=self.request.user)
    