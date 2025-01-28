#!/usr/bin/env python3
import sys
import Milter
import logging
import email
import os
from typing import List

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.email_scanner import EmailScanner
from backend.config import DLPConfig
from backend.logging_module import setup_logging

class PostfixDLPMilter(Milter.Milter):
    def __init__(self):
        self.logger = setup_logging()
        self.email_scanner = EmailScanner()
        self.temp_email_path = None
        self.email_parts = []

    def connect(self, hostname: str, family: int, port: int, address: str):
        """
        Handle incoming connection
        """
        self.logger.info(f"Connection from: {address}")
        return Milter.CONTINUE

    def envfrom(self, mailfrom: str, *args):
        """
        Process sender information
        """
        self.mailfrom = mailfrom
        # Create temporary file for email
        self.temp_email_path = f"/tmp/dlp_email_{os.getpid()}.eml"
        self.email_parts = []
        return Milter.CONTINUE

    def envrcpt(self, recipient: str, *args):
        """
        Process recipient information
        """
        if not hasattr(self, 'recipients'):
            self.recipients = []
        self.recipients.append(recipient)
        return Milter.CONTINUE

    def header(self, name: str, value: str):
        """
        Process email headers
        """
        self.email_parts.append(f"{name}: {value}")
        return Milter.CONTINUE

    def body(self, chunk: bytes):
        """
        Process email body
        """
        self.email_parts.append(chunk.decode('utf-8', errors='ignore'))
        return Milter.CONTINUE

    def eom(self):
        """
        End of message - perform DLP checks
        """
        try:
            # Write complete email to temporary file
            with open(self.temp_email_path, 'w') as f:
                f.write('\n'.join(self.email_parts))

            # Scan email
            scan_result = self.email_scanner.process_email(self.temp_email_path)

            # Clean up temporary file
            os.remove(self.temp_email_path)

            # Determine action based on scan result
            if scan_result['status'] == 'BLOCK':
                self.logger.warning(f"DLP Violation Detected: {scan_result}")
                return Milter.REJECT

            return Milter.ACCEPT

        except Exception as e:
            self.logger.error(f"Milter processing error: {e}")
            return Milter.TEMPFAIL

def main():
    """
    Initialize and run Milter
    """
    # Configure Milter
    Milter.factory = lambda: PostfixDLPMilter()
    
    # Run Milter
    socket_config = DLPConfig.POSTFIX_CONFIG['milter_socket']
    sys.exit(Milter.runmilter('dlp_milter', socket_config))

if __name__ == '__main__':
    main()