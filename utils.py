

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


def fix_accented_string(input_string: str) -> str:
    """Not Yet Implemented"""
    raise NotImplementedError
