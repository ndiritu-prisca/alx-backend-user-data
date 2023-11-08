#!/usr/bin/env python3
"""Class Basic auth"""


from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Class that inherits fro Auth"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        A method to that returns the base64 part of the auhtorizarion header"""
        if authorization_header is None:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        extracted = authorization_header.split(' ', 1)[1]
        return extracted
