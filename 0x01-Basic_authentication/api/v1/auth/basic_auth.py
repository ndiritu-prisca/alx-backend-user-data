#!/usr/bin/env python3
"""Class Basic auth"""


from api.v1.auth.auth import Auth
from base64 import b64decode


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """Method that returns the decoded value of a base64 string"""
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            b64_bytes = base64_authorization_header.encode('utf-8')
            res = b64decode(b64_bytes)
            decoded = res.decode('utf-8')
            return decoded
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """Method that returns the user email and password from base64decoded
           value"""
        if decoded_base64_authorization_header is None:
            return (None, None)
        if not isinstance(decoded_base64_authorization_header, str):
            return (None, None)
        if ":" not in decoded_base64_authorization_header:
            return (None, None)
        res = decoded_base64_authorization_header.split(':', 1)
        return res[0], res[1]
