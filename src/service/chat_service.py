from model.chat import Chat
from dao.chat_dao import ChatDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional, List


class ChatService:
    def __init__(self, chat_dao: ChatDAO = ChatDAO()):
        self.chat_dao = chat_dao

    def get_chat(self, id_chat: int) -> Optional[Chat]:
        """Récupère une conversation spécifique."""
        chat = self.chat_dao.get_chat(id_chat)
        if chat:
            return ResponseService(success=True, data=chat)
        return ResponseService(success=False, message="Chat introuvable.")

    def get_chats_by_id_user(self, id_user: int) -> ResponseService:
        """Retourne toutes les conversations d’un utilisateur."""
        chats = self.chat_dao.list_chats_id_user(id_user)
        if not chats:
            return ResponseService(success=False, message="Aucune conversation trouvée.")
        return ResponseService(success=True, data=chats)

    def create_chat(self, id_user: int, max_tokens: int, top_p: float,
                    temperature: float) -> ResponseService:
        """
        Crée une nouvelle conversation.
        Les paramètres (max_tokens, top_p, temperature) peuvent être stockés plus tard dans un champ JSON ou une autre table.
        """
        chat = Chat(
            id_chat=None,
            id_user=id_user,
            title="Nouvelle conversation",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )

        inserted_chat = self.chat_dao.insert(chat)
        if inserted_chat:
            return ResponseService(success=True, data=inserted_chat,
                                   message="Conversation créée avec succès.")
        return ResponseService(success=False, message="Erreur lors de la création du chat.")

    def request_title(self, id_chat: int) -> ResponseService:
        # je n'ai aucune idée :)
        pass

    def update_parameters_chat(self, id_chat: int, context: str, max_tokens: int,
                               top_p: float, temperature: float) -> ResponseService:
        """
        Met à jour les paramètres d’un chat (si ces champs existent dans la BDD).
        Pour le moment, on suppose qu’ils seront stockés ailleurs.
        """
        chat = self.chat_dao.get_chat(id_chat)
        if not chat:
            return ResponseService(success=False, message="Chat introuvable.")

        # TODO: si tu ajoutes ces colonnes (context, max_tokens, etc.), tu les modifies ici.
        return ResponseService(success=True, message="Paramètres mis à jour (simulation).")

    def update_chat(self, id_chat: int, updated_chat: Chat) -> ResponseService:
        """Met à jour le titre ou d’autres infos d’un chat."""
        updated = self.chat_dao.update(id_chat, updated_chat)
        if updated:
            return ResponseService(success=True, message="Chat mis à jour.", data=updated)
        return ResponseService(success=False, message="Échec de la mise à jour du chat.")

    def delete_chat(self, id_chat: int) -> ResponseService:
        """Supprime une conversation."""
        deleted = self.chat_dao.delete(id_chat)
        if deleted:
            return ResponseService(success=True, message="Chat supprimé avec succès.")
        return ResponseService(success=False, message="Chat introuvable ou non supprimé.")

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
