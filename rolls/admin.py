from django.contrib import admin
from .models import Roll, UrlPhoto
# Register your models here.

class UrlPhotoInline(admin.TabularInline):
    model = UrlPhoto
    extra = 1

@admin.register(Roll)
class RollAdmin(admin.ModelAdmin):
    list_display = ("id", "film_name", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("film_name", "user__username")
    inlines = [UrlPhotoInline]

@admin.register(UrlPhoto)
class UrlPhotoAdmin(admin.ModelAdmin):
    list_display = ("url", "provider", "roll", "created_at")
    list_filter = ("provider",)
    search_fields = ("url",)
                   