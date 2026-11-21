import os
from datetime import date

from models.cafe import Cafe
from models.championnat_annuel import ChampionnatAnnuel
from models.manche import Manche
from models.question import Question
from models.soiree_quiz import SoireeQuiz
from services.sauvegarde import Sauvegarde

class Terminal:
    """Présente les menus et délègue les opérations aux modèles du domaine."""
    
    def __init__(self, cafe: Cafe, chemin_donnees_locales: str = "data/donnees_cafe.json"):
        self.__cafe = cafe
        self.__sauvegarde = Sauvegarde()
        self.__chemin_local = chemin_donnees_locales
        self.__classement_visible = True
        self.__charger_donnees_locales()
        
    def __charger_donnees_locales(self) -> None:
        if not os.path.isfile(self.__chemin_local):
            return
        try:
            with open(self.__chemin_local, "r", encoding="utf-8") as fichier:
                self.__cafe.restaurer_etat(ficiher.read())
        except (OSError, ValueError, KeyError, TypeError) as erreur:
            print(f"[Avertissement] Chargement des données impossible : {erreur}")