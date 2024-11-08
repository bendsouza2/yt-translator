from django.core.management.base import BaseCommand
from django.utils.dateparse import parse_datetime


from today.models import Video
from today import constants
from python.yt_uploader import YTConnector


class Command(BaseCommand):
    """
    Django management command to fetch YouTube Shorts videos and save them to the database.

    This command connects to the YouTube API to retrieve videos from a specific channel,
    parses their details (title, description, upload date), and updates or creates
    corresponding video records in the database.
    """

    help = "Fetch YT Shorts videos and save them to the database"

    def handle(self, *args, **options):
        """
        Main logic of the command to fetch the videos and update the database.

        This method:
        1. Fetches video details from YouTube using the YTConnector.
        2. Parses video information (title, description, upload date).
        3. Updates or creates video records in the database.
        4. Outputs a success message for each video processed.

        :param args: Positional arguments to pass to the command
        :param options: Keyword arguments to pass to the command
        """

        yt = YTConnector(credentials_env=True)
        videos = yt.list_youtube_uploads(channel_id=constants.YOUTUBE_CHANNEL_ID)

        for video_id, details in videos.items():
            upload_date = parse_datetime(details["published_at"])
            video, created = Video.objects.update_or_create(
                video_id=video_id,
                defaults={
                    "title": details["title"],
                    "description": details["description"],
                    "thumbnail_url": details["thumbnail_url"],
                    "upload_date": upload_date,
                }
            )

            if created:
                self.stdout.write(f"New video added: {video.title}")
            else:
                self.stdout.write(f"Video updated: {video.title}")

