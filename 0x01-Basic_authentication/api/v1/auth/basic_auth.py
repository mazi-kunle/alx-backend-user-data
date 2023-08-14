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
            return data_bytes.decode('utf-8')
