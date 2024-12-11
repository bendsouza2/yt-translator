from typing import Dict, Callable, Optional
from datetime import datetime

from python.word_generator import Audio, ImageGenerator, VideoGenerator
from python.yt_uploader import YTConnector
from python.constants import Paths, LANGUAGE_TO_LEARN, NATIVE_LANGUAGE, Prompts
from python.db_handler import write_to_db


def process_video_and_upload(write_to_rds: bool = False) -> Dict[str, str]:
    """
    Combines the main functionality to generate audio and video for a random word and upload it to YouTube.
    Optionally writes metadata to a database using `db_write_function`.
    :param write_to_rds: Write video metadata to MySQL instance hosted in RDS
    """
    audio_generator = Audio(
        word_list_path=Paths.WORD_LIST_PATH,
        language_to_learn=LANGUAGE_TO_LEARN,
        native_language=NATIVE_LANGUAGE,
        cloud_storage=True,
    )

    prompt = Prompts.IMAGE_GENERATOR + audio_generator.sentence
    image_generator = ImageGenerator(prompts=prompt, cloud_storage=True)

    if audio_generator.cloud_storage is True:
        audio_file = audio_generator.audio_cloud_path
    else:
        audio_file = audio_generator.audio_path

    if audio_file is None:
        raise TypeError(f"audio_file must be a string")
    video_generator = VideoGenerator(
        word=audio_generator.word,
        sentence=audio_generator.sentence,
        translated_sentence=audio_generator.translated_sentence,
        image_paths=image_generator.image_paths,
        audio_filepath=audio_file,
        cloud_storage=True,
    )

    video_filepath = video_generator.generate_video()
    video_metadata = video_generator.generate_video_metadata(language_code=LANGUAGE_TO_LEARN)

    yt = YTConnector(credentials_env=True, cloud_storage=True)
    upload_details = yt.upload_youtube_short(
        video_path=video_filepath,
        title=str(video_metadata["title"]),
        description=str(video_metadata["description"]),
        tags=video_metadata["tags"],
    )

    video_id = upload_details["id"]
    upload_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    response = {
        "video_id": video_id,
        "word": audio_generator.word,
        "sentence": audio_generator.sentence,
        "translated_sentence": audio_generator.translated_sentence,
        "title": video_metadata["title"],
        "description": video_metadata["description"],
        "upload_time": upload_time,
        "thumbnail_url": upload_details["snippet"]["thumbnails"]["default"]["url"],
    }

    if write_to_rds is True:
        write_to_db(response)

    return response
