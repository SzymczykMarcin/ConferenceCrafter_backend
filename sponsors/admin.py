from django.contrib import admin

from .models import Coupon, Sponsor


@admin.register(Sponsor)
class SponsorAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "sponsor", "discount_amount", "valid_from", "valid_to")
    list_filter = ("sponsor",)
    search_fields = ("code", "description")
