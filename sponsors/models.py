from django.db import models


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

    class Meta:
        ordering = ["-valid_from", "code"]
        unique_together = ("sponsor", "code")

    def __str__(self):
        return f"{self.code} ({self.sponsor})"
