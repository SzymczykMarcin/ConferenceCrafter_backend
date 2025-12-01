from django.db import migrations, models
import django.db.models.deletion
from django.core.validators import MaxValueValidator, MinValueValidator


class Migration(migrations.Migration):

    dependencies = [
        ("events", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Feedback",
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
                ("rating", models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])),
                ("comment", models.TextField(blank=True)),
                ("client_token", models.CharField(max_length=64)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="feedback",
                        to="events.event",
                    ),
                ),
            ],
            options={"ordering": ["-created_at"]},
        ),
        migrations.AddIndex(
            model_name="feedback",
            index=models.Index(fields=["event", "client_token"], name="events_feed_event_c_35e153_idx"),
        ),
    ]
