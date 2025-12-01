"""Serializers for exposing speaker profiles through the API."""

from rest_framework import serializers

from .models import Speaker


class SpeakerSerializer(serializers.ModelSerializer):
    """Serialize speaker biography and contact fields for clients."""

    class Meta:
        model = Speaker
        fields = ["id", "name", "bio", "socials", "photo", "company"]
