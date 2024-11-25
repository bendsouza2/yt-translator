"""Module containing utility functions for use across the project"""
import os

import boto3

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


def upload_to_s3(file_path: str, bucket_name: str, s3_key):
    s3 = boto3.client('s3')
    s3.upload_file(file_path, bucket_name, s3_key)
    return f"s3://{bucket_name}/{s3_key}"


def fix_accented_string(input_string: str) -> str:
    """Not Yet Implemented"""
    raise NotImplementedError
