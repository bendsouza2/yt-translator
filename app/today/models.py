from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail_url = models.URLField()
