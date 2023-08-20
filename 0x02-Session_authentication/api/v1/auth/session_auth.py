#!/usr/bin/env python3
'''This is a module'''

from api.v1.auth.auth import Auth
import uuid


class SessionAuth(Auth):
    '''a sessionauth class
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        '''create a session ID for a user_id
        '''
        if (user_id is None or
                type(user_id) != str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id
