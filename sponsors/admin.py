from django.contrib import admin

from .models import Coupon, CouponRedemption, Sponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "sponsor",
        "discount_amount",
        "valid_from",
        "valid_to",
        "is_active",
        "max_redemptions",
        "remaining_redemptions",
    )
    list_filter = ("sponsor",)
    search_fields = ("code", "description")

    @admin.display(description="Remaining redemptions")
    def remaining_redemptions(self, obj):
        return obj.remaining_redemptions


@admin.register(CouponRedemption)
class CouponRedemptionAdmin(admin.ModelAdmin):
    list_display = ("coupon", "client_token", "redeemed_at")
    search_fields = ("coupon__code", "client_token")
    list_filter = ("coupon__sponsor",)
