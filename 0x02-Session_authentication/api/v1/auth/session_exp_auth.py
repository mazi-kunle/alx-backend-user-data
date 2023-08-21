#!/usr/bin/env python3
'''This is a module
'''

from api.v1.auth.session_auth import SessionAuth
import os
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''session expire auth class
    '''
    def __init__(self):
        '''an init method
        '''
        try:
            duration = int(os.getenv('SESSION_DURATION'))
        except Exception as e:
            duration = 0
        finally:
            self.session_duration = duration

    def create_session(self, user_id: str = None) -> str:
        '''create session
        '''
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        session_dictionary = {}
        session_dictionary['user_id'] = user_id
        session_dictionary['created_at'] = datetime.now()
        self.user_id_by_session_id[session_id] = session_dictionary

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''get user id from session id
        '''
        session_dict = super().user_id_for_session_id(session_id)
        if session_dict is None:
            return None
        if self.session_duration <= 0:
            return session_dict['user_id']
        elif 'created_at' not in session_dict.keys():
            return None
        elif ((session_dict['created_at'] +
                timedelta(seconds=self.session_duration))
                < datetime.now()):
            return None
        else:
            return session_dict['user_id']
