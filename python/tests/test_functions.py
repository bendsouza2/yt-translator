"""Module for testing the main functionality"""

import unittest
import os
from unittest.mock import patch

from python.word_generator import Audio


class TestWordGenerator(unittest.TestCase):
    """Class for testing the functionality used to generate the daily word"""
    mock_get = None
    mock_google_translator = None
    mock_tts = None

    @classmethod
    def setUpClass(cls):
        """Setup class method for creating mocks and other attributes used across the tests"""
        cls.mock_get = patch("python.word_generator.requests.get").start()
        cls.mock_google_translator = patch("python.word_generator.GoogleTranslator").start()
        cls.mock_sentence_generator = patch("python.word_generator.OpenAI").start()
        cls.mock_remove_word_from_file = patch("python.word_generator.Audio.remove_word_from_file").start()
        cls.mock_enchant = patch("python.word_generator.LanguageVerification.enchant_real_word").start()

        cls.mock_tts = patch("python.word_generator.Audio.text_to_speech").start()
        cls.mock_get_audio_duration = patch("python.word_generator.Audio.get_audio_duration").start()
        cls.mock_generate_srt_file = patch("python.word_generator.Audio.echogarden_generate_subtitles").start()

        cls.mock_google_translator.return_value.translate.return_value = "Translated sentence"
        cls.audio = Audio(
            word_list_path=os.path.join(os.path.dirname(__file__), "test_word_list.txt"),
            language_to_learn="es",
            native_language="en"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down class method to stop mocks once tests have run"""
        cls.mock_get.stop()
        cls.mock_google_translator.stop()
        cls.mock_remove_word_from_file.stop()
        cls.mock_enchant.stop()

        cls.mock_tts.stop()
        cls.mock_get_audio_duration()
        cls.mock_get_total_syllable_count.stop()
        cls.mock_generate_srt_file.stop()

    def test_read_text_file(self):
        """Test reading a text file with a valid path and valid inputs"""
        expected_text = ["apple", "banana", "orange"]
        self.assertEqual(self.audio.text_file, expected_text)

    def test_read_text_file_bad_path(self):
        """Test reading a text file when the path used does not exist"""
        with self.assertRaises(FileNotFoundError):
            bad_path = Audio(
                word_list_path="does_not_exist.txt",
                language_to_learn="es",
                native_language="en"
            )

    def test_get_random_word(self):
        """Test getting a random word from the text file where the text file and its contents are valid"""
        random_word = self.audio.get_random_word()
        self.assertIn(random_word, self.audio.text_file)

    def test_get_random_word_empty_text_file(self):
        """Test that a ValueError is raised when trying to get a word from an empty text file"""
        with self.assertRaises(ValueError):
            empty_file_path = Audio(
                word_list_path=os.path.join(os.path.dirname(__file__), "empty_file.txt"),
                language_to_learn="es",
                native_language="en"
            )

    @patch("python.word_generator.requests.get")
    def test_test_real_word(self, mock_get):
        """Test the test_real_word() method when called with a real word"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"n_results": 1}
        self.assertTrue(self.audio.test_real_word("apple"))

    @patch("python.word_generator.requests.get")
    def test_test_real_word_fake(self, mock_get):
        """Test the test_real_word() method when called with a fake word"""
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"n_results": 0}
        self.assertFalse(self.audio.test_real_word("blah"))


if __name__ == "__main__":
    unittest.main()
