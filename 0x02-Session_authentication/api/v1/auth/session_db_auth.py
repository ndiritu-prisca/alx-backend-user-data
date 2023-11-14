#!/usr/bin/env python3
"""SessionDBAuth module"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """Class that inherits from SessionExpAuth"""
    def __init__(self):
        """Initializing SessionDBAuth"""
        super().__init__()

    def create_session(self, user_id=None) -> str:
        """Method that creates and stores new instance of UserSession and
           returns the Session ID"""
        if user_id:
            session_id = super().create_session(user_id)
            if not session_id:
                return None
            new_session = UserSession(user_id=user_id, session_id=session_id)
            new_session.save()
            UserSession.save_to_file()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """Method that returns the User ID by requesting UserSession in the
           database based on session_id"""
        if not session_id:
            return None
        try:
            UserSession.load_from_file()
            user_sessions = UserSession.search({session_id: session_id})
            for session in user_sessions:
                created_at = session.get('created_at', None)
                if not created_at:
                    return None
                if (datetime.now() > created_at +
                        timedelta(seconds=self.session_duration)):
                    return
                return session.get('user_id', None)
        except Exception:
            return

    def destroy_session(self, request=None):
        """Method that destroys the UserSession based on the Session ID from
           the request cookie"""
        if request:
            session_value = self.session_cookie(request)
            if session_value:
                if super().destroy_session(request):
                    try:
                        sessions = UserSession.search({session_id: session_id})
                        for session in sessions:
                            session.remove()
                            return True
                    except Exception:
                        return False
        return False
