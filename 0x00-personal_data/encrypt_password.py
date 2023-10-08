#!/usr/bin/env python3
'''This is a module
'''

import bcrypt


def hash_password(password: str) -> bytes:
    '''a function that expects one string argument name password
        and returns a salted, hashed password, which is a byte string.
    '''
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed


def is_valid(hashed_password: bytes, password: str) -> bool:
    '''
    checks the validity of a password
    '''
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
