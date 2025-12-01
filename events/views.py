"""Viewsets exposing event types and events for admins and attendees."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import Event, EventType
from .serializers import EventSerializer, EventTypeSerializer


class EventTypeAdminViewSet(viewsets.ModelViewSet):
    """Full CRUD interface for managing event categories in the admin API."""

    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["name"]


class EventAdminViewSet(viewsets.ModelViewSet):
    """Administrative access for creating, updating, and organizing events."""

    queryset = Event.objects.select_related("event_type", "presenter").all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["event_type", "presenter", "room"]
    search_fields = ["title", "description", "room"]
    ordering_fields = ["start_time", "title"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class EventTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only view of available event categories for public clients."""

    queryset = EventType.objects.all()
    serializer_class = EventTypeSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name"]


class EventViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only listing of events with filtering by presenter, type, or room."""

    queryset = Event.objects.select_related("event_type", "presenter").all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["event_type", "presenter", "room"]
    search_fields = ["title", "description", "room"]
    ordering_fields = ["start_time", "title"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
