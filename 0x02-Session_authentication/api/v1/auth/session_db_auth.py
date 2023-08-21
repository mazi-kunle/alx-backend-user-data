#!/usr/bin/env python3
'''This is a module
'''

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    '''session auth class
    '''
    def create_session(self, user_id: str = None) -> str:
        '''create session'''
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        kwargs = {'user_id': user_id, 'session_id': session_id}
        user_session = UserSession(**kwargs)
        user_session.save()

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        '''get user_id from session_id
           from the database
        '''
        UserSession.load_from_file()
        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return None

        user_session = user_session[0]

        expired_time = user_session.created_at + \
            timedelta(seconds=self.session_duration)

        if expired_time < datetime.utcnow():
            return None

        return user_session.user_id

    def destroy_session(self, request=None):
        '''destroys the UserSession based on the Session ID
           from the request cookie
        '''
        if (request is None):
            return False

        session_id = self.session_cookie(request)
        if session_id is None:
            return False

        user_session = UserSession.search({'session_id': session_id})
        if len(user_session) == 0:
            return False

        user_session = user_session[0]
        try:
            user_session.remove()
        except Exception:
            return False
        return True
