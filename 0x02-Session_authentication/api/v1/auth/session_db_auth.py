#!/usr/bin/env python3
"""SessionDBAuth module"""

from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Class that inherits from SessionExpAuth"""
    def create_session(self, user_id=None) -> str:
        """Method that creates and stores new instance of UserSession and
           returns the Session ID"""
        

