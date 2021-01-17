from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64


def encrypt_user_password(
    password, t=16, m=2 ** 15, p=2, hash_len=32, salt_len=16
):
    argon2Hasher = PasswordHasher(
        time_cost=t,
        memory_cost=m,
        parallelism=p,
        hash_len=hash_len,
        salt_len=salt_len,
    )
    hash = argon2Hasher.hash(password)
    return hash


def verify_user_password(
    hash, password, t=16, m=2 ** 15, p=2, hash_len=32, salt_len=16
):
    argon2Hasher = PasswordHasher(
        time_cost=t,
        memory_cost=m,
        parallelism=p,
        hash_len=hash_len,
        salt_len=salt_len,
    )
    try:
        is_valid = argon2Hasher.verify(hash, password)
    except Exception as err:
        print(err)
        return False
    else:
        return is_valid


def encrypt_service_password(key, secret, aad):
    key = string_padding(key, 32)

    key = key.encode()
    secret = secret.encode()
    aad = aad.encode()

    aesgcm = AESGCM(key)
    nonce = os.urandom(96)
    ct = aesgcm.encrypt(nonce, secret, aad)
    return base64.b64encode(nonce + ct)


def decrypt_service_password(key, encrypted, aad):
    enc = base64.b64decode(encrypted)
    key = string_padding(key, 32)

    key = key.encode()
    aad = aad.encode()

    aesgcm = AESGCM(key)
    nonce = enc[:96]
    secret = enc[96:]
    pt = aesgcm.decrypt(nonce, secret, aad)
    return pt.decode()


def string_padding(string, length):
    padding_len = length - len(string) % length
    string = string + chr(padding_len) * padding_len
    return string


def string_unpadding(string):
    string = string[: -ord(string[-1])]
    return string
