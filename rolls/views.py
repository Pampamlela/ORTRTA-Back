from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Roll, UrlPhoto
from .serializers import RollSerializer, UrlPhotoSerializer
from.permissions import IsOwner, IsRollOwner
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class RollViewSet(viewsets.ModelViewSet):
    serializer_class = RollSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return (
            Roll.objects
            .filter(user=self.request.user)
            .select_related("camera", "lens", "user")
        )
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "camera", "lens", "iso", "format"]
    search_fields = ["film_name", "description"]
    ordering_fields = ["date_start", "created_at", "updated_at"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class UrlPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UrlPhotoSerializer
    permission_classes = [IsAuthenticated, IsRollOwner]

    def get_queryset(self):
        return Roll.objects.filter(user=self.request.user)
    