from view.abstract_view import AbstractView
from InquirerPy import inquirer
from view.session import Session
from dao.user_dao import UserDAO
from service.user_service import UserService


class ChangeCredentialsView(AbstractView):
    def __init__(self, message: str = "Modifier mes identifiants"):
        super().__init__(message)

    def choisir_menu(self):
        user = Session().user
        username = user.username
        user_dao = UserDAO()
        user_service = UserService(user_dao)

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
                if res_chgt_username.code == 200:
                    # test ok 
                    from view.home.home_view import HomeView
                    message = f"{res_chgt_username.content}\n" 
                    return HomeView(message)                 
                # si echec changement username
                elif res_chgt_username.code == 409:
                    # test ok
                    from view.userviews.main_menu_view import MainMenuView
                    message = f"{res_chgt_username.content}"
                    return MainMenuView(message)
                else : 
                    #non testé
                    from view.userviews.main_menu_view import MainMenuView
                    message=f"Erreur inconnue:{res_chgt_username.content}"
                    return MainMenuView(message)
            else:
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView("Mot de passe erronné! Retour au Menu Principal")

        elif choix == "Changer mon mot de passe":
            # demander mdp
            password = inquirer.secret(message="Rentrer votre mot de passe actuel:").execute()
            res = user_service.authenticate(username, password)
            if res.code == 200:
                # user confirmé, il peut changer le MOT DE PASSE
                new_password = inquirer.secret(message="Rentrez votre nouveau mot de passe: ").execute()
                res_chgt_password = user_service.change_password(user.id_user, password, new_password)
                if res_chgt_password.code==200:
                    # reussite chgt mdp test OK
                    from view.userviews.main_menu_view import MainMenuView
                    message = f"{res_chgt_password.content}\n"
                    return MainMenuView(message)
                elif res_chgt_password.code==400:
                    # mdp trop faible test OK
                    from view.userviews.main_menu_view import MainMenuView
                    message = f"Echec:{res_chgt_password.content}\n"
                    return MainMenuView(message)
                elif res_chgt_password.code==500:
                    from view.userviews.main_menu_view import MainMenuView
                    message = f"Echec, erreur inconnue:{res_chgt_password.content}\n"
                    return MainMenuView(message)
            else:
                from view.userviews.main_menu_view import MainMenuView
                return MainMenuView("Mot de passe erronné! Retour au Menu Principal")
        elif choix == "Retour":
            from view.userviews.main_menu_view import MainMenuView
            return MainMenuView("Menu Principal")