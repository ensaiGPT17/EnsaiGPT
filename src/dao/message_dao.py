from typing import Optional, List
from datetime import datetime
from model.message import Message
from dao.db_connection import DBConnection
from utils.singleton import Singleton


class MessageDAO(metaclass=Singleton):
    def __init__(self):
        pass

    def create_message(self, id_chat: int, role: str, content: str) -> Optional[Message]:
        """ ajouter un nouveau message a la bdd
        
        Parameters
        ----------
        id_chat : l'id de la conversation a laquelle le message appartient
        role : l'auteur du message 
        content : le contenu du message 
        
        Returns 
        --------
        L'objet Message cree 
        ou None en cas d'errreur 

        """
        pass

    def delete_message(self, id_message: int) -> bool:
        """supprimer un message de la bdd
        
        Parameters
        ----------
        id_message : l'id du message a supprimer
        
        Returns 
        -------
        bool : true si le message a bien ete supprime
        
        """
        pass

    def get_message_by_id(self, id_message: int) -> Optional[Message]:
        """ recuperer un message par son id
        
        Parameters 
        -----------
        id_message : l'identifiant du message 

        Returns 
        --------
        Un objet Message s'il existe
        None sinon
        
        """
        pass

    # def get_messages_by_chat(self, id_chat) ici ou dans chatDAO ?