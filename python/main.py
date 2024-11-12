from typing import Dict
from datetime import datetime

from python.word_generator import Audio, ImageGenerator, VideoGenerator
from python.yt_uploader import YTConnector
from python.constants import Paths, LANGUAGE_TO_LEARN, NATIVE_LANGUAGE, Prompts


def process_video_and_upload() -> Dict[str, str]:
    """
    Combines the main functionality of the project to generate audio and video for a random word
    :return: a dictionary with the ID of the uploaded video, and the word, sentence and translated sentence that the
    video is based on
    """
    audio_generator = Audio(
        word_list_path=Paths.WORD_LIST_PATH,
        language_to_learn=LANGUAGE_TO_LEARN,
        native_language=NATIVE_LANGUAGE
    )

    print(audio_generator.word)
    print(audio_generator.sentence)
    print(audio_generator.translated_sentence)

    prompt = Prompts.IMAGE_GENERATOR + audio_generator.sentence

    image_generator = ImageGenerator(
        prompts=prompt,
    )

    video_generator = VideoGenerator(
        word=audio_generator.word,
        sentence=audio_generator.sentence,
        translated_sentence=audio_generator.translated_sentence,
        image_paths=image_generator.image_paths,
        audio_filepath=audio_generator.audio_path,
        subtitles_filepath=audio_generator.sub_filepath
    )

    video_filepath = video_generator.generate_video()
    video_metadata = video_generator.generate_video_metadata(language_code=LANGUAGE_TO_LEARN)

    yt = YTConnector(
        credentials_env=True
    )
    upload_details = yt.upload_youtube_short(
        video_path=video_filepath,
        title=video_metadata["title"],  # type: ignore[arg-type]
        description=video_metadata["description"],  # type: ignore[arg-type]
        tags=video_metadata["tags"]
    )

    video_id = upload_details["id"]
    thumbnail_url = upload_details["snippet"]["thumbnails"]["default"]["url"]
    upload_time = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")

    print(video_id)
    response = {
        "video_id": video_id,
        "word": audio_generator.word,
        "sentence": audio_generator.sentence,
        "translated_sentence": audio_generator.translated_sentence,
        "title": video_metadata["title"],
        "description": video_metadata["description"],
        "upload_time": upload_time,
        "thumbnail_url": thumbnail_url
    }
    return response
