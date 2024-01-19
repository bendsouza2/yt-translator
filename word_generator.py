from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion

from constants import Prompts, WORD_LIST_PATH
import config


class WordGenerator:

    def __init__(self):
        self.text_file = self.read_text_file(WORD_LIST_PATH)

    @staticmethod
    def read_text_file(file_path: str):
        text = open(file_path, "r")
        return text

    @staticmethod
    def remove_word_from_file(file_path: str, word_to_remove: str):
        """Remove a given word from a text file
        :param file_path: Path to the file
        :param word_to_remove: The word to remove from the file
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        lines = [line.strip() for line in lines if line.strip() != word_to_remove]

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write('\n'.join(lines))


def generate_example_sentence(word: str) -> ChatCompletion:
    """Generate an example sentence demonstrating the context of a given word"""
    client = OpenAI(api_key=config.openai_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": Prompts.SENTENCE_GENERATOR.format(word=word)}
        ]
    )
    return completion


def translate_example_sentence(sentence: str) -> ChatCompletion:
    """Generate an example sentence demonstrating the context of a given word"""
    client = OpenAI(api_key=config.openai_key)
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": Prompts.SENTENCE_TRANSLATOR.format(sentence=sentence)}
        ]
    )
    return completion


