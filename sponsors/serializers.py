from rest_framework import serializers

from .models import Coupon, Sponsor


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ["id", "name", "logo_url", "description", "socials"]


class CouponSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.PrimaryKeyRelatedField(
        source="sponsor", queryset=Sponsor.objects.all(), write_only=True
    )

    class Meta:
        model = Coupon
        fields = [
            "id",
            "sponsor",
            "sponsor_id",
            "code",
            "description",
            "discount_amount",
            "valid_from",
            "valid_to",
        ]

    def validate(self, attrs):
        valid_from = attrs.get("valid_from") or getattr(self.instance, "valid_from", None)
        valid_to = attrs.get("valid_to") or getattr(self.instance, "valid_to", None)
        if valid_from and valid_to and valid_to < valid_from:
            raise serializers.ValidationError("valid_to must be after valid_from")
        return super().validate(attrs)
