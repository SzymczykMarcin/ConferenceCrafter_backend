from django.contrib import admin

from .models import Event, EventType, Feedback


@admin.register(EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "event_type", "start_time", "room", "presenter")
    list_filter = ("event_type",)
    search_fields = ("title", "room", "description")
    autocomplete_fields = ("event_type", "presenter")


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("event", "rating", "created_at")
    list_filter = ("rating", "event")
    search_fields = ("comment", "client_token")
    autocomplete_fields = ("event",)
    ordering = ("-created_at",)
