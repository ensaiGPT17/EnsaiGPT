def hash_password(password, salt=None):  #à faire
    return password


def password_is_secure(password) -> bool:  #à faire
    if len(password) < 5:
        return False
    return True