#!/usr/bin/env python3
'''This is a module'''

from typing import List
import os
import re
import mysql.connector
import logging


PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''returns the log message obfuscated
    '''
    for f in fields:
        message = re.sub(f'{f}=.*?{separator}',
                         f'{f}={redaction}{separator}', message)
    return message


def get_logger() -> logging.Logger:
    '''a get logger function
    '''
    # create custom logger
    logger = logging.getLogger('user_data')
    logger.setLevel(logging.INFO)
    logger.propagate = False

    # create handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(RedactingFormatter(list(PII_FIELDS)))

    # Add handler to logger
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    '''
    returns a connector to the database
    '''
    db = os.getenv('PERSONAL_DATA_DB_NAME')
    username = os.getenv('PERSONAL_DATA_DB_USERNAME') or 'root'
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD') or ''
    host = os.getenv('PERSONAL_DATA_DB_HOST') or 'localhost'

    mydb = mysql.connector.connection.MySQLConnection(
        host=host,
        user=username,
        password=password,
        database=db
    )
    return mydb


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        '''a format method
        '''
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.getMessage(), self.SEPARATOR)
        return super().format(record)


def main() -> None:
    '''obtain a database connection using get_db
        and retrieve all rows in the users table
        and display each row under a filtered format like this:
    '''
    cnx = get_db()
    cur = cnx.cursor()

    cur.execute('SELECT * FROM users')
    logger = get_logger()

    data = cur.fetchall()
    fields = ['name', 'email', 'phone', 'ssn',
              'password', 'ip', 'last_login', 'user_agent']
    
    for i in data:
        msg = ''.join(f'{j}={k};' for j, k in zip(fields, i))
        logger.info(msg)
    
    cur.close()
    cnx.close()




if __name__ == '__main__':
    main()