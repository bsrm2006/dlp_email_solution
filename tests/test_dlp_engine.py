import unittest
from backend.dlp_engine import DLPEngine

class TestDLPEngine(unittest.TestCase):
    def setUp(self):
        self.dlp_engine = DLPEngine()

    def test_credit_card_detection(self):
        test_content = "Credit card: 4111-1111-1111-1111"
        result = self.dlp_engine.scan_content(test_content)
        self.assertFalse(result['is_safe'])
        self.assertTrue(any('credit_card' in violation['type'] for violation in result['violations']))

    def test_safe_content(self):
        test_content = "This is a safe email content"
        result = self.dlp_engine.scan_content(test_content)
        self.assertTrue(result['is_safe'])

if __name__ == '__main__':
    unittest.main()