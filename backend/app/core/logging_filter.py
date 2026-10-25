import logging

class SensitiveDataFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        msg = str(record.msg)
        for token in ['password', 'secret', 'token', 'authorization']:
            if token in msg.lower():
                record.msg = '[REDACTED_SENSITIVE_CREDENTIAL]'
        return True
