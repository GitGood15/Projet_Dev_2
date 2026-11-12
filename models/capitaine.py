import uuid
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from models.equipe import Equipe

class Capitaine:
    def __init__(self, nom: str, prenom: str, telephone: str):
        self.__id: str(uuid.uuid4())
        self.__nom: nom
        self.__prenom: prenom
        self.__telephone: telephone
        self.__points_soirees: []
    
    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def nom(self) -> str:
        return self.__nom
    
    @property
    def prenom(self) -> str:
        return self.__prenom
    
    @property
    def telephone(self) -> str:
        return self.__telephone
    
    @property
    def points_soirees(self) -> List[int]:
        return list(self.__points_soirees)
    
    def associer_equipe(self, e: 'Equipe') -> None:
        """Valide l'association avec une équipe du soir."""
        if e is None:
            raise ValueError("L'équipe à associer ne peut pas être nulle.")
    
    def ajouter_points_championnat(self, pts: int) -> None:
        """Ajoute les points d'une soirée à l'historique du capitaine."""
        if pts > 0:
            self.__points_soirees.append(pts)
            
    def calculer_points_top10(self) -> int:
        """Retourne la somme des 10 meilleurs résultats de l'année."""
        scores_tries = sorted(self.__points_soirees, reverse=True)
        return sum(scores_tries[:10])
    
    def reinitialiser_points_saison(self) -> None:
        """Remet à zéro les points du championnat après validation."""
        self.__points_soirees = []
        
   # --- Persistance JSON ---