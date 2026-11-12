import os
from datetime import date
from models.cafe import Cafe


class Sauvegarde:
    def __init__(self, chemin_usb: str = "", date_sauvegarde: date = None):
        self.__date_sauvegarde = date_sauvegarde
        self.__chemin_usb = chemin_usb

    @property
    def date_sauvegarde(self) -> date:
        return self.__date_sauvegarde

    @property
    def chemin_usb(self) -> str:
        return self.__chemin_usb

    def verifier_support_externe(self, chemin_usb: str) -> bool:
        """Vérifie que la clé USB est connectée et accessible en écriture."""
        if not chemin_usb or not chemin_usb.strip():
            return False
        return os.path.isdir(chemin_usb) and os.access(chemin_usb, os.W_OK)

    def exporter_donnees(self, cafe: Cafe, chemin_usb: str) -> None:
        """Exporte l'état complet du café au format JSON sur la clé USB."""
        if not self.verifier_support_externe(chemin_usb):
            raise FileNotFoundError("Clé USB non connectée ou inaccessible.")
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
        """Lit un fichier de sauvegarde existant et retourne son contenu sérialisé."""
        if not chemin_fichier or not os.path.isfile(chemin_fichier):
            raise FileNotFoundError(f"Fichier de sauvegarde introuvable : '{chemin_fichier}'.")

        with open(chemin_fichier, "r", encoding="utf-8") as fichier:
            return fichier.read()