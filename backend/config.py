import os
from typing import Dict, List

class DLPConfig:
    # Sensitive Data Patterns
    SENSITIVE_PATTERNS: Dict[str, str] = {
        'credit_card': r'\b(?:\d{4}[-\s]?){3}\d{4}\b',
        'social_security': r'\b\d{3}-\d{2}-\d{4}\b',
        'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
        'confidential_keywords': r'\b(confidential|private|restricted)\b'
    }

    # File Size Limits
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB

    # Logging Configuration
    LOGGING_CONFIG: Dict[str, str] = {
        'log_dir': '/var/log/dlp_email_solution',
        'log_level': 'INFO',
        'log_file': 'dlp_email.log'
    }

    # Database Configuration
    DATABASE_CONFIG: Dict[str, str] = {
        'type': 'sqlite',
        'path': os.path.join(os.path.dirname(__file__), 'database', 'dlp_database.db')
    }

    # Email Server Configuration
    POSTFIX_CONFIG: Dict[str, int] = {
        'milter_socket': 'inet:8000@localhost',
        'milter_timeout': 300  # seconds
    }

    # Exception Types
    EXCEPTION_TYPES: List[str] = [
        'sender_domain',
        'recipient_domain', 
        'specific_email',
        'ip_range'
    ]

    @classmethod
    def get_sensitive_patterns(cls) -> Dict[str, str]:
        """
        Retrieve sensitive patterns
        """
        return cls.SENSITIVE_PATTERNS

    @classmethod
    def get_logging_config(cls) -> Dict[str, str]:
        """
        Retrieve logging configuration
        """
        return cls.LOGGING_CONFIG