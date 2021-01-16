from datetime import datetime, timedelta
from functools import wraps

import jwt
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import (load_pem_private_key,
                                                          load_pem_public_key)
from database.db import User
from flask import jsonify, request


def generate_token(identity, seconds):
    token = jwt.encode(
        {
            "sub": identity,
            "iat": datetime.utcnow(),
            "exp": datetime.utcnow() + timedelta(seconds=seconds),
        },
        _import_RS256_privatekey(),
        algorithm="RS256",
    )
    return token


def decode_token(jwt_token):
    invalid_msg = {"message": "Invalid token.", "authenticated": False}
    expired_msg = {"message": "Expired token.", "authenticated": False}
    try:
        data = jwt.decode(
            jwt_token, _import_RS256_publickey(), algorithms=["RS256"]
        )
        data["authenticated"] = True
        return data
    except jwt.ExpiredSignatureError:
        return jsonify(expired_msg), 401
    except (jwt.InvalidTokenError, Exception) as e:
        print(e)
        return jsonify(invalid_msg), 401


def token_required(f):
    @wraps(f)
    def _verify(*args, **kwargs):
        auth_headers = request.headers.get("Authorization", "").split(
            "Bearer "
        )

        invalid_msg = {"message": "Invalid token.", "authenticated": False}
        expired_msg = {"message": "Expired token.", "authenticated": False}

        if len(auth_headers) != 1:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[0]
            data = jwt.decode(
                token, _import_RS256_publickey(), algorithms=["RS256"]
            )
            user = User.query.filter_by(email=data["sub"]).first()
            if not user:
                raise RuntimeError("Token verification failed.")
            return f(user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            return jsonify(expired_msg), 401
        except (jwt.InvalidTokenError, Exception) as e:
            print(e)
            return jsonify(invalid_msg), 401

    return _verify


def _import_RS256_publickey(key_path="backend/encrytpion/jwtRS256.key.pub"):
    with open(key_path, "rb") as pem:
        pemlines = pem.read()
    public_key = load_pem_public_key(pemlines, backend=default_backend())
    return public_key


def _import_RS256_privatekey(key_path="backend/encryption/jwtRS256.key"):
    with open(key_path, "rb") as pem:
        pemlines = pem.read()
    private_key = load_pem_private_key(
        pemlines, password=None, backend=default_backend()
    )
    return private_key
