#!/usr/bin/env python3
"""Flask app module"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
