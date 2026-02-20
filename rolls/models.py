from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string
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
          on_delete=models.SET_NULL, 
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
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.film_name)
            random_part = get_random_string(6)
            self.slug = f"{base_slug}-{random_part}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.film_name} ({self.user.username})"
    
class PhotoProvider(models.TextChoices):
    FLICKR = "FLICKR", "Flickr"
    GOOGLE_PHOTOS = "GOOGLE_PHOTOS", "Google Photos"
    GOOGLE_DRIVE = "GOOGLE_DRIVE", "Google Drive"
    SITE = "SITE", "Site personnel"
    OTHER = "OTHER", "Autre"
    
class UrlPhoto(models.Model):
    roll = models.ForeignKey(
        Roll,
          on_delete=models.CASCADE, 
          related_name="photos"
    )
    url = models.URLField()
    provider = models.CharField(
        max_length=20,
        choices=PhotoProvider.choices,
        default=PhotoProvider.OTHER
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.url}"