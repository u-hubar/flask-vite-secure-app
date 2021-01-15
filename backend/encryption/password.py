from argon2 import PasswordHasher


def encrypt_user_password(password, t=16, m=2**15, p=2, hash_len=32, salt_len=16):
    argon2Hasher = PasswordHasher(time_cost=t, memory_cost=m,
                                  parallelism=p, hash_len=hash_len,
                                  salt_len=salt_len)
    hash = argon2Hasher.hash(password)
    return hash


def verify_user_password(hash, password, t=16, m=2**15, p=2, hash_len=32, salt_len=16):
    argon2Hasher = PasswordHasher(time_cost=t, memory_cost=m,
                                  parallelism=p, hash_len=hash_len,
                                  salt_len=salt_len)
    try:
        is_valid = argon2Hasher.verify(hash, password)
    except Exception as err:
        print(err)
        return False
    else:
        return is_valid
