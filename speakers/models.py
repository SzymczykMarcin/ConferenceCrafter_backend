from django.db import models


class Speaker(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    socials = models.JSONField(default=dict, blank=True)
    photo = models.URLField(blank=True)
    company = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
