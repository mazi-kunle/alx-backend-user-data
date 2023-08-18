#!/usr/bin/env python3
'''This is a module'''

import bcrypt


def _hash_password(password: str) -> bytes:
    '''returns a satled hash of the input password
    '''
    bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash

# from db import DB


# class Auth:
#     """Auth class to interact with the authentication database.
#     """

#     def __init__(self):
#         self._db = DB()
