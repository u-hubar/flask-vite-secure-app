import base64
import os
import re

from argon2 import PasswordHasher
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_user_password(
    password, t=16, m=2 ** 17, p=4, hash_len=32, salt_len=16
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
    hash, password, t=16, m=2 ** 17, p=4, hash_len=32, salt_len=16
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
    kek = decode_argon2id_base64(key)
    secret = secret.encode()
    aad = aad.encode()

    aesgcm = AESGCM(kek)
    nonce = os.urandom(96)
    ct = aesgcm.encrypt(nonce, secret, aad)
    return base64.b64encode(nonce + ct)


def decrypt_service_password(key, encrypted, aad):
    enc = base64.b64decode(encrypted)

    kek = decode_argon2id_base64(key)
    aad = aad.encode()

    aesgcm = AESGCM(kek)
    nonce = enc[:96]
    secret = enc[96:]
    pt = aesgcm.decrypt(nonce, secret, aad)
    return pt.decode()


def decode_argon2id_base64(hash, altchars=b"+/"):
    hash = ("$" + hash.split("$")[-1]).encode()
    hash = re.sub(rb"[^a-zA-Z0-9%s]+" % altchars, b"", hash)
    missing_padding = len(hash) % 4
    if missing_padding:
        hash += b"=" * (4 - missing_padding)
    return base64.b64decode(hash, altchars)
