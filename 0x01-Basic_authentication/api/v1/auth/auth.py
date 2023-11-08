#!/usr/bin/env python3
"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Class module"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method that requires authentication"""
        return False

    def authorization_header(self, request=None) -> str:
        """Method that authorizes header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Method that gets current user"""
        return None
