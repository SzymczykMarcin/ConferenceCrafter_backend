"""Viewsets exposing event types and events for admins and attendees."""

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from .models import Event, EventType, Feedback
from .serializers import EventSerializer, EventTypeSerializer, FeedbackAdminSerializer, FeedbackSerializer
from .throttling import EventFeedbackRateThrottle


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


class FeedbackViewSet(
    mixins.CreateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    """Public feedback submission and read access with throttling."""

    queryset = Feedback.objects.select_related("event").all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.AllowAny]
    throttle_classes = [EventFeedbackRateThrottle]
    filterset_fields = ["event"]
    ordering_fields = ["created_at", "rating"]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]


class FeedbackAdminViewSet(viewsets.ModelViewSet):
    """Admin moderation endpoint for viewing and removing feedback entries."""

    queryset = Feedback.objects.select_related("event").all()
    serializer_class = FeedbackAdminSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["event", "rating"]
    search_fields = ["comment", "client_token"]
    ordering_fields = ["created_at", "rating"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
