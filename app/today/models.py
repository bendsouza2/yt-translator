"""Contains Models (db tables) for storing data related to the video output"""

from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=255, unique=True, primary_key=True)
    word = models.CharField(max_length=25, null=True, blank=True)
    sentence = models.CharField(max_length=300, null=True, blank=True)
    translated_sentence = models.CharField(max_length=300, null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    upload_time = models.DateTimeField(null=True, blank=True)
    thumbnail_url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.video_id

    class Meta:
        db_table = "videos"

