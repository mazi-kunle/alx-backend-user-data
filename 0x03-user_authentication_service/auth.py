#!/usr/bin/env python3
'''This is a module'''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    '''returns a satled hash of the input password
    '''
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''register a user
        '''
        # check if user exists
        try:
            user = self._db.find_user_by(email=email)
        # if not add user
        except NoResultFound:
            hashed_password = _hash_password(password)
            return self._db.add_user(email, hashed_password)
        else:
            raise ValueError(f'User {email} already exists')