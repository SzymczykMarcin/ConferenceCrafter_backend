from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("speakers", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EventType",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Event",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=255)),
                ("start_time", models.DateTimeField()),
                ("room", models.CharField(max_length=100)),
                ("description", models.TextField(blank=True)),
                (
                    "event_type",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="events",
                        to="events.eventtype",
                    ),
                ),
                (
                    "presenter",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="events",
                        to="speakers.speaker",
                    ),
                ),
            ],
            options={"ordering": ["start_time", "title"]},
        ),
    ]
