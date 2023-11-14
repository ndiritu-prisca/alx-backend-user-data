#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request, abort
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")