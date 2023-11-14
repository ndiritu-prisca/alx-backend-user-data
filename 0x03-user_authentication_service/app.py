#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request, abort, redirect
from auth import Auth
from user import User

app = Flask(__name__)
AUTH = Auth()


@app.route('/')
def index() -> str:
    """Returns a str"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user() -> str:
    """End point to register a user"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    try:
        AUTH.register_user(email, pwd)
        return jsonify({"email": f"{email}", "message": "user created"}), 200
    except Exception:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login() -> str:
    """End point for logging in"""
    email = request.form.get('email')
    pwd = request.form.get('password')
    valid_login = AUTH.valid_login(email, pwd)
    if valid_login:
        sess_id = AUTH.create_session(email)
        response = jsonify({"email": f"{email}", "message": "logged in"})
        response.set_cookie('session_id', sess_id)
        return response
    else:
        abort(401)


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """Implementation of logout"""
    sess_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(sess_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'])
def profile() -> str:
    """Method to find user and respond with 200 HTTP Status"""
    sess_id = request.cookies.get("session_id")
    if not sess_id:
        abort(403)

    user = AUTH.get_user_from_session_id(sess_id)
    if not user:
        abort(403)

    return jsonify({"email": f"{user.email}"}), 200


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token() -> str:
    """Route to get reset password token"""
    email = request.form.get('email')
    if not email:
        abort(403)

    r_token = AUTH.get_reset_password_token(email)
    if not r_token:
        abort(403)
    return jsonify({"email": f"{email}", "reset_token": f"{r_token}"}), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
