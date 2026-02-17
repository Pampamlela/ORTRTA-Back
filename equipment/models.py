from django.db import models
from django.conf import settings
# Create your models here.

class Camera(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE, 
          related_name="cameras")
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model}"
    
class Lens(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
          on_delete=models.CASCADE, 
          related_name="lenses"
    )
    camera = models.ForeignKey(
        Camera,
          on_delete=models.CASCADE, 
          related_name="lenses"
    )
    model = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.model}"