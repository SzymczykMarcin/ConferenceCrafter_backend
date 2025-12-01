from django.contrib import admin

from .models import Speaker


@admin.register(Speaker)
class SpeakerAdmin(admin.ModelAdmin):
    list_display = ("name", "company")
    search_fields = ("name", "company", "bio")
