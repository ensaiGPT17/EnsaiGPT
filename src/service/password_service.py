import bcrypt
import re

def hash_password(password: str, salt: bytes = None) -> str:
    """
    Hash un mot de passe en utilisant bcrypt.
    :param password: Mot de passe en clair
    :param salt: Sel optionnel, sinon généré automatiquement
    :return: Hash du mot de passe en str
    """
    if not salt:
        salt = bcrypt.gensalt()  # génère un sel aléatoire

    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')  # convertir en str pour stocker

import bcrypt

def check_password(entered_password: str, stored_hash: str) -> bool:
    """
    Vérifie si le mot de passe entré correspond au hash stocké.
    :param entered_password: mot de passe fourni par l'utilisateur
    :param stored_hash: mot de passe hashé depuis la base de données
    :return: True si correspondance, False sinon
    """
    return bcrypt.checkpw(entered_password.encode('utf-8'), stored_hash.encode('utf-8'))


def password_is_secure(password: str) -> bool:
    """
    Vérifie si le mot de passe est sécurisé selon des critères de robustesse.
    :param password: Mot de passe en clair
    :return: True si sécurisé, False sinon
    """
    if len(password) < 8:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True


if __name__ == "__main__":
    pwd = "mot_de_passe_Br#@1"
    if password_is_secure(pwd):
        hashed = hash_password(pwd)
        print("Mot de passe sécurisé et hashé :", hashed)
    else:
        print("Mot de passe trop faible")

    # checker si le mot de passe est dejà la, je vais l'utiliser
    # lors de la connexion

    if check_password(pwd, hashed):
        print("Connexion réussie !")
