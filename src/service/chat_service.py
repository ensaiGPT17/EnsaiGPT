from model.chat import Chat
from model.message import Message
from dao.chat_dao import ChatDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional, List
from api.chat_client import EnsaiGPTClient
from service.message_service import MessageService
from dao.message_dao import MessageDAO
from utils.log_decorator import log
import Levenshtein


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
        self.message_service = MessageService(MessageDAO())
        self.client = EnsaiGPTClient()

    @log
    def get_chat(self, id_chat: int) -> Chat:
        """
        Récupère une conversation spécifique.
        """
        return self.chat_dao.get_chat(id_chat)

    @log
    def get_chats_by_id_user(self, id_user: int) -> Optional[List[Chat]]:
        """
        Retourne toutes les conversations d’un utilisateur, triées par dates.
        """
        chats = self.chat_dao.list_chats_id_user(id_user)
        if chats is None:
            return None
        chats.sort(key=lambda m: m.last_date)
        return chats

    @log
    def request_title(self, id_chat: int) -> str:
        history = self.message_service.get_messages_by_chat(id_chat)
        history.append(self.message_service.title_request())
        chat = self.get_chat(id_chat)
        return self.client.generate(chat, history)

    @log
    def create_chat(self, user_first_message_content: str, id_user: int,
                    max_tokens=512, top_p=1.0, temperature=0.7,
                    system_message="Tu es un assistant utile.") -> Chat:
        """
        Crée une nouvelle conversation.
        """
        new_chat = Chat(
            id_chat=-1,
            id_user=id_user,
            title="Nouvelle conversation",
            date_start=datetime.now(),
            last_date=datetime.now(),
            max_tokens=max_tokens,
            top_p=top_p,
            temperature=temperature
        )

        chat_inserted = self.chat_dao.insert(new_chat)

        # Message systeme
        self.message_service.create_message(
            id_chat=chat_inserted.id_chat, 
            date_sending=datetime.now(), 
            role_author="system", 
            content=system_message
        )

        # message user
        self.message_service.create_message(
            id_chat=chat_inserted.id_chat, 
            date_sending=datetime.now(), 
            role_author="user", 
            content=user_first_message_content
        )

        messages = self.message_service.get_messages_by_chat(chat_inserted.id_chat)

        assistant_response = self.client.generate(chat_inserted, messages)

        # reponse assistant
        self.message_service.create_message(
            id_chat=chat_inserted.id_chat, 
            date_sending=datetime.now(), 
            role_author="assistant", 
            content=assistant_response
        )

        # titre
        chat_inserted.title = self.request_title(chat_inserted.id_chat)
        chat_updated = self.chat_dao.update(chat_inserted.id_chat, chat_inserted)

        return chat_updated

    @log
    def send_message(self, chat: Chat, history: List[Message], content: str) -> \
            List[Message]:
        liste = history.copy()
        print(liste)
        user_message_sent = self.message_service.create_message(id_chat=chat.id_chat,
                                            date_sending=datetime.now(),
                                            role_author="user", content=content)[1]
        liste.append(user_message_sent)
        print(liste)
        assistant_response = self.client.generate(chat, history)
        assistant_response_saved = self.message_service.create_message(id_chat=chat.id_chat,
                                            date_sending=datetime.now(),
                                            role_author="assistant",
                                            content=assistant_response)[1]
        # messages_updated = self.message_service.get_messages_by_chat(chat.id_chat)
        return liste.append(assistant_response_saved)

    @log
    def delete_chat(self, id_chat: int) -> ResponseService:
        """Supprime une conversation."""
        deleted = self.chat_dao.delete(id_chat)
        if deleted:
            return ResponseService(*self.CHAT_DELETE_SUCCESS)
        return ResponseService(*self.CHAT_DELETE_ERROR)

    @log
    def search_chat_by_title(self, id_user: int, search: str) -> List[Chat]:
        """
        Recherche des conversations par titre, triées grâce à la distance de
        Levenshtein.
        """
        all_chats = self.chat_dao.list_chats_id_user(id_user)
        if not all_chats:
            return []

        search_words = search.lower().split()
        similarity_threshold = 0.6  # seuil (vérifier s'il n'est pas trop haut)

        scored_results = []

        for chat in all_chats:
            title_words = chat.title.lower().split()

            total_score = 0
            for sw in search_words:  # on compare mot à mot
                best_ratio = max(Levenshtein.ratio(sw, tw) for tw in title_words)
                total_score += best_ratio

            avg_score = total_score/len(search)

            if avg_score >= similarity_threshold or True:
                scored_results.append((avg_score, chat))

        # Trier par similarité décroissante
        scored_results.sort(key=lambda x: x[0], reverse=True)

        return [chat for _, chat in scored_results]

    def search_chat_by_date(self, id_user: int, search_date: str) -> List[Chat]:
        """Recherche les conversations créées à une certaine date."""
        date = datetime.strptime(search_date, "%Y-%m-%d")
        all_chats = self.chat_dao.search_by_date(id_user, date)
        if all_chats is None:
            return []
        all_chats.sort(key=lambda chat: chat.date_start, reverse=True)
        return all_chats

    def update_parameters_chat(self, id_chat: int, context: str, max_tokens: int,
                               top_p: float, temperature: float) -> ResponseService:
        """
        Met à jour les paramètres d’un chat (si ces champs existent dans la BDD).
        Pour le moment, on suppose qu’ils seront stockés ailleurs.
        """
        pass