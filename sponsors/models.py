from django.db import models
from django.utils import timezone


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    logo_url = models.URLField(blank=True)
    description = models.TextField(blank=True)
    socials = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Coupon(models.Model):
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE, related_name="coupons")
    code = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    discount_amount = models.DecimalField(max_digits=8, decimal_places=2)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    max_redemptions = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Optional maximum number of total redemptions for this coupon.",
    )
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-valid_from", "code"]
        unique_together = ("sponsor", "code")

    def __str__(self):
        return f"{self.code} ({self.sponsor})"

    @property
    def redemption_count(self) -> int:
        if hasattr(self, "_redemptions_count"):
            return self._redemptions_count
        return self.redemptions.count()

    @property
    def remaining_redemptions(self):
        if self.max_redemptions is None:
            return None
        return max(self.max_redemptions - self.redemption_count, 0)

    def can_redeem(self) -> bool:
        now = timezone.now()
        if not self.is_active:
            return False
        if self.valid_from > now or self.valid_to < now:
            return False
        if self.max_redemptions is not None and self.redemption_count >= self.max_redemptions:
            return False
        return True


class CouponRedemption(models.Model):
    coupon = models.ForeignKey(
        Coupon, on_delete=models.CASCADE, related_name="redemptions"
    )
    client_token = models.CharField(max_length=255)
    redeemed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-redeemed_at"]
        unique_together = ("coupon", "client_token")

    def __str__(self):
        return f"{self.coupon.code} redeemed by {self.client_token}"
