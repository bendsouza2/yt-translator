import os


class Prompts:
    SENTENCE_GENERATOR = "escribe una frase de ejemplo sobre el uso de la palabra {word}"
    SENTENCE_TRANSLATOR = "Translate the following sentence from Spanish to English: {sentence}"
    WORD_TRANSLATOR = "What does the following Spanish word mean in English: '{word}'"
    SYSTEM_MESSAGE = "You are a helpful assistant designed to help a user learn Spanish"
    IMAGE_GENERATOR = "generar una imagen relacionada con la palabra {word} en el contexto de la frase {sentence}"


WORD_LIST_PATH = os.getcwd() + "/top-10000-spanish-words.txt"
