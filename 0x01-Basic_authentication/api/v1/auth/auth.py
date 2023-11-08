#!/usr/bin/env python3
"""Auth class"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Class module"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Method that checks if a path requires authentication"""
        if path is None or excluded_paths is None:
            return True
        if path[-1] != '/':
            path = path + '/'
        else:
            path = path
        has_wildcard = any(e_p.endswith("*") for e_p in excluded_paths)
        if not has_wildcard:
            return path not in excluded_paths
        for e in excluded_paths:
            if e.endswith("*"):
                if path.startswith(e[:-1]):
                    return False
            if path == e:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """Method that authorizes header"""
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Method that gets current user"""
        return None
