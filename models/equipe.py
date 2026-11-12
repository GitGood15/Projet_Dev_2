import uuid
from typing import List
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
        
    @property
    def id(self) -> str:
        return self.__id

    @property
    def nom_soiree(self) -> str:
        return self.__nom_soiree

    @property
    def nb_participants(self) -> int:
        return self.__nb_participants

    @property
    def vainqueur_subsidiaire(self) -> bool:
        return self.__vainqueur_subsidiaire

    @property
    def capitaine(self) -> Capitaine:
        return self.__capitaine

    @property
    def scores(self) -> List['Score']:
        return list(self.__scores)
    
    def ajouter_score(self, score: 'Score') -> None:
        """Associe un score de manche à l'équipe."""
        if score not in self.__scores:
            self.__scores.append(score)
    
    def calculer_score_total(self) -> int:
        """Calcule le score total de l'équipe sur la soirée."""
        return sum(score.calculer_points_manche() for score in self.__scores)
    
    def definir_vainqueur_subsidiaire(self, est_vainqueur: bool) -> None:
        """Met à jour le statut de départage en cas d'égalité au classement final."""
        self.__vainqueur_subsidiaire = est_vainqueur