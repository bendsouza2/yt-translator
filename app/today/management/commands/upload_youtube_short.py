import datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from today.models import Video
from python.main import process_video_and_upload


class Command(BaseCommand):

    help = "Generate a word and sentence with audio and video for the sentence and upload the sentence to YT shorts"

    def handle(self, *args, **options):

        video_details = process_video_and_upload()

        sentence, created = Video.objects.update_or_create(
            video_id=video_details["video_id"],
            defaults={
                "word": video_details["word"],
                "sentence": video_details["sentence"],
                "translated_sentence": video_details["translated_sentence"],
                "title": video_details["title"],
                "description": video_details["description"],
                "upload_date": timezone.make_aware(video_details["upload_time"], datetime.timezone.utc),
                "thumbnail_url": video_details["thumbnail_url"],
            }
        )

        if created:
            self.stdout.write(f"New video created with ID: {video_details['video_id']} "
                              f"for word: {video_details['word']}")
        else:
            self.stdout.write("No new video created")
