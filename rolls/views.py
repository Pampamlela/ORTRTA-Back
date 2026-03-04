from django.shortcuts import render
from django.conf import settings
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from .models import Roll, UrlPhoto, RollStatus
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
    def qr(self, request, *args, **kwargs):
        roll = self.get_object()

        url = f"{settings.FRONTEND_URL}/rolls/{roll.slug}/"

        qr = qrcode.make(url)

        buffer = BytesIO()
        qr.save(buffer, format="PNG")

        return HttpResponse(buffer.getvalue(), content_type="image/png")
    
    def perform_update(self, serializer):
        roll = self.get_object()
        if roll.status == RollStatus.SCANNED:
            allowed_fields = {"date_scan", "description"}

            # champs envoyés dans la requête
            incoming_fields = set(serializer.validated_data.keys())

            # si un champ interdit est modifié
            if not incoming_fields.issubset(allowed_fields):
                raise ValidationError(
                    "Cette pellicule est scannée."
                    "Seul les champs 'date_scan' et 'description' peuvent être modifiés."
                )
        serializer.save()

    def perform_destroy(self, instance):
        if instance.status == RollStatus.SCANNED:
            raise ValidationError("Cette pellicule est scannée et ne peut plus être supprimée.")
        instance.delete()
        

class UrlPhotoViewSet(viewsets.ModelViewSet):
    serializer_class = UrlPhotoSerializer
    permission_classes = [IsAuthenticated, IsRollOwner]

    def get_queryset(self):
        return (
            UrlPhoto.objects
            .filter(roll__user=self.request.user)
            .select_related("roll")
        )
    