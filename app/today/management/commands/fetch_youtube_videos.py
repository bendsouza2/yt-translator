from django.core.management.base import BaseCommand

from app.today.models import Video
from python.yt_uploader import YTConnector


class Command(BaseCommand):

    help = "Fetch YT Shorts videos and save them to the database"

    def handle(self, *args, **options):

        yt = YTConnector()
        videos = yt.list_youtube_uploads(channel_id="UCQjyvCIR9IkG02Q0Wmpz9sQ")

        for video_id, details in videos.items():
            video, created = Video.objects.update_or_create(
                video_id=video_id,
                defaults={
                    "title": details["title"],
                    "description": details["description"],
                    "thumbnail_url": details["thumbnail_url"]
                }
            )

            if created:
                self.stdout.write(f"New video added: {video.title}")
            else:
                self.stdout.write(f"Video updated: {video.title}")

