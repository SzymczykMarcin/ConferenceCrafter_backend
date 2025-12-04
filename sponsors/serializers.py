from rest_framework import serializers

from .models import Coupon, CouponRedemption, Sponsor


class SponsorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sponsor
        fields = ["id", "name", "logo_url", "description", "socials"]


class CouponSerializer(serializers.ModelSerializer):
    sponsor = SponsorSerializer(read_only=True)
    sponsor_id = serializers.PrimaryKeyRelatedField(
        source="sponsor", queryset=Sponsor.objects.all(), write_only=True
    )
    remaining_redemptions = serializers.IntegerField(read_only=True)

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
            "max_redemptions",
            "is_active",
            "remaining_redemptions",
        ]
        read_only_fields = ["remaining_redemptions"]

    def validate(self, attrs):
        valid_from = attrs.get("valid_from") or getattr(self.instance, "valid_from", None)
        valid_to = attrs.get("valid_to") or getattr(self.instance, "valid_to", None)
        if valid_from and valid_to and valid_to < valid_from:
            raise serializers.ValidationError("valid_to must be after valid_from")
        return super().validate(attrs)


class CouponRedemptionSerializer(serializers.ModelSerializer):
    coupon = CouponSerializer(read_only=True)
    coupon_code = serializers.CharField(write_only=True)

    class Meta:
        model = CouponRedemption
        fields = [
            "id",
            "coupon",
            "coupon_code",
            "client_token",
            "redeemed_at",
        ]
        read_only_fields = ["id", "coupon", "redeemed_at"]

    def validate(self, attrs):
        coupon_code = attrs["coupon_code"]
        coupons = list(
            Coupon.objects.select_related("sponsor").filter(code=coupon_code)[:2]
        )

        if not coupons:
            raise serializers.ValidationError({"coupon_code": "Invalid coupon code."})

        if len(coupons) > 1:
            raise serializers.ValidationError(
                {
                    "coupon_code": "Multiple coupons found for this code. Please provide a sponsor-specific code.",
                }
            )

        coupon = coupons[0]

        coupon._redemptions_count = coupon.redemptions.count()

        if not coupon.can_redeem():
            raise serializers.ValidationError("Coupon is not valid for redemption.")

        client_token = attrs.get("client_token")
        if coupon.redemptions.filter(client_token=client_token).exists():
            raise serializers.ValidationError(
                {"client_token": "This coupon has already been redeemed by this client."}
            )

        attrs["coupon"] = coupon
        return attrs

    def create(self, validated_data):
        validated_data.pop("coupon_code", None)
        return super().create(validated_data)
