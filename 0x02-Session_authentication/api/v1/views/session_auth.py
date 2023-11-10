#!/usr/bin/env python3
"""Views for session authentication"""

from api.v1.views import app_views
from models.user import User
from os import getenv
from flask import abort, jsonify, request


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """A login route for session authentication"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    if email is None or email is "":
        return jsonify(error="email missing"), 400
    if pwd is None or pwd is "":
        return jsonify(error="password missing"), 400
    try:
        users = User.search({"email": email})
    except Exception:
        return jsonify(error="no user found for this email"), 404
    if not users:
        return jsonify(error="no user found for this email"), 404
    for user in users:
        if user.is_valid_password(pwd):
            user_id = user.id
            from api.v1.app import auth
            session_id = auth.create_session(user_id)
            response = jsonify(user.to_json())
            response.set_cookie(getenv('SESSION_NAME'), session_id)
            return response
        else:
            return jsonify(error="wrong password"), 401
    return jsonify(error="no user found for this email"), 404
