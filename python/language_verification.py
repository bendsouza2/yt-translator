"""Module for verifying language using LLMs to verify that a word/sentence is real"""

import os

import requests
import spacy
import enchant

from python.constants import URLs


class LanguageVerification:
    """
    Used to verify language
    """

    def __init__(
            self,
            language: str,
    ):
        """
        Initialise a LanguageVerification object
        :param language: the language you want to verify a word for
        """
        self.language = language

    def lexical_test_real_word(self, word: str) -> bool:
        """
        Test if a word is genuine by checking it is in the dictionary
        :param word: The word to test
        :return True if the word exists in the dictionary, else False
        """

        query = {"text": word, "language": self.language}
        headers = {
            "X-RapidAPI-Key": os.getenv("rapid_api_key"),
            "X-RapidAPI-Host": URLs.DICTIONARY_HOST,
        }
        response = requests.get(URLs.DICTIONARY_URL, headers=headers, params=query)
        if response.json()["n_results"] == 0:
            return False
        else:
            return True

    def spacy_real_word(self, model: str, word: str) -> bool:
        """
        Test a word is real using Spacy. For more info see https://spacy.io/
        :param model: The model to use to help identify the word
        :param word: The word to test
        :return: True if the word exists for the given language, False if not
        """

        if model is None:
            model = f"{self.language}_core_news_sm"

        language = spacy.load(model)
        doc = language(word)
        return doc[0].is_alpha and not doc[0].is_stop

    def enchant_real_word(self, word: str) -> bool:
        """
        Test a word is real using enchant. For more info see https://pyenchant.github.io/pyenchant/install.html
        :param word: The word to test
        :return: True if the word exists for the given language, False if not
        """
        thesaurus = enchant.Dict(self.language)
        return thesaurus.check(word)
