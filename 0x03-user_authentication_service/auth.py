#!/usr/bin/env python3
"""Auth module"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """Method that takes in a password string arguments and returns bytes."""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """Method that returns a string representation of a new UUID"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initializing class Auth"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Method that takes in mandatory email and password string arguments
        and returns a User object."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            user = self._db.add_user(email, hashed_pwd)
            return user
        else:
            raise ValueError(f"User {email} already exists")

    def valid_login(self, email: str, password: str) -> bool:
        """Method that locates the user by email and checks if the password
        matches"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Method that takes in an email as argument and returns
        the session ID as a string"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> str:
        """Method that takes a single session_id string argument and returns
        the corresponding User or None"""
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """Method that takes a single user_id integer argument and returns
        None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            pass
        self._db.update_user(user.id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Method that takes an email string argument and returns a string"""
        try:
            user = self._db.find_user_by(email=email)
            r_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=r_token)
            return r_token
        except NoResultFound:
            raise ValueError

    def update_password(self, reset_token: str, password: str) -> None:
        """Method  to update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_pwd = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_pwd,
                             reset_token=None)
