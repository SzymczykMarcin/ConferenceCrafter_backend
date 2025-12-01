from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Speaker",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=255)),
                ("bio", models.TextField(blank=True)),
                ("socials", models.JSONField(blank=True, default=dict)),
                ("photo", models.URLField(blank=True)),
                ("company", models.CharField(blank=True, max_length=255)),
            ],
            options={"ordering": ["name"]},
        ),
    ]
