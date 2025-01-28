import sqlite3
from typing import Dict, List, Any
from datetime import datetime, timedelta
from backend.config import DLPConfig

class ExceptionManager:
    def __init__(self, db_path=None):
        """
        Initialize Exception Manager
        """
        self.db_path = db_path or DLPConfig.DATABASE_CONFIG['path']
        self._create_tables()

    def _create_tables(self):
        """
        Create necessary database tables
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS exceptions (
                    id INTEGER PRIMARY KEY,
                    type TEXT NOT NULL,
                    value TEXT NOT NULL,
                    expiration DATETIME,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()

    def add_exception(self, exception_data: Dict[str, Any]) -> bool:
        """
        Add a new exception to the database
        """
        required_fields = ['type', 'value']
        for field in required_fields:
            if field not in exception_data:
                raise ValueError(f"Missing required field: {field}")

        # Validate exception type
        if exception_data['type'] not in DLPConfig.EXCEPTION_TYPES:
            raise ValueError("Invalid exception type")

        # Optional expiration (default 30 days)
        expiration = exception_data.get(
            'expiration', 
            datetime.now() + timedelta(days=30)
        )

        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO exceptions 
                (type, value, expiration) 
                VALUES (?, ?, ?)
            ''', (
                exception_data['type'], 
                exception_data['value'], 
                expiration
            ))
            conn.commit()

        return True

    def is_exempt(self, sender: str, recipients: List[str]) -> bool:
        """
        Check if communication is exempt from DLP
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            current_time = datetime.now()

            # Check sender domain
            sender_domain = sender.split('@')[-1] if '@' in sender else sender
            cursor.execute('''
                SELECT 1 FROM exceptions 
                WHERE type = 'sender_domain' 
                AND value = ? 
                AND (expiration IS NULL OR expiration > ?)
            ''', (sender_domain, current_time))
            if cursor.fetchone():
                return True

            # Check recipient domains
            for recipient in recipients:
                recipient_domain = recipient.split('@')[-1] if '@' in recipient else recipient
                cursor.execute('''
                    SELECT 1 FROM exceptions 
                    WHERE type = 'recipient_domain' 
                    AND value = ? 
                    AND (expiration IS NULL OR expiration > ?)
                ''', (recipient_domain, current_time))
                if cursor.fetchone():
                    return True

            # Check specific email addresses
            for email_addr in [sender] + recipients:
                cursor.execute('''
                    SELECT 1 FROM exceptions 
                    WHERE type = 'specific_email' 
                    AND value = ? 
                    AND (expiration IS NULL OR expiration > ?)
                ''', (email_addr, current_time))
                if cursor.fetchone():
                    return True

        return False

    def get_exceptions(self, exception_type: str = None) -> List[Dict]:
        """
        Retrieve exceptions, optionally filtered by type
        """
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            if exception_type:
                cursor.execute('''
                    SELECT id, type, value, expiration 
                    FROM exceptions 
                    WHERE type = ? 
                    AND (expiration IS NULL OR expiration > CURRENT_TIMESTAMP)
                ''', (exception_type,))
            else:
                cursor.execute('''
                    SELECT id, type, value, expiration 
                    FROM exceptions 
                    WHERE expiration IS NULL OR expiration > CURRENT_TIMESTAMP
                ''')
            
            columns = ['id', 'type', 'value', 'expiration']
            return [dict(zip(columns, row)) for row in cursor.fetchall()]