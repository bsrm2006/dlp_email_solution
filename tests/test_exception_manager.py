import unittest
import os
import tempfile
from backend.exception_manager import EnhancedExceptionManager
from datetime import datetime, timedelta

class TestExceptionManager(unittest.TestCase):
    def setUp(self):
        """
        Setup test environment
        """
        # Create a temporary database
        self.temp_db = tempfile.mktemp()
        self.exception_manager = EnhancedExceptionManager(db_path=self.temp_db)

    def test_add_exception(self):
        """
        Test adding a valid exception
        """
        exception_data = {
            'exception_type': 'sender_domain',
            'exception_value': 'example.com',
            'reason': 'Test exception',
            'severity': 'low',
            'is_active': True,
            'expiration': (datetime.now() + timedelta(days=30)).strftime('%Y-%m-%d')
        }

        result = self.exception_manager.add_exception(exception_data)
        self.assertEqual(result['status'], 'success')
        self.assertIsNotNone(result.get('exception_id'))

    def test_invalid_exception(self):
        """
        Test adding an invalid exception
        """
        invalid_exception = {
            'exception_type': 'sender_domain',
            'exception_value': 'invalid-domain'  # Invalid domain format
        }

        result = self.exception_manager.add_exception(invalid_exception)
        self.assertEqual(result['status'], 'error')

    def test_exception_expiration(self):
        """
        Test exception with past expiration date
        """
        expired_exception = {
            'exception_type': 'specific_email',
            'exception_value': 'test@example.com',
            'expiration': (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
        }

        result = self.exception_manager.add_exception(expired_exception)
        self.assertEqual(result['status'], 'error')

    def test_get_exceptions(self):
        """
        Test retrieving exceptions
        """
        # Add some test exceptions
        test_exceptions = [
            {
                'exception_type': 'sender_domain',
                'exception_value': 'example.com',
                'is_active': True
            },
            {
                'exception_type': 'recipient_domain',
                'exception_value': 'company.com',
                'is_active': True
            }
        ]

        for exception in test_exceptions:
            self.exception_manager.add_exception(exception)

        # Retrieve exceptions
        exceptions = self.exception_manager.get_exceptions()
        self.assertTrue(len(exceptions) > 0)

    def tearDown(self):
        """
        Clean up temporary database
        """
        if os.path.exists(self.temp_db):
            os.remove(self.temp_db)

if __name__ == '__main__':
    unittest.main()