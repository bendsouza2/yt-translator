"""Module for storing constants for the project"""

from dataclasses import dataclass
from typing import Literal, Final, Dict

LANGUAGE_TO_LEARN = "es"
NATIVE_LANGUAGE = "en"

THREE_LETTER_MAP: Final[Dict[str, str]] = {
    "eng": "en",  # English
    "spa": "es",  # Spanish
    "fra": "fr",  # French
    "deu": "de",  # German
    "ita": "it",  # Italian
    "por": "pt",  # Portuguese
    "nld": "nl",  # Dutch
    "rus": "ru",  # Russian
    "swe": "sv",  # Swedish
    "nor": "no",  # Norwegian
    "dan": "da",  # Danish
    "fin": "fi",  # Finnish
    "pol": "pl",  # Polish
    "ell": "el",  # Greek
    "hun": "hu",  # Hungarian
    "bul": "bg",  # Bulgarian
    "ron": "ro",  # Romanian
    "ces": "cs",  # Czech
    "slk": "sk",  # Slovak
}

TWO_LETTER_MAP: Final[Dict[str, str]] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "de": "German",
    "it": "Italian",
    "pt": "Portuguese",
    "nl": "Dutch",
    "ru": "Russian",
    "sv": "Swedish",
    "no": "Norwegian",
    "da": "Danish",
    "fi": "Finnish",
    "pl": "Polish",
    "el": "Greek",
    "hu": "Hungarian",
    "bg": "Bulgarian",
    "ro": "Romanian",
    "cs": "Czech",
    "sk": "Slovak",
}


class EnvVariables:
    YOUTUBE_CREDENTIALS = "YOUTUBE_CREDENTIALS"


@dataclass
class Prompts:
    SENTENCE_GENERATOR = "escribe una frase de ejemplo sobre el uso de la palabra {word}"
    SENTENCE_TRANSLATOR = (
        f"Translate the following sentence from {TWO_LETTER_MAP[LANGUAGE_TO_LEARN]} "
        f"to {TWO_LETTER_MAP[NATIVE_LANGUAGE]}: "
    )
    WORD_TRANSLATOR = (
        f"What does the following {TWO_LETTER_MAP[LANGUAGE_TO_LEARN]} word mean "
        f"in {TWO_LETTER_MAP[NATIVE_LANGUAGE]}: "
    )
    SYSTEM_MESSAGE = "You are a helpful assistant designed to help a user learn languages"
    IMAGE_GENERATOR = F"Generate an image to match the following {TWO_LETTER_MAP[LANGUAGE_TO_LEARN]} sentence: "


@dataclass
class URLs:
    DICTIONARY_URL = "https://lexicala1.p.rapidapi.com/search"
    DICTIONARY_HOST = "lexicala1.p.rapidapi.com"


@dataclass
class ModelTypes:
    DALLE_MODEL = "dall-e-3"
    GPT_MODEL = "gpt-3.5-turbo"


@dataclass
class VideoSettings:
    SQUARE: Literal["1024x1024"] = "1024x1024"
    VERTICAL: Literal["1024x1792"] = "1024x1792"
    TAGS = ["languages", "education", "language learning"]


class Paths:
    WORD_LIST_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/top-10000-spanish-words.txt"
    SUBTITLE_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/subtitles"
    AUDIO_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/audio"
    IMAGE_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/images"
    NODE_SUBS_FILE_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/node/sync_subtitles.js"
    VIDEO_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/video"
    GOOGLE_CREDS_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/google_creds.json"
    YT_TOKEN_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/python/token.json"
