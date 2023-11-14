#!/usr/bin/env python3
"""Main module for end-to-end integration test"""

import requests

URL = 'http://localhost:5000'


def register_user(email: str, password: str) -> None:
    """Integration test for register user method"""
    credentials = {"email": email, "password": password}
    response = requests.post(f'{URL}/users', data=credentials)
    assert response.status_code == 200

    msg = {"email": email, "message": "user created"}
    assert response.json() == msg


def log_in_wrong_password(email: str, password: str) -> None:
    """Integration test for login with wrong password"""
    credentials = {"email": email, "password": password}
    response = requests.post(f'{URL}/sessions', data=credentials)

    assert response.status_code == 401


def log_in(email: str, password: str) -> str:
    """Integration test for a successful login """
    credentials = {"email": email, "password": password}
    response = requests.post(f'{URL}/sessions', data=credentials)
    assert response.status_code == 200

    msg = {"email": email, "message": "logged in"}
    assert response.json() == msg

    sess_id = response.cookies.get("session_id")

    return sess_id


def profile_unlogged() -> None:
    """Integration test for validation of profile with no login"""
    cookies = {"session_id": ""}
    response = requests.get(f'{URL}/profile', cookies=cookies)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """Integration test for validation of profile with login"""
    cookies = {"session_id": session_id}
    response = requests.get(f'{URL}/profile', cookies=cookies)
    assert response.status_code == 200

    msg = {"email": EMAIL}
    assert response.json() == msg


def log_out(session_id: str) -> None:
    """Integration test for logging out"""
    cookies = {"session_id": session_id}
    response = requests.delete(f'{URL}/sessions', cookies=cookies)
    assert response.status_code == 200

    msg = {"message": "Bienvenue"}
    assert response.json() == msg


def reset_password_token(email: str) -> str:
    """Integration test for password reset token"""
    data = {"email": email}
    response = requests.post(f'{URL}/reset_password', data=data)

    assert response.status_code == 200

    reset_token = response.json().get("reset_token")

    msg = {"email": email, "reset_token": reset_token}
    assert response.json() == msg

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Integration test for updating password"""
    credentials = {
        "email": email,
        "reset_token": reset_token,
        "new_password": new_password
    }
    response = requests.put(f'{URL}/reset_password', data=credentials)
    assert response.status_code == 200

    msg = {"email": email, "message": "Password updated"}
    assert response.json() == msg


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
