import uuid
from datetime import date

class Question:
    def __init__(self, enonce : str, reponse : str, theme : str, niveau_diffulte : int, derniere_utilisation : date = None):
        if not enonce or not enonce.strip():
            raise ValueError("L'énoncé de la question est obligatoire.")
        if not reponse or not reponse.strip():
            raise ValueError("La réponse attendue est obligatoire.")
        if niveau_difficulte < 1 or niveau_difficulte > 3:
            raise ValueError("Le niveau de difficulté doit être compris entre 1 et 3.")
        
        self.__id = str(uuid.uuid4)
        self.__enonce = enonce.strip()
        self.__reponse = reponse.strip()
        self.__theme = theme.strip() if theme else "Général"
        self.__niveau_diffulte = niveau_diffulte
        self.__derniere_utilisation = derniere_utilisation
        
    @property
    def id(self) -> str:
        return self.__id

    @property
    def enonce(self) -> str:
        return self.__enonce

    @property
    def reponse(self) -> str:
        return self.__reponse

    @property
    def theme(self) -> str:
        return self.__theme

    @property
    def niveau_difficulte(self) -> int:
        return self.__niveau_difficulte
    
    @property
    def derniere_utilisation(self) -> Date:
        return self.__derniere_utilisation
    
    def est_disponible(self, date_soiree: date) -> bool:
        """Vérifie qu'au moins 1 an s'est écoulé depuis la dernière utilisation."""
        if self.__derniere_utilisation is None:
            return True

        try:
            date_disponibilite = self.__derniere_utilisation.replace(
                year=self.__derniere_utilisation.year + 1
            )
        except ValueError:
            """Cas si la question à été posée un 29 février (année bissextile) -> 1er mars suivant"""
            date_disponibilite = date(self.__derniere_utilisation.year + 1, 3, 1)

        return date_soiree >= date_disponibilite
    
    def marquer_utilisee(self, date_soiree: date) -> None:
        """Enregistre la date d'utilisation de la question."""
        self.__derniere_utilisation = date_soiree