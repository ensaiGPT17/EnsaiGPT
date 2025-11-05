from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from dao.user_dao import UserDAO
from service.user_service import UserService
from view.userviews.main_menu_view import MainMenuView

class ChangeCredentialsView(AbstractView):
    def __init__(self, message: str = ""):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        user_dao = UserDAO()
        user_service = UserService(user_dao)

        print("\n" + "-" * 50 + "\nModifier mes identifiants\n" + "-" * 50 + "\n")
        choix = inquirer.select(
            message=f"Que voulez-vous faire {username} ?",
            choices=[
                "Changer nom d'utilisateur",
                "Changer mon mot de passe",
                "Retour"               
            ],
        ).execute()

        if choix == "Changer nom d'utilisateur":
            # demander mdp
            password = inquirer.secret(message="Rentrer votre mot de passe :").execute()
            res = user_service.authenticate(username, password)

            if res.code == 200:
                # user confirmé, il peut changer le USERNAME
                new_username = inquirer.text(message="Rentrez votre nouveau nom d'utilisateur:").execute()
                res_chgt_username = user_service.change_username(user.id_user, new_username)
                # si reussite changement username 
                if res_chgt_username.code == 200:
                    message = f"{res_chgt_username.content}\n" 
                    return MainMenuView(message)                   
                # si echec changement username
                elif res_chgt_username == 409:
                    message = f"{res_chgt_username.content}"
                    return MainMenuView(message)
                elif res_chgt_username == 500 : 
                    message=f"Erreur inconnue:{res_chgt_username.content}"
                    return MainMenuView(message)
            else:
                return MainMenuView("Mot de passe erronné! Retour au Menu Principal")

        elif choix == "Changer mon mot de passe":
            # demader mdp
            password = inquirer.secret(message="Rentrer votre mot de passe actuel:").execute()
            res = user_service.authenticate(username, password)
            if res.code == 200:
                # user confirmé, il peut changer le MOT DE PASSE
                new_password = inquirer.secret(message="Rentrez votre nouveau mot de passe: ")
                res_chgt_password = user_service.change_password(user.id_user, password, new_password)
                if res_chgt_password.code==200:
                    message = f"{res_chgt_password.content}\n"
                elif res_chgt_password.code==400:
                    message = f"Echec:{res_chgt_password.content}\n"
                elif res_chgt_password.code==500:
                    message = f"Echec, erreur inconnue:{res_chgt_password.content}\n"
                return MainMenuView(message)
            else:
                return MainMenuView("Mot de passe erronné! Retour au Menu Principal")
        elif choix == "Retour":
            return MainMenuView("Menu Principal")