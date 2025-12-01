from rest_framework import permissions, viewsets

from .models import Speaker
from .serializers import SpeakerSerializer


class SpeakerAdminViewSet(viewsets.ModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["name", "company", "bio"]


class SpeakerViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name", "company"]
    filterset_fields = ["company"]
