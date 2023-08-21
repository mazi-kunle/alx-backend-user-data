#!/usr/bin/env python3
'''This is a module'''

from api.v1.auth.auth import Auth
from typing import TypeVar


class BasicAuth(Auth):
    '''a basicauth class
    '''
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        '''returns the Base64 part of the
            Authorization header for a basic Authentication
        '''
        if (authorization_header is None or
                type(authorization_header) != str
                or authorization_header.split(' ')[0] != 'Basic'):

            return None

        return authorization_header.split(' ')[1]

    def decode_base64_authorization_header(
            self,
            base64_authorization_header: str
    ) -> str:
        '''returns the decoded value of a Base64 string
        '''
        if (base64_authorization_header is None or
                type(base64_authorization_header) != str):
            return None
        try:
            import base64
            base64.b64encode(
                base64.b64decode(base64_authorization_header)
            ) == base64_authorization_header
        except Exception:
            return None
        else:
            data_bytes = base64.b64decode(base64_authorization_header)
            try:
                return data_bytes.decode('utf-8')
            except UnicodeDecodeError:
                return None

    def extract_user_credentials(
            self,
            decoded_base64_authorization_header: str
    ) -> (str, str):
        '''return the user email and password from the Base64 decoded value'''
        if (decoded_base64_authorization_header is None or
                type(decoded_base64_authorization_header) != str or
                ':' not in decoded_base64_authorization_header):
            return None, None
        else:
            a, b = decoded_base64_authorization_header.split(':', maxsplit=1)
            return (a, b)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        '''a function'''
        if (type(user_email) != str or
                user_email is None or
                type(user_pwd) != str or
                user_pwd is None):
            return None

        from models.user import User
        User()
        user = User.search({'email': user_email})
        if len(user) == 0:
            return None
        elif user[0].is_valid_password(user_pwd):
            return user[0]
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        '''Overloads Auth and retrieve the User instance
            for a request.
        '''
        authorization_header = self.authorization_header(request)
        base64_auth_header = self.extract_base64_authorization_header(
                                authorization_header)

        decoded_auth_header = self.decode_base64_authorization_header(
                                base64_auth_header)
        user_credentials = self.extract_user_credentials(decoded_auth_header)

        user_object = self.user_object_from_credentials(
                        user_credentials[0],
                        user_credentials[1]
                        )
        return user_object
