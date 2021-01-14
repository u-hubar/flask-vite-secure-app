from database.db import User, db_session
from flask import Flask, jsonify, request
from flask_script import Manager
from sqlalchemy.exc import IntegrityError

from backend.encryption.jwt_tokens import decode_token, generate_token
from backend.encryption.password import (encrypt_user_password)

app = Flask(__name__)

manager = Manager(app)


@manager.command
def run():
    app.run()


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/api/register', methods=["POST"])
def register():
    data = request.get_json()
    email = data.get("email")
    password = encrypt_user_password(data.get("password"))

    try:
        new_user = User(email=email, password=password)
        db_session.add(new_user)
        db_session.commit()
    except IntegrityError as e:
        db_session.rollback()
        error = str(e).split('\n')[0]
        return jsonify({
            "status": "error",
            "message": "Could not add user",
            "error": f"{error}"
        }), 400

    return jsonify({
        "status": "success",
        "message": "User added successfully"
    }), 201


@app.route('/api/login', methods=["POST"])
def login():
    data = request.get_json()
    user = User.authenticate(**data)

    if user is None:
        return jsonify({
            "status": "failed",
            "message": "Failed getting user"
        }), 401

    access_token = generate_token(identity=user.email, seconds=15)
    refresh_token = generate_token(identity=user.email, seconds=86400) # 24h

    return jsonify({
        "access": access_token,
        "refresh": refresh_token,
    }), 200


@app.route('/api/token_refresh', methods=["POST"])
def refresh():
    data = request.get_json()
    refresh_token = data.get("refresh", None)

    if refresh_token is None:
        return jsonify({
            "status": "failde",
            "message": "Invalid token."
        }), 401

    data = decode_token(refresh_token)

    if not data.get("authenticated"):
        return data

    email = data.get("email")
    access_token = generate_token(identity=email, seconds=15)

    return jsonify({
        "access": access_token
    })


if __name__ == "__main__":
    manager.run()
