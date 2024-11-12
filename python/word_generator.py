"""Module containing the functionality for generating sentences, audio and video for language learning resources"""

import random
from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict, Sequence
from pathlib import Path
import os
import re
import subprocess
import tempfile
import time

import requests
import numpy as np
from gtts import gTTS
from soundfile import SoundFile
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from deep_translator import GoogleTranslator
from moviepy.editor import ColorClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip, concatenate_videoclips
from moviepy.video.tools.subtitles import SubtitlesClip
from PIL import Image

from python.constants import Prompts, URLs, ModelTypes, VideoSettings, Paths, TWO_LETTER_MAP
from python.utils import spanish_syllable_count
from python.language_verification import LanguageVerification


Image.ANTIALIAS = Image.Resampling.LANCZOS  # type: ignore[attr-defined]


class Audio:
    def __init__(self,
                 word_list_path: str,
                 language_to_learn: str,
                 native_language: str,
                 ):
        """
        Initialise an Audio object
        :param word_list_path: The file path to the list of words.
        :param language_to_learn: The language the user is learning.
        :param native_language: The native language of the user.
        """
        self.file_path = word_list_path
        self.language_to_learn = language_to_learn
        self.native_language = native_language
        self.text_file = self.read_text_file()
        self.trial_word = self.get_random_word()
        self.word, self.word_is_real = self.get_real_word()
        self.sentence = self.generate_example_sentence()
        self.translated_sentence = self.google_translate(
            source_language=self.language_to_learn, target_language=self.native_language
        )
        self.audio_path = self.text_to_speech(language=self.language_to_learn)
        self.audio_duration = self.get_audio_duration()
        self.sub_filepath = self.echogarden_generate_subtitles(sentence=self.sentence)

    def text_to_speech(self, language: str, filepath: Optional[str] = None) -> str:
        """
        Generate an audio file
        :param language: The language that the audio should be generated in
        :param filepath: Optional, the filepath to save the resulting .mp3 file to
        """
        if filepath is None:
            dt = datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")
            filepath = f"{Paths.AUDIO_DIR_PATH}/{dt}.wav"
        tts = gTTS(self.sentence, lang=language)
        tts.save(filepath)
        return filepath

    def get_audio_duration(self) -> float:
        """
        Get the length in seconds of a .wav file
        """
        file = SoundFile(self.audio_path)
        samples = file.frames
        sample_rate = file.samplerate
        seconds = samples / sample_rate
        return seconds

    def get_total_syllable_count_spanish(self) -> int:
        """
        Get the total number of syllables in a Spanish sentence
        """
        sentence_count = 0
        for word in self.sentence:
            word_count = spanish_syllable_count(word)
            sentence_count += word_count
        return sentence_count

    def generate_srt_file(self, total_syllable_count: int) -> str:
        """
        Writes the sentence to a .srt subtitle file
        :param total_syllable_count: The total number of syllables in the audio
        """
        syllables_per_second = self.audio_duration / total_syllable_count
        subtitle_length = 3
        words = self.sentence.split(" ")
        phrases = []
        phrase = []
        phrase_time = 0.0
        for index, word in enumerate(words):
            syllable_count = spanish_syllable_count(word)
            phrase_time += syllable_count * syllables_per_second
            if phrase_time < subtitle_length:
                phrase.append(word)
            elif phrase_time > subtitle_length:
                phrases.append(phrase)
                phrase = [word]
                phrase_time = syllable_count * syllables_per_second

            if index == len(words) - 1 and len(phrases) == 0:
                phrases.append(phrase)
            elif index == len(words) - 1 and phrases[-1] != phrase:
                phrases.append(phrase)

        splits = len(phrases)
        sub_start = timedelta(hours=0, seconds=-subtitle_length)
        sub_duration = timedelta(seconds=subtitle_length)
        times = [sub_start + sub_duration for _ in range(splits + 1)]
        srt_list = [
            f"{i + 1}\n{times[i]},000 --> {times[i + 1]},000\n{phrases[i]}\n"
            for i in range(splits)
        ]
        srt = "\n".join(srt_list)

        pat = r"^(\d:)"
        repl = "0\\1"
        srt_reformatted = re.sub(pat, repl, srt, 0, re.MULTILINE)

        srtout = os.path.join(os.path.dirname(__file__), "subtitles.srt")
        with open(srtout, "w") as newfile:
            newfile.write(srt_reformatted)

        return srtout

    def echogarden_generate_subtitles(self, sentence: str) -> str:
        """
        Use the node.js package echogarden to sync an audio file with the text spoken in that audio file
        :param sentence: The text to match to the audio file
        :return: The output_file_path that the .srt file was written to if successfully generated, else None
        """
        dt = datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")
        output_file_path = f"{Paths.SUBTITLE_DIR_PATH}/{dt}.srt"
        command = ["node", Paths.NODE_SUBS_FILE_PATH, self.audio_path, sentence, output_file_path]
        try:
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise subprocess.CalledProcessError(
                e.returncode, e.cmd, stderr=f"Command failed with exit code {e.returncode}. stderr {e.stderr}"
            )

        return output_file_path

    def read_text_file(self) -> list:
        """
        Read a text file
        :return: list of lines in the text file
        """
        with open(self.file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
        return [line.strip() for line in lines]

    @staticmethod
    def remove_word_from_file(file_path: str, word_to_remove: str):
        """Remove a given word from a text file
        :param file_path: Path to the file
        :param word_to_remove: The word to remove from the file
        """
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines if line.strip() != word_to_remove]

        with open(file_path, "w", encoding="utf-8") as file:
            file.write("\n".join(lines))

    def get_random_word(self) -> str:
        """
        Choose a random word from the text file
        :return: a single word from the file
        """
        if len(self.text_file) == 0:
            raise ValueError("The text file is empty or does not exist. No content could be read from file")
        return random.choice(self.text_file)

    def test_real_word(self, word: Optional[str] = None) -> bool:
        """
        Test if a word is genuine by checking it is in the dictionary
        :param word: The word to test
        :return True if the word exists in the dictionary, else False
        """

        if word is None:
            word = self.trial_word

        query = {"text": word, "language": self.language_to_learn}
        headers = {
            "X-RapidAPI-Key": os.getenv("rapid_api_key"),
            "X-RapidAPI-Host": URLs.DICTIONARY_HOST,
        }
        response = requests.get(URLs.DICTIONARY_URL, headers=headers, params=query)
        if response.json()["n_results"] == 0:
            return False
        else:
            return True

    def get_real_word(self) -> tuple[str, bool]:
        """
        Generate a random word from the text file and recursively test its existence in the dictionary.
        Continues to select random words until a genuine word (i.e., found in the dictionary) is obtained.

        :return: A tuple containing the generated word and a boolean indicating whether it is genuine.
        """
        word = ""
        real_word = False

        while real_word is False:
            word = self.get_random_word()
            real_word = LanguageVerification(self.language_to_learn).enchant_real_word(word)
            self.remove_word_from_file(file_path=self.file_path, word_to_remove=word)
        return word, real_word

    def get_spanish_definition(self) -> Dict[str, List[str]]:
        """
        Get the definition of a word in Spanish and English
        :return: A dictionary with a list of definitions
        """
        response = LanguageVerification(self.language_to_learn).get_spanish_dictionary_definition(word=self.word)
        result = {}
        for entry in response:
            headword = entry.get('meta', {}).get('id')
            if headword != self.word:
                continue
            result["short"] = []
            for shortdef in entry.get("shortdef", []):
                result["short"].append(shortdef)
        return result

    def generate_example_sentence(self) -> str:
        """Generate an example sentence demonstrating the context of a given word"""
        client = OpenAI(api_key=os.getenv("openai_key"))
        completion = client.chat.completions.create(
            model=ModelTypes.GPT_MODEL,
            messages=[
                {
                    "role": "user",
                    "content": Prompts.SENTENCE_GENERATOR.format(word=self.word),
                }
            ],
        )

        sentence = completion.choices[0].message.content
        return sentence  # type: ignore

    def translate_example_sentence_gpt(self) -> ChatCompletion:
        """Generate an example sentence demonstrating the context of a given word"""
        client = OpenAI(api_key=os.getenv("openai_key"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": Prompts.SENTENCE_TRANSLATOR + self.sentence,
                }
            ],
        )
        return completion

    def google_translate(
        self, target_language: str, source_language: Optional[str] = None
    ) -> str:
        """
        Translate a sentence into your target language
        :param target_language: The language you want to translate to
        :param source_language: The current language of the sentence, if None the translator will attempt to guess the
        source language
        """
        if source_language is None:
            source_language = "auto"
        translator = GoogleTranslator(source=source_language, target=target_language)
        translated_sentence = translator.translate(self.sentence)
        return translated_sentence


