"""Module for testing the main functionality"""

import unittest
import os
from unittest.mock import patch

from python.word_generator import Audio


class TestWordGenerator(unittest.TestCase):
    mock_get = None
    mock_google_translator = None
    mock_tts = None

    @classmethod
    def setUpClass(cls):
        cls.mock_get = patch("python.word_generator.requests.get").start()
        cls.mock_google_translator = patch("python.word_generator.GoogleTranslator").start()
        cls.mock_remove_word_from_file = patch("python.word_generator.Audio.remove_word_from_file").start()
        cls.mock_enchant = patch("python.word_generator.LanguageVerification.enchant_real_word").start()

        # can remove mock attributes for these 5 methods once I write unit tests to test them in controlled env
        cls.mock_srt_file = patch("python.word_generator.Audio.generate_srt_file").start()
        cls.mock_tts = patch("python.word_generator.Audio.text_to_speech").start()
        cls.mock_get_audio_duration = patch("python.word_generator.Audio.get_audio_duration").start()
        cls.mock_get_total_syllable_count = patch("python.word_generator.Audio.get_total_syllable_count_spanish").start()
        cls.mock_generate_srt_file = patch("python.word_generator.Audio.echogarden_generate_subtitles").start()

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
        cls.mock_remove_word_from_file.stop()
        cls.mock_enchant.stop()

        cls.mock_srt_file.stop()
        cls.mock_tts.stop()
        cls.mock_get_audio_duration()
        cls.mock_get_total_syllable_count.stop()
        cls.mock_generate_srt_file.stop()

    def test_read_text_file(self):
        expected_text = ["apple", "banana", "orange"]
        self.assertEqual(self.audio.text_file, expected_text)

    def test_get_random_word(self):
        random_word = self.audio.get_random_word()
        self.assertIn(random_word, self.audio.text_file)

    @patch("python.word_generator.requests.get")
    def test_test_real_word(self, mock_get):
        #TODO need to amend these two tests --> delete this function from the Audio class and test the LangVerif instead
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"n_results": 1}
        self.assertTrue(self.audio.test_real_word("apple"))

    @patch("python.word_generator.requests.get")
    def test_test_real_word_fake(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"n_results": 0}
        self.assertFalse(self.audio.test_real_word("blah"))


if __name__ == "__main__":
    unittest.main()
