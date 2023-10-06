#!/usr/bin/env python3
'''This is a module'''

from typing import List
import re


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated
    '''
    for data in message.split(separator):
        if data.split('=')[0] in fields:
            message = re.sub(data.split('=')[1], redaction, message)
    return message
