import random
import requests

from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from deep_translator import GoogleTranslator

from constants import Prompts, WORD_LIST_PATH, URLs, LANGUAGE_TO_LEARN, NATIVE_LANGUAGE
import config


class WordGenerator:
    def __init__(self):
        self.text_file = self.read_text_file(WORD_LIST_PATH)
        self.trial_word = self.get_random_word()
        self.word, self.word_is_real = self.get_real_word()

    @staticmethod
    def read_text_file(file_path: str) -> list:
        with open(file_path, "r", encoding="utf-8") as file:
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

        query = {
            "text": word,
            "language": language_code
        }
        headers = {
            "X-RapidAPI-Key": config.rapid_api_key,
            "X-RapidAPI-Host": URLs.DICTIONARY_HOST
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
            self.remove_word_from_file(file_path=WORD_LIST_PATH, word_to_remove=word)
        return word, real_word


class SentenceGenerator:
    def __init__(self, word: str):
        self.word = word
        self.sentence = self.generate_example_sentence()
        self.translated_sentence = self.google_translate(source_language=LANGUAGE_TO_LEARN,
                                                         target_language=NATIVE_LANGUAGE)

    def generate_example_sentence(self) -> ChatCompletion:
        """Generate an example sentence demonstrating the context of a given word"""
        client = OpenAI(api_key=config.openai_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": Prompts.SENTENCE_GENERATOR.format(word=self.word)}
            ],
        )
        return completion

    def translate_example_sentence_gpt(self) -> ChatCompletion:
        """Generate an example sentence demonstrating the context of a given word"""
        client = OpenAI(api_key=config.openai_key)
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": Prompts.SENTENCE_TRANSLATOR.format(sentence=self.sentence),
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
        sentence = self.sentence.choices[0].message.content
        translator = GoogleTranslator(source=source_language, target=target_language)
        translated_sentence = translator.translate(sentence)
        return translated_sentence


def fix_accented_string(input_string):
    """Not Yet Implemented"""
    raise NotImplementedError
