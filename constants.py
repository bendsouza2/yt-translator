import os

LANGUAGE_TO_LEARN = "es"
NATIVE_LANGUAGE = "en"


class Prompts:
    SENTENCE_GENERATOR = "escribe una frase de ejemplo sobre el uso de la palabra {word}"
    SENTENCE_TRANSLATOR = "Translate the following sentence from Spanish to English: {sentence}"
    WORD_TRANSLATOR = "What does the following Spanish word mean in English: '{word}'"
    SYSTEM_MESSAGE = "You are a helpful assistant designed to help a user learn Spanish"
    # IMAGE_GENERATOR = "generar una imagen relacionada con la palabra {word} en el contexto de la frase {sentence}"
    # IMAGE_GENERATOR2 = "Genera una imagen de un {word}."
    IMAGE_GENERATOR = "{sentence}."


class URLs:
    DICTIONARY_URL = "https://lexicala1.p.rapidapi.com/search"
    DICTIONARY_HOST = "lexicala1.p.rapidapi.com"


class ModelTypes:
    DALLE_MODEL = "dall-e-2"
    GPT_MODEL = "gpt-3.5-turbo"


class VideoSettings:
    IMAGE_SIZE = "1024x1024"


WORD_LIST_PATH = os.getcwd() + "/top-10000-spanish-words.txt"
