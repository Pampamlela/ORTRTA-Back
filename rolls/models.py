from django.db import models
from django.conf import settings
# Create your models here.

class RollStatus(models.TextChoices):
    IN_PROGRESS = "IN_PROGRESS", "En cours"
    FINISHED = "FINISHED", "Terminée"
    DEVELOPED = "DEVELOPED", "Développée"
    SCANNED = "SCANNED", "Scannée"

class Roll(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE, 
          related_name="rolls"
    )
    camera = models.ForeignKey(
        "equipment.Camera",
          on_delete=models.CASCADE, 
          related_name="rolls"
    )
    lens = models.ForeignKey(
        "equipment.Lens",
          on_delete=models.CASCADE, 
          related_name="rolls",
          null=True, 
          blank=True
    )
    film_name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    iso = models.IntegerField()
    format = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date_start = models.DateField()
    date_end = models.DateField(null=True, blank=True)
    date_development = models.DateField(null=True, blank=True)
    date_scan = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=RollStatus.choices,
        default=RollStatus.IN_PROGRESS
    )
    slug = models.SlugField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.film_name}"