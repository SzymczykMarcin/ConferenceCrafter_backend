"""Models defining conference events and their classifications."""

from django.db import models

from speakers.models import Speaker


class EventType(models.Model):
    """Categorizes events so schedules can be filtered or grouped."""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Event(models.Model):
    """Represents a scheduled session with timing and presenter details."""

    title = models.CharField(max_length=255)
    event_type = models.ForeignKey(EventType, on_delete=models.CASCADE, related_name="events")
    start_time = models.DateTimeField()
    room = models.CharField(max_length=100)
    presenter = models.ForeignKey(
        Speaker,
        on_delete=models.SET_NULL,
        related_name="events",
        null=True,
        blank=True,
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["start_time", "title"]

    def __str__(self):
        return self.title
