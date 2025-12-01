from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, permissions, viewsets

from .models import Coupon, CouponRedemption, Sponsor
from .serializers import CouponRedemptionSerializer, CouponSerializer, SponsorSerializer


class SponsorAdminViewSet(viewsets.ModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.IsAdminUser]
    search_fields = ["name", "description"]


class CouponAdminViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.select_related("sponsor").annotate(
        _redemptions_count=Count("redemptions")
    )
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["sponsor"]
    search_fields = ["code", "description"]
    ordering_fields = ["valid_from", "valid_to", "discount_amount", "code"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class CouponRedemptionAdminViewSet(viewsets.ModelViewSet):
    queryset = CouponRedemption.objects.select_related("coupon", "coupon__sponsor")
    serializer_class = CouponRedemptionSerializer
    permission_classes = [permissions.IsAdminUser]
    filterset_fields = ["coupon__sponsor", "coupon"]
    search_fields = ["coupon__code", "client_token"]
    ordering_fields = ["redeemed_at"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class SponsorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sponsor.objects.all()
    serializer_class = SponsorSerializer
    permission_classes = [permissions.AllowAny]
    search_fields = ["name", "description"]


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.select_related("sponsor").annotate(
        _redemptions_count=Count("redemptions")
    )
    serializer_class = CouponSerializer
    permission_classes = [permissions.AllowAny]
    filterset_fields = ["sponsor", "code"]
    search_fields = ["code", "description"]
    ordering_fields = ["valid_from", "valid_to", "discount_amount", "code"]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]


class CouponRedemptionViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = CouponRedemption.objects.select_related("coupon", "coupon__sponsor")
    serializer_class = CouponRedemptionSerializer
    permission_classes = [permissions.AllowAny]
