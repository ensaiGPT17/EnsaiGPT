from model.chat import Chat
from model.message import Message
from model.user import User
from dao.chat_dao import ChatDAO
from service.response_service import ResponseService
from datetime import datetime
from typing import Optional, List
from api.chat_client import EnsaiGPTClient
from service.message_service import MessageService
from dao.message_dao import MessageDAO
from utils.log_decorator import log
import Levenshtein
import os
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from model.user import User


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
    CHATS_CLEARED_ERROR = (500, "echec de la suppression de liste de conversations")
    CHATS_CLEARED_SUCCES = (200, "Suppression de liste de conversations réussie")

    def __init__(self, chat_dao: ChatDAO = ChatDAO()):
        """
        Constructeur du service ChatService.

        Paramètres
        ----------
        chat_dao : ChatDAO, optionnel
            DAO permettant l'accès aux données des conversations.
            Par défaut : une instance standard de ChatDAO.
        """
        self.chat_dao = chat_dao
        self.message_service = MessageService(MessageDAO())
        self.client = EnsaiGPTClient()

    @log
    def get_chat(self, id_chat: int) -> Chat:
        """
        Récupère une conversation spécifique par son identifiant.

        Paramètres
        ----------
        id_chat : int
            Identifiant de la conversation.

        Retour
        ------
        Chat
            La conversation correspondante.
        """
        return self.chat_dao.get_chat(id_chat)

    @log
    def get_chats_by_id_user(self, id_user: int) -> Optional[List[Chat]]:
        """
        Récupère toutes les conversations d’un utilisateur.

        Paramètres
        ----------
        id_user : int
            Identifiant de l'utilisateur.

        Retour
        ------
        Optional[List[Chat]]
            Liste triée des conversations (ordre : last_date décroissant),
            ou None si aucune conversation n’est trouvée.
        """
        chats = self.chat_dao.list_chats_id_user(id_user)
        if chats is None:
            return None
        chats.sort(key=lambda m: m.last_date, reverse=True)
        return chats

    @log
    def request_title(self, id_chat: int) -> str:
        """
        Demande automatiquement un titre court pour une conversation,
        en ajoutant un message interne puis en interrogeant l’API.

        Paramètres
        ----------
        id_chat : int
            Identifiant de la conversation.

        Retour
        ------
        str
            Titre généré automatiquement.
        """
        history = self.message_service.get_messages_by_chat(id_chat)
        history.append(self.message_service.title_request())
        chat = self.get_chat(id_chat)
        title = self.client.generate(chat, history).strip()
        # Supprime les guillemets simples et doubles en début/fin
        title = title.strip(' "\'')
        return title

    @log
    def create_chat(self, user_first_message_content: str, id_user: int,
                    max_tokens=512, top_p=1.0, temperature=0.7,
                    system_message="Tu es un assistant utile.") -> Chat:
        """
        Crée une nouvelle conversation et génère automatiquement la première réponse de l'assistant.

        Étapes :
        - Création du chat
        - Ajout d’un message système
        - Ajout du premier message utilisateur
        - Génération de la réponse assistant
        - Génération automatique du titre

        Paramètres
        ----------
        user_first_message_content : str
            Contenu du premier message envoyé par l’utilisateur.
        id_user : int
            Identifiant de l’utilisateur.
        max_tokens, top_p, temperature : paramètres du modèle.
        system_message : str
            Message système envoyé en premier.

        Retour
        ------
        Chat
            La conversation nouvellement créée et mise à jour.
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
        """
        Envoie un message dans un chat, puis génère la réponse de l'assistant.

        Paramètres
        ----------
        chat : Chat
            Conversation en cours.
        history : List[Message]
            Historique actuel des messages.
        content : str
            Contenu du message envoyé par l’utilisateur.

        Retour
        ------
        List[Message]
            Historique mis à jour (message utilisateur + réponse assistant).
        """

        user_message_sent = self.message_service.create_message(id_chat=chat.id_chat,
                                            date_sending=datetime.now(),
                                            role_author="user", content=content)[1]
        history.append(user_message_sent)
        assistant_response = self.client.generate(chat, history)
        assistant_response_saved = self.message_service.create_message(id_chat=chat.id_chat,
                                            date_sending=datetime.now(),
                                            role_author="assistant",
                                            content=assistant_response)[1]
        chat.last_date = datetime.now()
        self.chat_dao.update(chat.id_chat, chat)
        history.append(assistant_response_saved)
        return history

    @log
    def delete_chat(self, id_chat: int) -> ResponseService:
        """
        Supprime une conversation.

        Paramètres
        ----------
        id_chat : int
            Identifiant du chat à supprimer.

        Retour
        ------
        ResponseService
            Résultat de l'opération (succès ou erreur).
        """
        deleted = self.chat_dao.delete(id_chat)
        if deleted:
            return ResponseService(*self.CHAT_DELETE_SUCCESS)
        return ResponseService(*self.CHAT_DELETE_ERROR)

    @log
    def search_chat_by_title(self, id_user: int, search: str) -> List[Chat]:
        """
        Recherche les conversations d’un utilisateur selon leur titre,
        en utilisant une similarité par distance de Levenshtein.

        Paramètres
        ----------
        id_user : int
            Identifiant utilisateur.
        search : str
            Mot-clé recherché.

        Retour
        ------
        List[Chat]
            Conversations triées par similarité décroissante.
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

    @log
    def search_chat_by_date(self, id_user: int, search_date: str) -> List[Chat]:
        """
        Recherche les conversations créées à une date spécifique.

        Paramètres
        ----------
        id_user : int
            Identifiant de l’utilisateur.
        search_date : str
            Date au format 'YYYY-MM-DD'.

        Retour
        ------
        List[Chat]
            Conversations triées par date décroissante.
        """
        date = datetime.strptime(search_date, "%Y-%m-%d")
        all_chats = self.chat_dao.search_by_date(id_user, date)
        if all_chats is None:
            return []
        all_chats.sort(key=lambda chat: chat.date_start, reverse=True)
        return all_chats

    @log
    def delete_all_chats(self, id_user: int):
        """
        Supprime toutes les conversations associées à un utilisateur.

        Paramètres
        ----------
        id_user : int
            Identifiant unique de l'utilisateur dont toutes les conversations
            doivent être supprimées.

        Retour
        ------
        ResponseService
            - Renvoie CHATS_CLEARED_SUCCES code 200.
            - Renvoie CHATS_CLEARED_ERROR code 500.

        Description
        """
        res = self.chat_dao.delete_all_chats(id_user)
        if res == False:
            return ResponseService(*self.CHATS_CLEARED_ERROR)
        return ResponseService(*self.CHATS_CLEARED_SUCCES)

    
    @log
    def counts_user_message(self, id_user: int):
        """
        Compte le nombre total de messages envoyés par un utilisateur.

        Paramètres
        ----------
        id_user : int
            Identifiant de l’utilisateur.

        Retour
        ------
        int
            Nombre total de messages (somme des messages de chaque chat).
        """
        chats = self.get_chats_by_id_user(id_user=id_user)

        if chats is None:
            return 0

        else:
            message_dao = MessageDAO()
            nombre_total_de_message = -1

            chats_ids = [c.id_chat for c in chats]        
            for id in chats_ids:
                messages = message_dao.get_messages_by_chat(id_chat=id)
                nombre_total_de_message += len(messages)

            return nombre_total_de_message + 1

    def split_text(self, text, max_len=95):
        """
        Coupe un long texte en plusieurs lignes à longueur maximale définie.
        Utilisé pour l’affichage propre des messages dans le PDF.

        Paramètres
        ----------
        text : str
            Texte à découper.
        max_len : int
            Longueur maximale par ligne.

        Retour
        ------
        List[str]
            Liste de lignes de texte.
        """
        words = text.split()
        lines = []
        current = ""

        for word in words:
            if len(current) + len(word) + 1 <= max_len:
                current += " " + word if current else word
            else:
                lines.append(current)
                current = word

        if current:
            lines.append(current)

        return lines

    @log 
    def export_chat_to_PDF(self, user: User, id_chat: int, messages: List[Message], file_path: str = "exports/"):
        """
        Exporte une conversation en PDF.

        Le PDF contient :
        - les informations utilisateur,
        - les informations du chat,
        - tous les messages de la conversation,
        - une mise en page propre et minimaliste.

        Paramètres
        ----------
        user : User
            Utilisateur associé au chat.
        id_chat : int
            Identifiant du chat à exporter.
        messages : List[Message]
            Liste des messages de la conversation.
        file_path : str
            Dossier de sortie (par défaut : "exports/").

        Retour
        ------
        str
            Chemin complet du fichier PDF exporté.
        """

        # Créer dossier par défaut si nécessaire
        chat = self.chat_dao.get_chat(id_chat=id_chat)

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        safe_title = "".join(c for c in chat.title if c.isalnum() or c in (" ", "_")).rstrip()
        filename = f"conversation_{chat.id_chat}_{safe_title}.pdf"
        file_path = os.path.join(file_path, filename)

        # Création du PDF
        pdf = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4

        
        y = height - 50

        # ---------- HEADER ----------
        pdf.setFillColor(colors.HexColor("#1F2937"))  # gris foncé élégant
        pdf.setFont("Helvetica-Bold", 18)
        pdf.drawString(40, y, "Conversation Exportée")
        y -= 30

        pdf.setFillColor(colors.black)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(40, y, f"Titre : {chat.title}")
        y -= 25

        # ---------- USER INFO ----------
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(40, y, "Informations de l'utilisateur")
        y -= 15
        pdf.setFont("Helvetica", 10)
        y -= 15
        pdf.drawString(40, y, f"Nom d'utilisateur     : {user.username}")
        y -= 30

        # ---------- CHAT INFO ----------
        pdf.setFont("Helvetica-Bold", 11)
        pdf.drawString(40, y, "Details de la conversation")
        y -= 15
        pdf.setFont("Helvetica", 10)
        y -= 15
        pdf.drawString(40, y,
                       f"Début         : {chat.date_start.strftime('%Y-%m-%d %H:%M')}")
        y -= 15
        pdf.drawString(40, y, f"Derniere maj    : {chat.last_date.strftime('%Y-%m-%d %H:%M')}")
        y -= 15
        pdf.drawString(40, y, f"Tokens         : {chat.max_tokens}")
        y -= 15
        pdf.drawString(40, y, f"Temperature    : {chat.temperature}")
        y -= 15
        pdf.drawString(40, y, f"Top_P          : {chat.top_p}")
        y -= 30

        # Séparation visuelle
        pdf.setStrokeColor(colors.grey)
        pdf.line(40, y, width - 40, y)
        y -= 40

        # ---------- MESSAGES ----------
        pdf.setFont("Helvetica-Bold", 12)
        pdf.setFillColor(colors.HexColor("#111827"))
        pdf.drawString(40, y, "Messages")
        y -= 30

        pdf.setFont("Helvetica", 10)

        for msg in messages:
            sender = msg.role_author
            content = msg.content
            timestamp = msg.date_sending.strftime("%Y-%m-%d %H:%M")

            pdf.setFillColor(colors.HexColor("#374151"))
            pdf.setFont("Helvetica-Bold", 10)
            pdf.drawString(40, y, f"{sender}  -  {timestamp}")
            y -= 15

            pdf.setFont("Helvetica", 10)
            pdf.setFillColor(colors.black)

            # Gestion du retour à la ligne
            for line in self.split_text(content, max_len=95):
                if y < 50:  # Nouvelle page si espace insuffisant
                    pdf.showPage()
                    y = height - 50
                    pdf.setFont("Helvetica", 10)
                pdf.drawString(50, y, line)
                y -= 13

            y -= 15  # Espace entre messages

        pdf.save()
        return file_path

    def export_chat_to_TXT(self, user: User, id_chat: int, messages: list[Message], file_path: str = "exports/") -> str:
        """
        Exporte une conversation au format texte (.txt).

        Contenu exporté :
        - Informations utilisateur
        - Informations du chat
        - Liste chronologique des messages
        - Mise en forme lisible

        Paramètres
        ----------
        user : User
            Utilisateur concerné.
        id_chat : int
            Identifiant du chat.
        messages : List[Message]
            Messages de la conversation.
        file_path : str
            Dossier de sortie.

        Retour
        ------
        str
            Chemin complet du fichier généré.
        """
        # Créer dossier par défaut si nécessaire

        if not os.path.exists(file_path):
            os.makedirs(file_path)

        chat = self.chat_dao.get_chat(id_chat=id_chat)

        filename = f"chat_{chat.id_chat}.txt"
        filepath = os.path.join(file_path, filename)

        with open(filepath, "w", encoding="utf-8") as f:

            # ---- HEADER ----
            f.write("=========================================\n")
            f.write("          CONVERSATION EXPORTÉE\n")
            f.write("=========================================\n\n")

            # ---- USER INFO ----
            f.write("👤 UTILISATEUR\n")
            f.write(f"ID utilisateur   : {user.id_user}\n")
            f.write(f"Nom d'utilisateur: {user.username}\n\n")

            f.write("-----------------------------------------\n")

            # ---- CHAT INFO ----
            f.write("💬 CONVERSATION\n")
            f.write(f"ID chat        : {chat.id_chat}\n")
            f.write(f"Titre          : {chat.title}\n")
            f.write(f"Début          : {chat.date_start.strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Dernière maj   : {chat.last_date.strftime('%Y-%m-%d %H:%M')}\n")
            f.write(f"Max Tokens     : {chat.max_tokens}\n")
            f.write(f"Top P          : {chat.top_p}\n")
            f.write(f"Température    : {chat.temperature}\n\n")

            f.write("-----------------------------------------\n")
            f.write("📨 MESSAGES\n\n")

            # ---- MESSAGES ----
            for msg in messages:
                role = msg.role_author.capitalize()
                timestamp = msg.date_sending.strftime("%Y-%m-%d %H:%M:%S")

                f.write(f"[{timestamp}] {role} :\n")
                f.write(f"{msg.content}\n\n")

            f.write("=========================================\n")
            f.write("        FIN DE LA CONVERSATION\n")
            f.write("=========================================\n")

        return filepath

    @log
    def get_user_statistics(self, id_user: int) -> dict[str, any]:
        """
        Retourne des statistiques détaillées pour un utilisateur :

        - nb_conversations : int
        - nb_messages : int
        - avg_messages_per_chat : float
        - first_chat_date : str (YYYY-MM-DD HH:MM)
        - last_chat_date  : str (YYYY-MM-DD HH:MM)

        Paramètres
        ----------
        id_user : int
            Identifiant utilisateur.

        Retour
        ------
        dict
            Dictionnaire contenant les statistiques calculées.
        """
        stats = {
            "nb_conversations": 0,
            "nb_messages": 0,
            "avg_messages_per_chat": 0,
            "first_chat_date": None,
            "last_chat_date": None,
        }

        chats = self.get_chats_by_id_user(id_user)

        if not chats:
            return stats

        stats["nb_conversations"] = len(chats)
        stats["nb_messages"] = self.counts_user_message(id_user) - 1
        stats["first_chat_date"] = min(chat.date_start for chat in chats).strftime(
            "%Y-%m-%d %H:%M")
        stats["last_chat_date"] = max(chat.last_date for chat in chats).strftime(
            "%Y-%m-%d %H:%M")

        # Titre de la dernière conversation (par date)

        # Moyenne de messages par conversation
        stats["avg_messages_per_chat"] = round(
            stats["nb_messages"] / stats["nb_conversations"], 2
        )

        return stats
    
    def update_parameters_chat(self, id_chat: int, context: str, max_tokens: int,
                               top_p: float, temperature: float) -> ResponseService:
        """
        Met à jour les paramètres d’un chat (si ces champs existent dans la BDD).
        Pour le moment, on suppose qu’ils seront stockés ailleurs.
        """
        pass
