from argon2 import PasswordHasher


def encrypt_user_password(password):
    argon2Hasher = PasswordHasher(time_cost=16, memory_cost=2**15,
                                  parallelism=2, hash_len=32,
                                  salt_len=16)
    hash = argon2Hasher.hash(password)
    return hash


def verify_user_password(hash, password):
    argon2Hasher = PasswordHasher(time_cost=16, memory_cost=2**15,
                                  parallelism=2, hash_len=32,
                                  salt_len=16)
    try:
        is_valid = argon2Hasher.verify(hash, password)
    except Exception as err:
        print(err)
        return False
    else:
        return is_valid
