from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("sponsors", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="is_active",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="coupon",
            name="max_redemptions",
            field=models.PositiveIntegerField(
                blank=True,
                help_text="Optional maximum number of total redemptions for this coupon.",
                null=True,
            ),
        ),
        migrations.CreateModel(
            name="CouponRedemption",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("client_token", models.CharField(max_length=255)),
                ("redeemed_at", models.DateTimeField(auto_now_add=True)),
                (
                    "coupon",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="redemptions",
                        to="sponsors.coupon",
                    ),
                ),
            ],
            options={"ordering": ["-redeemed_at"]},
        ),
        migrations.AlterUniqueTogether(
            name="couponredemption",
            unique_together={("coupon", "client_token")},
        ),
    ]

