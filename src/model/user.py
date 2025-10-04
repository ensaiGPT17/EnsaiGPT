class User:
    def __init__(self, id_user : int, username: str, hashed_password: str):
        self.id_user = id_user
        self.username = username
        self.hashed_password = hashed_password
