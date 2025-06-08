"""
This file is AI generated. Reviewed by human
"""

import unittest
from demo import AgenticSearchService


class TestFallbackKeywordExtraction(unittest.TestCase):
    def setUp(self):
        self.service = AgenticSearchService()

    def test_fallback_keyword_extraction(self):
        # Test with a simple question
        question = "What is the capital of France?"
        expected_keywords = ["capital", "france"]
        result = self.service._fallback_keyword_extraction(question)
        self.assertEqual(result, expected_keywords)

        # Test with a question containing stop words and short words
        question = "How artificial intelligence work in modern cars?"
        expected_keywords = ["artificial", "intelligence", "work", "modern", "cars"]
        result = self.service._fallback_keyword_extraction(question)
        self.assertEqual(result, expected_keywords)

        # Test with a question that has no meaningful keywords
        question = "Is it the or a?"
        expected_keywords = []
        result = self.service._fallback_keyword_extraction(question)
        self.assertEqual(result, expected_keywords)

        # Test with a question that has more than 5 meaningful keywords
        question = "What are the best practices for Python web development in 2024?"
        expected_keywords = ["best", "practices", "python", "web", "development"]
        result = self.service._fallback_keyword_extraction(question)
        self.assertEqual(result, expected_keywords)


if __name__ == "__main__":
    unittest.main()
