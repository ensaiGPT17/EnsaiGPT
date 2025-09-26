def hash_password(password, salt=None):
    return password


def password_is_secure(password) -> bool:
    if len(password) < 5:
        return False
    return True