class ImageGenerator:
    """
    Can be used to generate and store images
    """
    def __init__(
            self,
            prompts: str | list,
            local_image_storage: Optional[bool] = True,
            local_file_path: Optional[str] = None,
            s3_file_path: Optional[str] = None,
    ):
        """
        Initialise an object of the ImageGenerator class
        :param prompts: The prompts to use to create the image
        :param local_image_storage: Optional. Whether to store the image locally or remotely. Defaults to True
        :param local_file_path: Optional. The file path if storing the file locally
        :param s3_file_path: Optional. The file path if storing the file in S3
        """
        self.prompts = prompts
        self.image_urls = self.image_generator()
        self.image_paths = self.save_image()
        self.local_image_storage = local_image_storage
        self._check_valid_image_path()

    def call_dalle(self, sentence: str):
        """
        Make a call to DALL-E API
        :param sentence: The prompt for the API to base the image on
        """
        client = OpenAI(api_key=os.getenv("openai_key"))
        response = client.images.generate(
            model=ModelTypes.DALLE_MODEL,
            prompt=sentence,
            size=VideoSettings.VERTICAL,
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url

        return image_url

    def image_generator(self) -> list:
        """
        Make calls to the DALL-E API
        """
        if isinstance(self.prompts, str):
            image = self.call_dalle(self.prompts)
            return [image]
        elif isinstance(self.prompts, list):
            images = [self.call_dalle(prompt) for prompt in self.prompts]
            return images
        else:
            raise TypeError(f"prompts argument must be either string or list, got type {type(self.prompts)}")

    def save_image(self):
        """
        Save images to local directory
        """
        filepaths = []
        for url in self.image_urls:
            dt = datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")
            output_file_path = f"{Paths.IMAGE_DIR_PATH}/{dt}.jpg"
            img_data = requests.get(url).content
            with open(output_file_path, "wb") as handler:
                handler.write(img_data)
            filepaths.append(output_file_path)
        return filepaths

    def save_image_to_s3(self):
        """
        Save images to S3
        """
        raise NotImplementedError

    def _check_valid_image_path(self):
        """
        Check the image is saved to a valid location
        """
        if self.local_image_storage is True:
            for local_image_path in self.image_paths:
                file_path = Path(local_image_path)
                if not file_path.is_file():
                    raise ValueError(f"Either the image path you provided could not be located, or an image could not "
                                     f"be found in the default path location.")
        elif self.local_image_storage is False:
            raise NotImplementedError


class VideoGenerator:
    """Class for generating videos"""

    def __init__(self,
                 word: str,
                 sentence: str,
                 translated_sentence: str,
                 image_paths: List[str],
                 audio_filepath: str,
                 subtitles_filepath: str,
                 local_image_storage: bool = False,
                 ):
        """
        Initialise a VideoGenerator object
        :param word: the key word from the sentence
        :param sentence: the sentence to display subtitles for
        :param translated_sentence: the sentence translated to the native language
        :param image_paths: a list of paths to images to use in the video
        :param audio_filepath: the path to the audio file
        :param subtitles_filepath: the path to the subtitles
        :param local_image_storage: True if the images are stored locally, False otherwise
        """
        self.word = word
        self.sentence = sentence
        self.translated_sentence = translated_sentence
        self.image_paths = image_paths
        self.audio_filepath = audio_filepath
        self.subtitles_filepath = subtitles_filepath
        self.local_image_storage = local_image_storage

    @staticmethod
    def create_subtitle_clip(
            text: str,
            font_size: int = 50,
            colour: str = "white",
            background_opacity: float = 0.7,
            text_pos: Tuple[str, str] | Tuple[int, int] | Tuple[float, float] = ("center", "center"),
            font: str = "Courier",
            padding: int = 60
    ) -> CompositeVideoClip:
        """
        Create subtitles for given text with dynamic background width.
        :param text: the text to create a TextClip for
        :param font_size: the size of font to use for the subtitles
        :param colour: the colour to use for the subtitles
        :param background_opacity: the opacity of the background of the subtitles
        :param text_pos: where to display the subtitles
        :param font: The font for the text
        :param padding: padding for background width around the text
        :return: CompositeVideoClip consisting of the subtitles
        """
        text_clip = TextClip(text, fontsize=font_size, color=colour, font=font)

        width, height = text_clip.size
        background = ColorClip(
            size=(width + padding * 2, height),
            color=(0, 0, 0)
        ).set_opacity(background_opacity)

        final_clip = CompositeVideoClip([background.set_position(text_pos), text_clip.set_position(text_pos)])
        return final_clip.set_duration(text_clip.duration)

    def create_translated_subtitle_clip(
            self,
            translated_sentence: str,
            audio_duration: float,
            font_size: int = 50,
            colour: str = "white",
            font: str = "Courier",
            padding: int = 60
    ) -> CompositeVideoClip:
        """
        Creates a subtitle clip for a translated sentence with dynamically resizing background.
        :param translated_sentence: The translated sentence to display as subtitles.
        :param audio_duration: The total duration of the audio.
        :param font_size: The font size for the subtitles.
        :param colour: The colour for the subtitles.
        :param font: The font for the text.
        :param padding: Padding for the subtitle background
        :return: A CompositeVideoClip containing the timed translated subtitles.
        """
        words = translated_sentence.split()
        word_groups = [words[i:i + 3] for i in range(0, len(words), 3)]

        group_count = len(word_groups)
        display_duration = audio_duration / group_count

        subtitle_clips = []
        current_time = 0.0

        for group in word_groups:
            text = " ".join(group)

            subtitle_clip = self.create_subtitle_clip(
                text=text,
                font_size=font_size,
                colour=colour,
                text_pos=("center", "top"),
                font=font,
                padding=padding
            ).set_start(current_time).set_duration(display_duration)

            subtitle_clips.append(subtitle_clip)
            current_time += display_duration

        final_subtitle_clip = CompositeVideoClip(subtitle_clips)
        return final_subtitle_clip

    def create_translated_subtitles_file(self, audio_duration: float) -> str:
        """
        Creates a temporary SRT file for translated subtitles.
        :param audio_duration: Duration of the audio clip
        :return: Path to the created subtitles file
        """
        words = self.translated_sentence.split()
        word_groups = [words[i:i + 3] for i in range(0, len(words), 3)]

        group_count = len(word_groups)
        display_duration = audio_duration / group_count

        temp_srt = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.srt')

        for idx, group in enumerate(word_groups):
            start_time = idx * display_duration
            end_time = (idx + 1) * display_duration

            start_str = time.strftime('%H:%M:%S,000', time.gmtime(start_time))
            end_str = time.strftime('%H:%M:%S,000', time.gmtime(end_time))

            temp_srt.write(f"{idx + 1}\n")
            temp_srt.write(f"{start_str} --> {end_str}\n")
            temp_srt.write(f"{' '.join(group)}\n\n")

        temp_srt.close()
        return temp_srt.name

    @staticmethod
    def create_fancy_word_clip(
            word: str,
            font_size: int = 80,
            font: str = "Toppan-Bunkyu-Gothic-Demibold",
            duration: float = 1.0,
            stroke_colour: str = "green",
            style: str = "bounce"
    ) -> CompositeVideoClip:
        """
        Create a centered text clip for the given word
        :param word: The word to visualise
        :param font_size: The font size to display the word in
        :param font: The font to display the word in, defaults to 'Courier'
        :param duration: The length of time to display the text clip for
        :param stroke_colour: The outer/lining colour of the font
        :param style: The effect to apply to the text clip
        :return: a CompositeVideoClip with the applied effects
        """

        effects = {
            'bounce': lambda t: ('center', 'center' + 20 * np.sin(2 * np.pi * t)),
            'fade': lambda t: 0.7 + 0.3 * np.sin(2 * np.pi * t)
        }

        word_text = TextClip(
            txt=word,
            fontsize=font_size,
            font=font,
            color='white',
            stroke_color=stroke_colour,
            stroke_width=5,
            kerning=-2
        )

        background = ColorClip(                                 # TODO - change background to have rounded edges
            size=(word_text.w + 100, word_text.h + 20),
            color=(128, 128, 128)
        ).set_opacity(0.7)

        if style == 'bounce':
            word_clip = CompositeVideoClip([background.set_position('center'), word_text.set_position('center')])
            word_clip = word_clip.set_position(effects['bounce'])
        elif style == 'fade':
            word_clip = CompositeVideoClip([background, word_text]).set_opacity(effects['fade'])
        else:
            raise ValueError(f"{style} is not a recognised style. Use either 'bounce' or 'fade")

        shadow = TextClip(
            txt=word,
            fontsize=font_size,
            font=font,
            color='gray',
            stroke_width=0,
            kerning=-2
        ).set_position(lambda t: ('center', int(word_text.h / 2 + 10))).set_opacity(0.3)

        final_clip = CompositeVideoClip([shadow, word_clip.set_position('center')]).set_duration(duration)

        return final_clip

    def generate_video(self, output_filepath: Optional[str] = None, word_font: str = "Courier") -> str:
        """
        Combine audio, images, word overlay and subtitles to generate and save a video
        :param output_filepath: the absolute path to store the generated video
        :param word_font: The font for the text
        :return: the file path to where the video is written
        """
        if output_filepath is None:
            dt = datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")
            output_filepath = f"{Paths.VIDEO_DIR_PATH}/{dt}.mp4"

        audio_clip = AudioFileClip(self.audio_filepath)
        image_clips = [
            ImageClip(image).set_duration(audio_clip.duration / len(self.image_paths)) for image in self.image_paths
        ]

        word_clip = self.create_fancy_word_clip(
            word=self.word,
            font_size=80,
            font=word_font,
            duration=audio_clip.duration,
            style='bounce'
        )

        subtitles = SubtitlesClip(self.subtitles_filepath, self.create_subtitle_clip)

        translated_srt = self.create_translated_subtitles_file(audio_clip.duration)
        translated_subtitles = SubtitlesClip(translated_srt, lambda txt: self.create_subtitle_clip(
            txt,
            text_pos=("center", "top")
        ))

        video_clip = concatenate_videoclips(image_clips)
        video_clip = video_clip.set_audio(audio_clip)
        video_clip.duration = audio_clip.duration

        final_video = CompositeVideoClip([
            video_clip,
            word_clip.set_pos(('center', 'center')),
            subtitles.set_pos(('center', 'bottom')),
            translated_subtitles.set_pos(('center', 'top')),
        ])

        final_video.duration = video_clip.duration
        final_video.write_videofile(
            output_filepath,
            fps=24,
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
            codec="libx264",
            audio_codec="aac"
        )

        os.unlink(translated_srt)

        # Close clips to free up resources
        audio_clip.close()
        subtitles.close()
        translated_subtitles.close()
        word_clip.close()
        final_video.close()
        for clip in image_clips:
            clip.close()

        return output_filepath

    def generate_video_title(self, language: str) -> str:
        """
        Generate a title for the video
        :param language: The language that the video is in
        :return: A string formatted to include the language
        """
        return f"{language} Word of the Day: {self.word}"

    def generate_video_description(self, language: str) -> str:
        """
        Generate a description explaining the content of the video
        :param language: the language that the video is in
        :return: a text description of the video
        """
        descr = f"Today's {language} word of the day is {self.word}. An example use of this word is: " \
                f"'{self.sentence}' which translates to {self.translated_sentence}"
        return descr

    @staticmethod
    def generate_video_tags(language: str) -> Sequence[str]:
        """
        Generate the tags for a video
        :param language: the language that the video is in
        :return: a list of tags which describe the video
        """
        tags = VideoSettings.TAGS
        tags.append(language)
        tags.append(f"Easy {language}")
        return tags

    def generate_video_metadata(self, language_code: str) -> Dict[str, str | Sequence[str]]:
        """
        Generate the metadata for a video
        :param language_code: the two letter language code representing the language that the video is in
        :return: A dictionary containing a video title, description and tags
        """
        language = TWO_LETTER_MAP.get(language_code, language_code)
        tags = self.generate_video_tags(language)
        description = self.generate_video_description(language)
        title = self.generate_video_title(language)
        meta = {
            "tags": tags,
            "description": description,
            "title": title,
        }
        return meta


