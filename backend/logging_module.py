import os
import logging
from logging.handlers import RotatingFileHandler
from backend.config import DLPConfig

def setup_logging():
    """
    Configure logging for DLP solution
    """
    # Ensure log directory exists
    log_dir = DLPConfig.LOGGING_CONFIG['log_dir']
    os.makedirs(log_dir, exist_ok=True)

    # Full log file path
    log_file = os.path.join(log_dir, DLPConfig.LOGGING_CONFIG['log_file'])

    # Configure logging
    logger = logging.getLogger('dlp_email_solution')
    logger.setLevel(getattr(logging, DLPConfig.LOGGING_CONFIG['log_level']))

    # Create rotating file handler
    file_handler = RotatingFileHandler(
        log_file, 
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5
    )

    # Console handler
    console_handler = logging.StreamHandler()

    # Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger