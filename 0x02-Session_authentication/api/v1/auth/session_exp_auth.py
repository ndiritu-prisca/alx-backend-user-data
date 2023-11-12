#!/usr/bin/env python3
"""SessionExpAuth module"""

from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Class that inherits from SessionAuth"""
    def __init__(self):
        """Initialilzing SessionExpAuth"""
        super().__init__()
        session_duration = getenv('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Overload create session of parent"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None

        session_dict = {
            "user_id": user_id,
            "created_at": datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Overloads parent's method"""
        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id.keys():
            return None
        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_dict.get('user_id')

        created_at = session_dict.get('created_at')
        if not created_at:
            return None

        total_time = created_at + timedelta(seconds=self.session_duration)
        if total_time < datetime.now():
            return None
        return session_dict.get('user_id')
