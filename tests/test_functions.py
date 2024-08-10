"""Module for testing the main functionality"""

import unittest
import os
from unittest.mock import patch

from word_generator import WordGenerator, SentenceGenerator


class TestWordGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mock_get = patch("word_generator.requests.get")
        cls.mock_get.start()
        cls.word_generator = WordGenerator(os.path.join(os.path.dirname(__file__), "test_word_list.txt"))

    @classmethod
    def tearDownClass(cls) -> None:
        cls.mock_get.stop()

    def test_read_text_file(self):
        expected_text = ["apple", "banana", "orange"]
        self.assertEqual(self.word_generator.text_file, expected_text)

    def test_get_random_word(self):
        random_word = self.word_generator.get_random_word()
        self.assertIn(random_word, self.word_generator.text_file)

    @patch("word_generator.requests.get")
    def test_test_real_word(self, mock_get):
        mock_get.return_value.json.return_value = {"n_results": 1}
        self.assertTrue(self.word_generator.test_real_word("apple", "en"))

    @patch("word_generator.requests.get")
    def test_test_real_word_fake(self, mock_get):
        mock_get.return_value.json.return_value = {"n_results": 0}
        self.assertFalse(self.word_generator.test_real_word("blah", "en"))


if __name__ == "__main__":
    unittest.main()
