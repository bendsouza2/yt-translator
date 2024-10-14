from word_generator import Audio, ImageGenerator, VideoGenerator
from constants import Paths, LANGUAGE_TO_LEARN, NATIVE_LANGUAGE, Prompts

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

video_generator.generate_video()
