import uuid
from typing import List, Dict, Any
from models.capitaine import Capitaine

class Equipe:
    def __init__(self, nom_soiree: str, nb_participants: int, capitaine: Capitaine):
        if not nom_soiree or not nom_soiree.strip():
            raise ValueError("Le nom de l'équipe pour la soirée est obligatoire.")
        if nb_participants < 1:
            raise ValueError("Une équipe doit compter au moins 1 participant, capitaine inclus.")
        
        self.__id = str(uuid.uuid4())
        self.__nom_soiree = nom_soiree.strip()
        self.__nb_participants = nb_participants
        self.__vainqueur_subsidiaire = False
        
        self.__capitaine = capitaine
        self.__scores = []