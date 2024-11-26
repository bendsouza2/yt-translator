"""Module containing utility functions for use across the project"""
import os
import tempfile


def spanish_syllable_count(word: str) -> int:
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


def remove_trailing_slash(string_to_check: str) -> str:
    """
    Remove forward slash at the end of a string
    :param string_to_check: The string to remove the forward slash from
    :return: The string with the forward slash removed
    """
    if string_to_check.endswith("/"):
        string_to_check = string_to_check[: -1]
    return string_to_check


def is_running_on_aws() -> bool:
    """
    Determine if the code is running in an AWS environment by checking for the existence of the 'AWS_EXECUTION_ENV'
    variable
    :return: True if running in an AWS env, else False
    """
    return os.getenv("AWS_EXECUTION_ENV") is not None


def write_bytes_to_local_temp_file(bytes_object: bytes, suffix: str, delete_file: bool = False) -> str:
    """
    Write a bytes object to the local file system temporarily
    :param bytes_object:
    :param suffix:
    :param delete_file:
    :return:
    """
    with tempfile.NamedTemporaryFile(suffix=suffix, delete=delete_file) as temp_file:
        temp_file.write(bytes_object)
        temp_file_path = temp_file.name
    return temp_file_path


def remove_temp_file(temp_file_path: str) -> bool:
    """
    Remove a temporary file from the local file system
    :param temp_file_path: The path to the temporary file
    :return: True if the file has been removed, False if it still exists
    """
    os.remove(temp_file_path)
    return not os.path.exists(temp_file_path)


def fix_accented_string(input_string: str) -> str:
    """Not Yet Implemented"""
    raise NotImplementedError
