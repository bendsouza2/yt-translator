from django.db import models


class Video(models.Model):
    video_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail_url = models.URLField()
    upload_date = models.DateTimeField(default="2024-11-05T15:41:31Z")

    def __str__(self):
        return self.video_id
