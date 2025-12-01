from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Sponsor",
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
                ("name", models.CharField(max_length=255)),
                ("logo_url", models.URLField(blank=True)),
                ("description", models.TextField(blank=True)),
                ("socials", models.JSONField(blank=True, default=dict)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Coupon",
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
                ("code", models.CharField(max_length=50)),
                ("description", models.TextField(blank=True)),
                ("discount_amount", models.DecimalField(decimal_places=2, max_digits=8)),
                ("valid_from", models.DateTimeField()),
                ("valid_to", models.DateTimeField()),
                (
                    "sponsor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="coupons",
                        to="sponsors.sponsor",
                    ),
                ),
            ],
            options={"ordering": ["-valid_from", "code"]},
        ),
        migrations.AlterUniqueTogether(
            name="coupon",
            unique_together={("sponsor", "code")},
        ),
    ]
