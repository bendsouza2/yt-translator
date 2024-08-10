import random
from datetime import datetime, timedelta
import os
import re

import requests
from gtts import gTTS
from soundfile import SoundFile
from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from deep_translator import GoogleTranslator

from constants import Prompts, URLs, LANGUAGE_TO_LEARN, NATIVE_LANGUAGE, ModelTypes, VideoSettings


class WordGenerator:

    def __init__(self, word_list_path):
        self.file_path = word_list_path
        self.text_file = self.read_text_file()
        self.trial_word = self.get_random_word()
        self.word, self.word_is_real = self.get_real_word()

    def read_text_file(self) -> list:
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
        """
        return random.choice(self.text_file)

    def test_real_word(self, word: str = None, language_code: str = None) -> bool:
        """
        Test if a word is genuine by checking it is in the dictionary
        :param word: The word to test
        :param language_code: The language the word should exist in
        """

        if language_code is None:
            language_code = LANGUAGE_TO_LEARN

        if word is None:
            word = self.trial_word

        query = {"text": word, "language": language_code}
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
            real_word = self.test_real_word(word=word)
            self.remove_word_from_file(file_path=self.file_path, word_to_remove=word)
        return word, real_word


class SentenceGenerator:

    def __init__(self, word: str):
        self.word = word
        self.sentence = self.generate_example_sentence()
        self.translated_sentence = self.google_translate(
            source_language=LANGUAGE_TO_LEARN, target_language=NATIVE_LANGUAGE
        )

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
        return sentence

    def translate_example_sentence_gpt(self) -> ChatCompletion:
        """Generate an example sentence demonstrating the context of a given word"""
        client = OpenAI(api_key=os.getenv("openai_key"))
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": Prompts.SENTENCE_TRANSLATOR.format(
                        sentence=self.sentence
                    ),
                }
            ],
        )
        return completion

    def google_translate(
        self, target_language: str, source_language: str = None
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


def fix_accented_string(input_string):
    """Not Yet Implemented"""
    raise NotImplementedError


class ImageGenerator:

    def __init__(self, prompts: str | list):
        self.prompts = prompts
        self.image_urls = self.image_generator()
        self.save_image()

    def call_dalle(self, sentence: str):
        """
        Make a call to DALL-E API
        :param sentence: The prompt for the API to base the image on
        """
        client = OpenAI(api_key=os.getenv("openai_key"))
        response = client.images.generate(
            model=ModelTypes.DALLE_MODEL,
            prompt=sentence,
            size=VideoSettings.IMAGE_SIZE,
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
            raise TypeError("prompts argument must be either string or list")

    def save_image(self):
        """
        Save images to local directory
        """
        for url in self.image_urls:
            dt = datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")
            filepath = os.getcwd() + f"/images/{dt}.jpg"
            img_data = requests.get(url).content
            with open(filepath, 'wb') as handler:
                handler.write(img_data)


def spanish_syllable_count(word) -> int:
    """
    Get the number of syllables in a Spanish word
    :param word: the word to count the syllables of
    """
    word = word.lower()
    vowels = "aeiouyéó"
    count = 0
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels:
            count += 1
    if count == 0:
        count += 1
    return count


class Audio:
    def __init__(self, sentence: str):
        self.sentence = sentence
        self.audio_path = self.text_to_speech(language=LANGUAGE_TO_LEARN)
        self.audio_duration = self.get_audio_duration()
        self.syllable_count = self.get_total_syllable_count_spanish()
        self.sub_filepath = self.generate_srt_file()

    def text_to_speech(self, language: str, filepath: str = None) -> str:
        """
        Generate an audio file
        :param language: The language that the audio should be generated in
        :param filepath: The filepath to save the resulting .mp3 file to
        """
        if filepath is None:
            dt = datetime.utcnow().strftime("%m-%d-%Y %H:%M:%S")
            filepath = os.getcwd() + f"/audio/{dt}.wav"
        tts = gTTS(self.sentence, lang=language)
        tts.save(filepath)
        return filepath

        # TODO - gtts accepts max 100 characters before splitting into multiple files - need to either have something in the
        # prompt that stops sentences > 100 characters being generated + a test that the returned sentence is < 100, OR need
        # a way of piecing together split audio files
        # On reflection think the best way to do this is probably to be able to piece together text files when they get split

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

    def generate_srt_file(self) -> str:
        """
        Writes the sentence to a .srt subtitle file
        """
        syllables_per_second = self.audio_duration / self.syllable_count
        subtitle_length = 3
        words = self.sentence.split(" ")
        phrases = []
        phrase = []
        phrase_time = 0
        for index, word in enumerate(words):
            syllable_count = spanish_syllable_count(word)
            phrase_time += syllable_count * syllables_per_second
            if phrase_time < subtitle_length:
                phrase.append(word)
            elif phrase_time > subtitle_length:
                phrases.append(phrase)
                phrase = [word]
                phrase_time = syllable_count * syllables_per_second

            if index == len(words) - 1 and phrases[-1] != phrase:
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

        srtout = os.path.join(os.path.dirname(__file__), "/subtitles.srt")
        with open(srtout, "w") as newfile:
            newfile.write(srt_reformatted)

        return srtout
