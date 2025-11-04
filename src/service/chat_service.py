from model.chat import Chat
from dao.chat_dao import ChatDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional, List
from utils.log_decorator import log

class ChatService:

    # CHAT_NOT_FOUND = (404, "Conversation non trouvée!")
    CHAT_GET_ERROR = (500, "Erreur interne lors de la recupération de la conversation ")
    CHAT_GET_SUCCESS = (200, "Récupération de conversation réussie")
    CHATS_GET_BY_ID_SUCCES = (200, "Récupération réussie")
    CHATS_GET_BY_ID_ERROR = (500, "Erreur interne lors de la recupération des conversations")
    CHAT_CREATE_SUCCESS = (200, "creation de la conversation reussie")
    CHAT_CREATE_ERROR = (500, "echec de la creation de la conversation")
    CHAT_DELETE_ERROR = (500, "echec suppression conversation")
    CHAT_DELETE_SUCCESS = (200, "supression conversation reussie")

    def __init__(self, chat_dao: ChatDAO = ChatDAO()):
        self.chat_dao = chat_dao

    @log
    def get_chat(self, id_chat: int) -> Optional[Chat]:
        """Récupère une conversation spécifique.
        Code de  sortie:
        - 500 : Erreur inconnue
        - 200 : succes
        """
        chat = self.chat_dao.get_chat(id_chat)
        if chat:
            return ResponseService(*self.CHAT_GET_SUCCESS)
        return ResponseService(*self.CHAT_GET_ERROR)

    @log
    def get_chats_by_id_user(self, id_user: int) -> ResponseService:
        """Retourne toutes les conversations d’un utilisateur.
        code de sortie:
        - 200: succes
        - 500: Echec
        """
        chats = self.chat_dao.list_chats_id_user(id_user)
        if chats:
            return ResponseService(*self.CHATS_GET_BY_ID_SUCCES)
        return ResponseService(*self.CHATS_GET_BY_ID_ERROR)

    @log
    def request_title(self, id_chat: int) -> ResponseService:
        pass

    @log
    def create_chat(self, id_user: int, title, date_start, last_date, max_tokens: int, top_p: float,
                    temperature: float) -> ResponseService:
        """
        Crée une nouvelle conversation.
        """
        chat = Chat(
            id_chat=None,
            id_user=id_user,
            title="Nouvelle conversation",
            date_start=datetime.now(),
            last_date=datetime.now(),
            max_tokens=max_tokens,
            top_p = top_p,
            temperature = temperature
        )

        inserted_chat = self.chat_dao.insert(chat)
        if inserted_chat:
            return ResponseService(*self.CHAT_CREATE_SUCCESS)
        return ResponseService(*self.CHAT_CREATE_ERROR)

    @log
    def delete_chat(self, id_chat: int) -> ResponseService:
        """Supprime une conversation."""
        deleted = self.chat_dao.delete(id_chat)
        if deleted:
            return ResponseService(*self.CHAT_DELETE_SUCCESS)
        return ResponseService(*self.CHAT_DELETE_ERROR)

    def search_chat_by_tile(self, search: str) -> ResponseService:
        """Recherche les conversations contenant un mot-clé dans le titre."""
        all_chats = self.chat_dao.get_all()
        if not all_chats:
            return ResponseService(success=False, message="Aucun chat disponible.")

        results = [chat for chat in all_chats if search.lower() in chat.title.lower()]
        if not results:
            return ResponseService(success=False, message="Aucun chat correspondant trouvé.")
        return ResponseService(success=True, data=results)

    def search_chat_by_date(self, search: datetime) -> ResponseService:
        """Recherche les conversations créées à une certaine date."""
        all_chats = self.chat_dao.get_all()
        if not all_chats:
            return ResponseService(success=False, message="Aucun chat disponible.")

        results = [chat for chat in all_chats if chat.created_at.date() == search.date()]
        if not results:
            return ResponseService(success=False, message="Aucun chat à cette date.")
        return ResponseService(success=True, data=results)


    def update_parameters_chat(self, id_chat: int, context: str, max_tokens: int,
                               top_p: float, temperature: float) -> ResponseService:
        """
        Met à jour les paramètres d’un chat (si ces champs existent dans la BDD).
        Pour le moment, on suppose qu’ils seront stockés ailleurs.
        """
        pass

    def update_chat(self, id_chat: int, updated_chat: Chat) -> ResponseService:
        """Met à jour le titre ou d’autres infos d’un chat."""
        pass