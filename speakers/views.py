"""Viewsets for administering and browsing conference speakers."""

from rest_framework import permissions, viewsets

from .models import Speaker
from .serializers import SpeakerSerializer


class SpeakerAdminViewSet(viewsets.ModelViewSet):
    """Admin CRUD endpoint for maintaining speaker records."""

    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["name", "company", "bio"]


class SpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    """Public read-only endpoint exposing speaker profiles."""

    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name", "company"]
    filterset_fields = ["company"]
