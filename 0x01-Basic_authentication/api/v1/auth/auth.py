#!/usr/bin/env python3
'''This is a module'''

from flask import request
from typing import List
from typing import TypeVar


class Auth:
    '''Auth class
    '''
    def __init_(self) -> None:
        '''init function
        '''

    def require_auth(self,
                     path: str,
                     excluded_paths: List[str]) -> bool:
        '''
        returns False
        '''
        if (path is None or
                excluded_paths is None or
                (len(excluded_paths) == 0)):

            return True

        valid_path = path + '/' if path[-1] != '/' else path
        short_path = valid_path.split('/')[-2]

        for path in excluded_paths:
            path = path.split('/')[-1]
            if '*' in path:
                path = path[:-1]
                if short_path.startswith(path):
                    return False

        if valid_path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        '''A function
        '''

        if (request is None or
                'Authorization' not in dict(request.headers)):
            return None
        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        '''A function
        '''
        return None
