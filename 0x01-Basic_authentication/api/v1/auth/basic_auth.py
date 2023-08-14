#!/usr/bin/env python3
'''This is a module'''

from api.v1.auth.auth import Auth


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
