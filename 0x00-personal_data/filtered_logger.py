#!/usr/bin/env python3
"""Regex-ing"""

from typing import List
import re
import logging


def filter_datum(fields: List[str], redaction: str, message: str,
                 separator: str) -> str:
    """Function that returns the log message obfuscated"""
    for field in fields:
        message = re.sub(rf'({field}=(.*?)){separator}',
                         f'{field}={redaction}{separator}', message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields):
        """Initializing the class"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Method to filter values in incoming log records using filter_datum
        """
        msg = filter_datum(self.fields, RedactingFormatter.REDACTION,
                                  record.msg, self.SEPARATOR)
        parts = msg.rsplit(self.SEPARATOR, 1)
        if len(parts) == 2:
            parts = parts[0].split(self.SEPARATOR) + [parts[1]]
            record.msg = ''
            for part in parts[:-1]:
                record.msg += f"{part} {self.SEPARATOR}"
            record.msg += parts[-1]
        return super().format(record)
