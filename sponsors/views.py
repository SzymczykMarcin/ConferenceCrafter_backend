from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, viewsets

from .models import Coupon, Sponsor
from .serializers import CouponSerializer, SponsorSerializer


class SponsorAdminViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["name", "description"]


class CouponAdminViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.select_related("sponsor").all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["sponsor"]
    search_fields = ["code", "description"]
    ordering_fields = ["valid_from", "valid_to", "discount_amount", "code"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name", "description"]


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.select_related("sponsor").all()
    serializer_class = CouponSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["sponsor", "code"]
    search_fields = ["code", "description"]
    ordering_fields = ["valid_from", "valid_to", "discount_amount", "code"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
