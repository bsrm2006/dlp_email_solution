import unittest
import os
import tempfile
from backend.email_scanner import EmailScanner
from backend.dlp_engine import DLPEngine

class TestEmailScanner(unittest.TestCase):
    def setUp(self):
        """
        Setup test environment
        """
        self.dlp_engine = DLPEngine()
        self.email_scanner = EmailScanner()
        
        # Create a temporary directory for test files
        self.test_dir = tempfile.mkdtemp()

    def _create_test_email(self, content):
        """
        Create a temporary email file for testing
        """
        temp_file = os.path.join(self.test_dir, 'test_email.eml')
        with open(temp_file, 'w') as f:
            f.write(content)
        return temp_file

    def test_safe_email_scanning(self):
        """
        Test scanning a safe email
        """
        safe_email = self._create_test_email("""
        From: sender@example.com
        To: recipient@example.com
        Subject: Test Email

        This is a safe email content.
        """)

        result = self.email_scanner.process_email(safe_email)
        self.assertEqual(result['status'], 'PASS')

    def test_sensitive_email_scanning(self):
        """
        Test scanning an email with sensitive content
        """
        sensitive_email = self._create_test_email("""
        From: sender@example.com
        To: recipient@example.com
        Subject: Confidential Information

        Credit Card: 4111-1111-1111-1111
        Social Security: 123-45-6789
        """)

        result = self.email_scanner.process_email(sensitive_email)
        self.assertEqual(result['status'], 'BLOCK')
        self.assertTrue(len(result['content_violations']) > 0)

    def test_attachment_scanning(self):
        """
        Test email with attachments
        """
        # This would require creating a mock attachment
        pass

    def tearDown(self):
        """
        Clean up temporary files
        """
        for file in os.listdir(self.test_dir):
            os.remove(os.path.join(self.test_dir, file))
        os.rmdir(self.test_dir)

if __name__ == '__main__':
    unittest.main()