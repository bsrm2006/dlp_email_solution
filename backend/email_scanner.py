import os
import email
import logging
from typing import Dict, Any
from backend.dlp_engine import DLPEngine
from backend.exception_manager import ExceptionManager

class EmailScanner:
    def __init__(self, config=None):
        """
        Initialize Email Scanner
        """
        self.dlp_engine = DLPEngine(config)
        self.exception_manager = ExceptionManager()
        self.logger = logging.getLogger(__name__)

    def process_email(self, email_file: str) -> Dict[str, Any]:
        """
        Comprehensive email processing and scanning
        """
        try:
            # Read email file
            with open(email_file, 'rb') as f:
                msg = email.message_from_binary_file(f)

            # Extract email metadata
            sender = msg.get('From', '')
            recipients = msg.get('To', '').split(',')

            # Check for exceptions
            if self.exception_manager.is_exempt(sender, recipients):
                return {
                    'status': 'PASS',
                    'reason': 'Exempted communication'
                }

            # Scan email content
            email_content = self._extract_email_content(msg)
            content_result = self.dlp_engine.scan_content(email_content)

            # Scan attachments
            attachment_results = self._scan_attachments(msg)

            # Determine overall email safety
            is_safe = (
                content_result['is_safe'] and 
                all(result['is_safe'] for result in attachment_results)
            )

            # Log results
            if not is_safe:
                self.logger.warning(f"DLP Violation Detected: {content_result}")

            return {
                'status': 'PASS' if is_safe else 'BLOCK',
                'content_violations': content_result.get('violations', []),
                'attachment_violations': attachment_results
            }

        except Exception as e:
            self.logger.error(f"Email processing error: {e}")
            return {
                'status': 'ERROR',
                'reason': str(e)
            }

    def _extract_email_content(self, msg: email.message.Message) -> str:
        """
        Extract email content from message
        """
        content = []
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                content.append(part.get_payload(decode=True).decode('utf-8', errors='ignore'))
        return '\n'.join(content)

    def _scan_attachments(self, msg: email.message.Message) -> list:
        """
        Scan email attachments
        """
        attachment_results = []
        for part in msg.walk():
            if part.get_content_maintype() == 'multipart':
                continue

            filename = part.get_filename()
            if filename:
                try:
                    # Save attachment temporarily
                    temp_path = os.path.join('/tmp', filename)
                    with open(temp_path, 'wb') as f:
                        f.write(part.get_payload(decode=True))

                    # Scan attachment
                    attachment_result = self.dlp_engine.scan_attachment(temp_path)
                    attachment_results.append(attachment_result)

                    # Clean up temporary file
                    os.remove(temp_path)

                except Exception as e:
                    self.logger.error(f"Attachment scanning error: {e}")
                    attachment_results.append({
                        'is_safe': False,
                        'reason': str(e)
                    })

        return attachment_results