from django.shortcuts import render
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from .models import Roll, UrlPhoto
from .serializers import RollSerializer, UrlPhotoSerializer
from.permissions import IsOwner, IsRollOwner
from django_filters.rest_framework import DjangoFilterBackend
import qrcode
from io import BytesIO
from django.http import HttpResponse
from rest_framework.decorators import action

# Create your views here.

class RollViewSet(viewsets.ModelViewSet):
    serializer_class = RollSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return (
            Roll.objects
            .filter(user=self.request.user)
            .select_related("camera", "lens", "user")
            .prefetch_related("photos") # si bcp de photos, ça peut être lourd, à tester
        )
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "camera", "lens", "iso", "format"]
    search_fields = ["film_name", "description"]
    ordering_fields = ["date_start", "created_at", "updated_at"]
    lookup_field = "slug"

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # génération des QrCodes pour chaque roll
    @action(detail=True, methods=["get"])
    def qr(self, request, pk=None):
        roll = self.get_object()

        url = f"http://127.0.0.1:8000/rolls/{roll.slug}/"

        qr = qrcode.make(url)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        return HttpResponse(buffer.getvalue(), content_type="image/png")

class UrlPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UrlPhotoSerializer
    permission_classes = [IsAuthenticated, IsRollOwner]

    def get_queryset(self):
        return (
            UrlPhoto.objects
            .filter(roll__user=self.request.user)
            .select_related("roll")
        )
    