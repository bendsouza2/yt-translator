"""Module for storing constants for the project"""
import os
from dataclasses import dataclass
from typing import Literal

LANGUAGE_TO_LEARN = "es"
NATIVE_LANGUAGE = "en"


@dataclass
class Prompts:
    SENTENCE_GENERATOR = "escribe una frase de ejemplo sobre el uso de la palabra {word}"
    SENTENCE_TRANSLATOR = "Translate the following sentence from Spanish to English: {sentence}"
    WORD_TRANSLATOR = "What does the following Spanish word mean in English: '{word}'"
    SYSTEM_MESSAGE = "You are a helpful assistant designed to help a user learn languages"
    IMAGE_GENERATOR = "Generate an image to match the following Spanish sentence {sentence}"


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


class Paths:
    WORD_LIST_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/top-10000-spanish-words.txt"
    SUBTITLE_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/subtitles"
    AUDIO_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/audio"
    IMAGE_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/images"
    NODE_SUBS_FILE_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/node/sync_subtitles.js"
    VIDEO_DIR_PATH = "/Users/bendsouza/PycharmProjects/yt_translator/video"
