"""Module for testing the main functionality"""

import unittest
import os
from unittest.mock import patch

from word_generator import Audio


class TestWordGenerator(unittest.TestCase):
    mock_get = None
    mock_google_translator = None

    @classmethod
    def setUpClass(cls):
        cls.mock_get = patch("word_generator.requests.get").start()
        cls.mock_google_translator = patch("word_generator.GoogleTranslator").start()
        cls.mock_srt_file = patch("word_generator.Audio.generate_srt_file").start()
        cls.mock_google_translator.return_value.translate.return_value = "Translated sentence"
        cls.audio = Audio(
            word_list_path=os.path.join(os.path.dirname(__file__), "test_word_list.txt"),
            language_to_learn="es",
            native_language="en"
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_get.stop()
        cls.mock_google_translator.stop()

    def test_read_text_file(self):
        expected_text = ["apple", "banana", "orange"]
        self.assertEqual(self.audio.text_file, expected_text)

    def test_get_random_word(self):
        random_word = self.audio.get_random_word()
        self.assertIn(random_word, self.audio.text_file)

    @patch("word_generator.requests.get")
    def test_test_real_word(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"n_results": 1}
        self.assertTrue(self.audio.test_real_word("apple"))

    @patch("word_generator.requests.get")
    def test_test_real_word_fake(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"n_results": 0}
        self.assertFalse(self.audio.test_real_word("blah"))


if __name__ == "__main__":
    unittest.main()
