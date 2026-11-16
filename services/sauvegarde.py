import os
from datetime import date
from models.cafe import Cafe


class Sauvegarde:
    def __init__(self, chemin_usb: str = "", date_sauvegarde: date = None):
        # Attributs exacts du diagramme de classes
        self.__date_sauvegarde = date_sauvegarde
        self.__chemin_usb = chemin_usb

    @property
    def date_sauvegarde(self) -> date:
        return self.__date_sauvegarde

    @property
    def chemin_usb(self) -> str:
        return self.__chemin_usb

    def verifier_support_externe(self, chemin_usb: str) -> bool:
        """Vérifie qu'une clé USB est connectée et accessible en écriture (EF-08.2, Diagramme F-08)."""
        if not chemin_usb or not chemin_usb.strip():
            return False
        return os.path.isdir(chemin_usb) and os.access(chemin_usb, os.W_OK)

    def exporter_donnees(self, cafe: Cafe, chemin_usb: str) -> None:
        """Exporte l'ensemble des données du café sur la clé USB au format JSON (D-06, EF-08.1, EF-08.2)."""
        if not self.verifier_support_externe(chemin_usb):
            raise FileNotFoundError("Clé USB non connectée ou inaccessible (EF-08.2).")
        if cafe is None:
            raise ValueError("L'instance de Cafe ne peut pas être nulle.")

        donnees_completes = cafe.serialiser_etat()
        self.__date_sauvegarde = date.today()
        self.__chemin_usb = chemin_usb

        nom_fichier = f"sauvegarde_quiz_{self.__date_sauvegarde.isoformat()}.json"
        chemin_complet = os.path.join(chemin_usb, nom_fichier)

        with open(chemin_complet, "w", encoding="utf-8") as fichier:
            fichier.write(donnees_completes)

    def importer_donnees(self, chemin_fichier: str) -> str:
        """Lit un fichier de sauvegarde existant et retourne son contenu sérialisé (EF-08.3, Diagramme F-08)."""
        if not chemin_fichier or not os.path.isfile(chemin_fichier):
            raise FileNotFoundError(f"Fichier de sauvegarde introuvable : '{chemin_fichier}' (EF-08.3).")

        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()