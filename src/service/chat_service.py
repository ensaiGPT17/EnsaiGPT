from model.chat import Chat
from dao.chat_dao import ChatDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional, List
from api.chat_client import EnsaiGPTClient
from service.message_service import MessageService
from dao.message_dao import MessageDAO
from utils.log_decorator import log

class ChatService:
    CHAT_GET_ERROR = (500, "Erreur interne lors de la recupération de la conversation ")
    CHAT_GET_SUCCESS = (200, "Récupération de conversation réussie")
    CHATS_GET_BY_ID_SUCCES = (200, "Récupération réussie")
    CHATS_GET_BY_ID_ERROR = (500, "Erreur interne lors de la recupération des conversations")
    CHAT_CREATE_SUCCESS = (200, "creation de la conversation reussie")
    CHAT_CREATE_ERROR = (500, "echec de la creation de la conversation")
    CHAT_DELETE_ERROR = (500, "echec suppression conversation")
    CHAT_DELETE_SUCCESS = (200, "supression conversation reussie")
    CHAT_TITLE_FOUND = (200, "conversation par recherche titre trouvée")
    CHAT_TITLE_ERROR = (500, "conversation par recherche titre non trouvée")
    CHAT_DATE_FOUND = (200, "conversation par date trouvée")
    CHAT_DATE_ERROR = (500, "conversation par date non trouvée")

    def __init__(self, chat_dao: ChatDAO = ChatDAO()):
        self.chat_dao = chat_dao
        self.history = [
            {"role": "system", "content": "Tu es un assistant utile."}
        ]

    @log
    def get_chat(self, id_chat: int) -> ResponseService:
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
    def create_chat(self, user_first_message, id_user: int, max_tokens = 150, top_p=1.0,
                    temperature=0.7) -> ResponseService:
        """
        Crée une nouvelle conversation.
        """
        new_chat = Chat(
            id_chat= -1,
            id_user=id_user,
            title="Nouvelle conversation",
            date_start=datetime.now(),
            last_date=datetime.now(),
            max_tokens=max_tokens,
            top_p = top_p,
            temperature = temperature
        )



        chat_inserted = self.chat_dao.insert(new_chat)

        # Message 0: Pour le SYSTEME
        message_service = MessageService(MessageDAO())
        message_service.create_message(
            id_chat=chat_inserted.id_chat, 
            date_sending=datetime.now(), 
            role_author="system", 
            content= self.history[0]['content']
        )

        self.history.append(
            {'role': "user", "content": user_first_message}
        )
        
        # Message 1: Pour le USER
        message_service = MessageService(MessageDAO())
        message_service.create_message(
            id_chat=chat_inserted.id_chat, 
            date_sending=datetime.now(), 
            role_author="user", 
            content=user_first_message
        )
        
        payload = {
            "history": self.history,
            "temperature": new_chat.temperature,
            "top_p": new_chat.top_p,
            "max_tokens": new_chat.max_tokens
        }

        client_ensaiGPT = EnsaiGPTClient(payload=payload)
        assistant_response = client_ensaiGPT.generate()

        # Emplier la reponse de l'assistant puis le stocker
        self.history.append(assistant_response)
        message_service = MessageService(MessageDAO())
        message_service.create_message(
            id_chat=chat_inserted.id_chat, 
            date_sending=datetime.now(), 
            role_author="assistant", 
            content=assistant_response
        )
        



    @log
    def delete_chat(self, id_chat: int) -> ResponseService:
        """Supprime une conversation."""
        deleted = self.chat_dao.delete(id_chat)
        if deleted:
            return ResponseService(*self.CHAT_DELETE_SUCCESS)
        return ResponseService(*self.CHAT_DELETE_ERROR)

    @log
    def search_chat_by_title(self, search: str) -> ResponseService:
        """Recherche les conversations contenant un mot-clé dans le titre."""
        # faire plutot methode search by title dans chat dao ? 
        all_chats = self.chat_dao.get_all()
        if not all_chats:
            return ResponseService(success=False, message="Aucun chat disponible.")

        results = [chat for chat in all_chats if search.lower() in chat.title.lower()]
        if not results:
            return ResponseService(*self.CHAT_TITLE_ERROR)
        return ResponseService(*self.CHAT_TITLE_FOUND)





    

    def search_chat_by_date(self, search: datetime) -> ResponseService:
        """Recherche les conversations créées à une certaine date."""
        all_chats = self.chat_dao.get_all()
        if not all_chats:
            return ResponseService(success=False, message="Aucun chat disponible.")

        results = [chat for chat in all_chats if chat.created_at.date() == search.date()]
        if not results:
            return ResponseService(*self.CHAT_DATE_ERROR)
        return ResponseService(*self.CHAT_DATE_FOUND)


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