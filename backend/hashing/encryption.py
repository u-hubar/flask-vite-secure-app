from hashlib import sha256


def encrypt_user_password(password):
    hash = sha256(password.encode("utf-8")).hexdigest()
    return hash
