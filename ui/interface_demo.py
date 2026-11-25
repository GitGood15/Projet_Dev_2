"""Interface réduite pour présenter le parcours principal d'une soirée quiz."""

import os
from datetime import date

from models.cafe import Cafe
from models.manche import Manche
from models.soiree_quiz import SoireeQuiz


class InterfaceDemo:
    """Permet de créer une soirée, inscrire des équipes, saisir des scores et afficher le classement."""

    def __init__(self, cafe: Cafe, chemin_donnees_locales: str = "data/donnees_cafe.json"):
        self.__cafe = cafe
        self.__chemin_local = chemin_donnees_locales
        self.__charger_donnees_locales()

    def __charger_donnees_locales(self) -> None:
        if not os.path.isfile(self.__chemin_local):
            return
        try:
            with open(self.__chemin_local, "r", encoding="utf-8") as fichier:
                donnees = fichier.read()
            if not donnees.strip():
                print("[Avertissement] Fichier local vide ; démarrage avec des données vierges.")
                return
            self.__cafe.restaurer_etat(donnees)
        except (OSError, ValueError, KeyError, TypeError) as erreur:
            print(f"[Avertissement] Chargement des données impossible : {erreur}")

    def __sauvegarder_auto(self) -> None:
        dossier = os.path.dirname(self.__chemin_local)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        with open(self.__chemin_local, "w", encoding="utf-8") as fichier:
            fichier.write(self.__cafe.serialiser_etat())

    def __obtenir_soiree_active(self) -> SoireeQuiz | None:
        return next((soiree for soiree in self.__cafe.soirees if soiree.en_cours), None)

    @staticmethod
    def __lire_texte(message: str) -> str:
        while True:
            valeur = input(message).strip()
            if valeur:
                return valeur
            print("Cette information est obligatoire.")

    @staticmethod
    def __lire_entier(
        message: str, minimum: int, maximum: int | None = None, defaut: int | None = None
    ) -> int:
        while True:
            valeur = input(message).strip()
            if not valeur and defaut is not None:
                return defaut
            try:
                nombre = int(valeur)
                if nombre < minimum or (maximum is not None and nombre > maximum):
                    raise ValueError
                return nombre
            except ValueError:
                limites = f"entre {minimum} et {maximum}" if maximum is not None else f"au moins {minimum}"
                print(f"Veuillez saisir un nombre entier {limites}.")

    def lancer(self) -> None:
        actions = {
            "1": self.__creer_soiree,
            "2": self.__inscrire_equipe,
            "3": self.__saisir_scores,
            "4": self.__afficher_classement,
            "5": self.__terminer_soiree,
        }
        while True:
            soiree = self.__obtenir_soiree_active()
            statut = f"En cours ({soiree.date:%d/%m/%Y})" if soiree else "Aucune"
            print(f"\n=== {self.__cafe.nom.upper()} — MODE DÉMO ===")
            print(f"Soirée active : {statut}")
            print("1. Créer une soirée")
            print("2. Inscrire une équipe")
            print("3. Saisir les scores d'une manche")
            print("4. Afficher le classement")
            print("5. Terminer la soirée en cours")
            print("0. Quitter")

            choix = input("Votre choix : ").strip()
            if choix == "0":
                self.__sauvegarder_auto()
                print("Données enregistrées. Au revoir !")
                return

            action = actions.get(choix)
            if action is None:
                print("[Erreur] Choix invalide.")
                continue
            try:
                action()
            except (ValueError, OSError, KeyError, TypeError) as erreur:
                print(f"[Erreur] {erreur}")

    def __creer_soiree(self) -> None:
        if self.__cafe.a_soiree_en_cours():
            raise ValueError("Une soirée est déjà en cours.")

        print("\n--- CRÉER UNE SOIRÉE ---")
        nb_manches = self.__lire_entier("Nombre de manches [3] : ", 1, defaut=3)
        nb_questions = self.__lire_entier("Questions par manche [5] : ", 1, defaut=5)
        soiree = SoireeQuiz.creer_soiree(date.today(), nb_manches, nb_questions)
        for numero in range(1, nb_manches + 1):
            soiree.ajouter_manche(Manche(numero, False))
        self.__cafe.ajouter_soiree(soiree)
        self.__sauvegarder_auto()
        print(f"[OK] Soirée créée : {nb_manches} manches de {nb_questions} questions.")

    def __inscrire_equipe(self) -> None:
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            raise ValueError("Créez d'abord une soirée.")

        print("\n--- INSCRIRE UNE ÉQUIPE ---")
        nom = self.__lire_texte("Nom du capitaine : ")
        prenom = self.__lire_texte("Prénom du capitaine : ")
        capitaine = self.__cafe.rechercher_capitaine(nom, prenom)
        if capitaine is not None and any(
            equipe.capitaine.id == capitaine.id for equipe in soiree.equipes
        ):
            raise ValueError("Ce capitaine est déjà inscrit à cette soirée.")
        telephone = input("Téléphone (facultatif) : ").strip() if capitaine is None else ""
        nom_equipe = self.__lire_texte("Nom de l'équipe : ")
        participants = self.__lire_entier("Nombre de participants, capitaine inclus : ", 1)
        if capitaine is None:
            capitaine = self.__cafe.creer_capitaine(nom, prenom, telephone)
        equipe = self.__cafe.creer_equipe(capitaine, nom_equipe, participants)
        soiree.inscrire_equipe(equipe)
        self.__sauvegarder_auto()
        print(f"[OK] Équipe « {equipe.nom_soiree} » inscrite.")

    def __saisir_scores(self) -> None:
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            raise ValueError("Aucune soirée n'est en cours. Créez d'abord une soirée.")
        if not soiree.equipes:
            raise ValueError("Inscrivez d'abord au moins une équipe.")

        print("\n--- SAISIR LES SCORES ---")
        for manche in soiree.manches:
            print(f"Manche {manche.numero}")
        numero = self.__lire_entier("Numéro de manche : ", 1, soiree.nb_manches)
        manche = soiree.obtenir_manche(numero)
        equipes_a_saisir = [
            equipe for equipe in soiree.equipes if manche.score_pour(equipe) is None
        ]
        if not equipes_a_saisir:
            raise ValueError("Les scores de cette manche ont déjà été saisis.")

        for equipe in equipes_a_saisir:
            points = self.__lire_entier(
                f"Score de {equipe.nom_soiree} (0 à {soiree.nb_questions_par_manche}) : ",
                0,
                soiree.nb_questions_par_manche,
            )
            soiree.enregistrer_score_equipe(equipe, numero, points)
            self.__sauvegarder_auto()

        print("[OK] Scores enregistrés.")
        self.__afficher_classement()

    def __afficher_classement(self) -> None:
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            raise ValueError("Aucune soirée n'est en cours. Créez d'abord une soirée.")
        if not soiree.equipes:
            raise ValueError("Aucune équipe n'est inscrite à cette soirée.")

        print(f"\n--- CLASSEMENT DU {soiree.date:%d/%m/%Y} ---")
        for rang, equipe in enumerate(soiree.calculer_classement_soiree(), start=1):
            print(f"{rang}. {equipe.nom_soiree} — {equipe.calculer_score_total()} point(s)")

    def __terminer_soiree(self) -> None:
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            raise ValueError("Aucune soirée en cours à terminer.")
        if input("Terminer la soirée et attribuer les points de championnat ? (o/n) : ").strip().lower() not in (
            "o",
            "oui",
        ):
            print("Clôture annulée.")
            return

        soiree.cloturer_soiree()
        self.__sauvegarder_auto()
        self.__afficher_classement_termine(soiree)
        print("[OK] Soirée terminée et points de championnat attribués.")

    @staticmethod
    def __afficher_classement_termine(soiree: SoireeQuiz) -> None:
        print(f"\n--- CLASSEMENT FINAL DU {soiree.date:%d/%m/%Y} ---")
        for rang, equipe in enumerate(soiree.calculer_classement_soiree(), start=1):
            print(f"{rang}. {equipe.nom_soiree} — {equipe.calculer_score_total()} point(s)")
