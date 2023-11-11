#!/usr/bin/env python3
"""SessionAuth Module"""

from api.v1.auth.auth import Auth
from uuid import uuid4
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """SessionAuth class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Method  that creates a Session ID for a user_id"""
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Method that returns a User ID based on a Session ID:"""
        if session_id is None or not isinstance(session_id, str):
            return None
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """Method that returns a User instance based on a cookie value"""
        if request:
            cookie_value = self.session_cookie(request)
            if cookie_value:
                user_id = self.user_id_for_session_id(cookie_value)
                return User.get(user_id)

    def destroy_session(self, request=None) -> bool:
        """Method that deletes the user session / logout"""
        if request is None:
            return False
        cookie_value = self.session_cookie(request)
        if not cookie_value:
            return False
        user_id = self.user_id_for_session_id(cookie_value)
        if not user_id:
            return False
        try:
            del self.user_id_by_session_id[cookie_value]
        except Exception:
            pass
        return True
