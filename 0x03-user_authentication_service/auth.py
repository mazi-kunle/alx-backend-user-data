#!/usr/bin/env python3
'''This is a module'''

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union


def _hash_password(password: str) -> bytes:
    '''returns a satled hash of the input password
    '''
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def _generate_uuid() -> str:
    '''generate uuid'''
    import uuid

    return str(uuid.uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        '''authenticate a user
        '''
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            return False
        else:
            password = password.encode('utf-8')
            if bcrypt.checkpw(password, user.hashed_password):
                return True
            return False

    def create_session(self, email: str) -> str:
        '''find user corresponding to email,
            generate a new UUID and store it
            in the database as the user's
            session_id

            Return: session id'''
        try:
            user = self._db.find_user_by(email=email)
        except Exception as e:
            pass
        else:
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        '''get user from session id
        '''
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception as e:
            return None
        else:
            return user

    def destroy_session(self, user_id: int) -> None:
        '''update current user's session to None
        '''
        self._db.update_user(user_id, session_id=None)
