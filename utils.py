"""Module containing utility functions for use across the project"""

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


def fix_accented_string(input_string: str) -> str:
    """Not Yet Implemented"""
    raise NotImplementedError
