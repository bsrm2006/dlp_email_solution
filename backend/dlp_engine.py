import re
import hashlib
import logging
from typing import Dict, List

class DLPEngine:
    def __init__(self, config: Dict):
        self.sensitive_patterns = config.get('sensitive_patterns', [])
        self.max_file_size = config.get('max_file_size', 10 * 1024 * 1024)  # 10MB default
    
    def scan_content(self, email_content: str) -> Dict:
        """
        Scan email content for sensitive information
        """
        violations = []
        
        # Check for predefined sensitive patterns
        for pattern in self.sensitive_patterns:
            matches = re.findall(pattern, email_content)
            if matches:
                violations.append({
                    'type': 'content_match',
                    'pattern': pattern,
                    'matches': matches
                })
        
        # Additional checks can be added here
        
        return {
            'is_safe': len(violations) == 0,
            'violations': violations
        }
    
    def scan_attachment(self, file_path: str) -> Dict:
        """
        Scan email attachments
        """
        try:
            with open(file_path, 'rb') as f:
                file_content = f.read()
                
            # Check file size
            if len(file_content) > self.max_file_size:
                return {
                    'is_safe': False,
                    'reason': 'File size exceeds limit'
                }
            
            # File hash for tracking
            file_hash = hashlib.sha256(file_content).hexdigest()
            
            return {
                'is_safe': True,
                'file_hash': file_hash
            }
        
        except Exception as e:
            logging.error(f"Attachment scan error: {e}")
            return {
                'is_safe': False,
                'reason': str(e)
            }