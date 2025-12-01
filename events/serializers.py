"""Serializers for exposing event and event type data via the API."""

from rest_framework import serializers

from speakers.models import Speaker
from speakers.serializers import SpeakerSerializer
from .models import Event, EventType


class EventTypeSerializer(serializers.ModelSerializer):
    """Serialize and validate event type metadata for API consumers."""

    class Meta:
        model = EventType
        fields = ["id", "name", "description"]


class EventSerializer(serializers.ModelSerializer):
    """Expose event details with nested presenter and type information."""

    event_type = EventTypeSerializer(read_only=True)
    event_type_id = serializers.PrimaryKeyRelatedField(
        source="event_type",
        queryset=EventType.objects.all(),
        write_only=True,
    )
    presenter = SpeakerSerializer(read_only=True)
    presenter_id = serializers.PrimaryKeyRelatedField(
        source="presenter",
        queryset=Speaker.objects.all(),
        required=False,
        allow_null=True,
        write_only=True,
    )

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "event_type",
            "event_type_id",
            "start_time",
            "room",
            "presenter",
            "presenter_id",
            "description",
        ]
