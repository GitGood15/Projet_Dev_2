import os
from datetime import date
from models.cafe import Cafe
from models.question import Question
from models.soiree_quiz import SoireeQuiz
from models.manche import Manche
from models.championnat_annuel import ChampionnatAnnuel
from services.sauvegarde import Sauvegarde


class InterfaceCLI:
    def __init__(self, cafe: Cafe, chemin_donnees_locales: str = "data/donnees_cafe.json"):
        self.__cafe = cafe
        self.__sauvegarde = Sauvegarde()
        self.__chemin_local = chemin_donnees_locales
        self.__classement_visible = True
        self.__charger_donnees_locales()

    def __charger_donnees_locales(self) -> None:
        if os.path.isfile(self.__chemin_local):
            try:
                contenu = self.__sauvegarde.importer_donnees(self.__chemin_local)
                self.__cafe.restaurer_etat(contenu)
            except Exception as e:
                print(f"[Avertissement] Impossible de charger les données locales : {e}")

    def __sauvegarder_auto(self) -> None:
        """Enregistre automatiquement les données en local après chaque modification (ENF-03, RM-14)."""
        dossier = os.path.dirname(self.__chemin_local)
        if dossier and not os.path.exists(dossier):
            os.makedirs(dossier)
        with open(self.__chemin_local, "w", encoding="utf-8") as f:
            f.write(self.__cafe.serialiser_etat())

    def __obtenir_soiree_active(self) -> SoireeQuiz:
        for s in self.__cafe.soirees:
            if s.en_cours:
                return s
        return None

    def lancer(self) -> None:
        while True:
            soiree_active = self.__obtenir_soiree_active()
            statut = f"EN COURS ({soiree_active.date.isoformat()})" if soiree_active else "Aucune"

            print("\n==============================================")
            print(f"  {self.__cafe.nom.upper()} - GESTION QUIZ")
            print(f"  Soirée active : {statut}")
            print("==============================================")
            print("1. Gérer les équipes (F-01)")
            print("2. Gérer et importer les questions (F-02)")
            print("3. Organiser une nouvelle soirée (F-03)")
            print("4. Encoder / modifier les scores et mises (F-04, F-07)")
            print("5. Clôturer la soirée en cours (RM-13, EF-06.1)")
            print("6. Consulter l'historique des soirées (F-05)")
            print("7. Consulter le championnat annuel (F-06)")
            print("8. Sauvegarder / Restaurer sur clé USB (F-08)")
            print("9. Annuler la dernière modification (F-09)")
            print("0. Quitter")

            choix = input("\nVotre choix : ").strip()

            try:
                if choix == "1":
                    self.__menu_equipes()
                elif choix == "2":
                    self.__menu_questions()
                elif choix == "3":
                    self.__menu_organiser_soiree()
                elif choix == "4":
                    self.__menu_scores()
                elif choix == "5":
                    self.__menu_cloturer_soiree()
                elif choix == "6":
                    self.__menu_historique()
                elif choix == "7":
                    self.__menu_championnat()
                elif choix == "8":
                    self.__menu_sauvegarde_usb()
                elif choix == "9":
                    self.__cafe.restaurer_etat_precedent()
                    self.__sauvegarder_auto()
                    print("[OK] Dernière modification annulée (RM-15).")
                elif choix == "0":
                    self.__sauvegarder_auto()
                    print("Données enregistrées localement. À mardi prochain !")
                    break
                else:
                    print("[Erreur] Choix invalide.")
            except Exception as e:
                print(f"[Erreur] {e}")

    # --- F-01 : Gérer les équipes ---
    def __menu_equipes(self) -> None:
        print("\n--- F-01 : INSCRIPTION D'UNE ÉQUIPE ---")
        nom_cap = input("Nom du capitaine : ").strip()
        prenom_cap = input("Prénom du capitaine : ").strip()

        cap = self.__cafe.rechercher_capitaine(nom_cap, prenom_cap)
        if cap is None:
            print("Nouveau capitaine détecté (EF-01.0).")
            tel = input("Téléphone du capitaine : ").strip()
            cap = self.__cafe.creer_capitaine(nom_cap, prenom_cap, tel)
        else:
            print(f"Capitaine retrouvé : {cap.prenom} {cap.nom} (EF-01.1).")

        nom_soiree = input("Nom de l'équipe pour ce soir : ").strip()
        nb_joueurs = int(input("Nombre de participants (capitaine inclus) : "))
        equipe = self.__cafe.creer_equipe(cap, nom_soiree, nb_joueurs)

        soiree_active = self.__obtenir_soiree_active()
        if soiree_active is not None:
            inscrire = input("Inscrire directement cette équipe à la soirée en cours ? (o/n) : ").strip().lower()
            if inscrire == "o":
                soiree_active.inscrire_equipe(equipe)
                print(f"[OK] Équipe '{equipe.nom_soiree}' inscrite à la soirée en cours (RM-11).")

        self.__sauvegarder_auto()
        print(f"[OK] Équipe '{equipe.nom_soiree}' enregistrée pour {cap.prenom} {cap.nom}.")

    # --- F-02 : Gérer et importer les questions ---
    def __menu_questions(self) -> None:
        print("\n--- F-02 : BANQUE DE QUESTIONS ---")
        print("1. Ajouter une question")
        print("2. Supprimer une question")
        print("3. Importer depuis un fichier CSV / JSON")
        print("4. Lister les questions disponibles aujourd'hui (RM-05)")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            enonce = input("Énoncé : ")
            reponse = input("Réponse attendue : ")
            theme = input("Thème : ")
            diff = int(input("Difficulté (1 à 3) : "))
            q = Question(enonce, reponse, theme, diff)
            self.__cafe.ajouter_question(q)
            self.__sauvegarder_auto()
            print(f"[OK] Question ajoutée ({q.id}).")

        elif choix == "2":
            for q in self.__cafe.questions:
                print(f"  [{q.id}] ({q.theme} - Niv.{q.niveau_difficulte}) {q.enonce}")
            q_id = input("ID de la question à supprimer : ").strip()
            self.__cafe.supprimer_question(q_id)
            self.__sauvegarder_auto()
            print("[OK] Question supprimée.")

        elif choix == "3":
            chemin = input("Chemin du fichier (.csv ou .json) : ").strip()
            self.__cafe.importer_questions(chemin)
            self.__sauvegarder_auto()
            print("[OK] Questions importées avec succès.")

        elif choix == "4":
            aujourd_hui = date.today()
            dispos = [q for q in self.__cafe.questions if q.est_disponible(aujourd_hui)]
            print(f"\nQuestions disponibles ({len(dispos)}/{len(self.__cafe.questions)}) :")
            for q in dispos:
                print(f"  [{q.id}] ({q.theme} - Niv.{q.niveau_difficulte}) {q.enonce} -> Rép: {q.reponse}")

    # --- F-03 : Organiser une soirée ---
    def __menu_organiser_soiree(self) -> None:
        if self.__cafe.a_soiree_en_cours():
            raise ValueError("Une soirée est déjà en cours. Clôturez-la avant d'en créer une nouvelle.")

        print("\n--- F-03 : ORGANISER UNE SOIRÉE QUIZ ---")
        nb_manches = int(input("Nombre de manches (défaut 6) : ") or "6")
        nb_questions = int(input("Nombre de questions par manche (défaut 8) : ") or "8")
        num_miser = int(input("Numéro de la manche à miser (0 si aucune) : ") or "6")

        soiree = SoireeQuiz.creer_soiree(date.today(), nb_manches, nb_questions)
        for i in range(1, nb_manches + 1):
            soiree.ajouter_manche(Manche(i, est_a_miser=(i == num_miser)))

        self.__cafe.ajouter_soiree(soiree)
        self.__sauvegarder_auto()
        print(f"[OK] Soirée créée ({nb_manches} manches de {nb_questions} questions). Inscrivez les équipes via le menu 1.")

    # --- F-04 & F-07 : Encoder et modifier les scores ---
    def __menu_scores(self) -> None:
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            raise ValueError("Aucune soirée n'est actuellement en cours.")
        if not soiree.equipes:
            raise ValueError("Aucune équipe n'est inscrite à cette soirée.")

        print("\n--- F-04 / F-07 : SCORES ET CLASSEMENT ---")
        print("1. Encoder les scores d'une manche")
        print("2. Modifier un score déjà encodé (EF-04.2)")
        print(f"3. {'Masquer' if self.__classement_visible else 'Afficher'} le classement (EF-04.3)")
        print("4. Départager une égalité - Question subsidiaire (RM-08)")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            for m in soiree.manches:
                tag = " [MANCHE À MISER]" if m.est_a_miser else ""
                print(f"  Manche {m.numero}{tag}")
            num_manche = int(input("Numéro de la manche : "))

            manche_cible = next((m for m in soiree.manches if m.numero == num_manche), None)
            if manche_cible is None:
                raise ValueError("Manche introuvable.")

            self.__cafe.sauvegarder_etat_temporaire()
            for eq in soiree.equipes:
                if manche_cible.est_a_miser:
                    print(f"\nÉquipe '{eq.nom_soiree}' (score actuel : {eq.calculer_score_total()} pts)")
                    mise = int(input("  Mise (1 à 5) : "))
                    rep = input("  Bonne réponse ? (o/n) : ").strip().lower() == "o"
                    manche_cible.enregistrer_score(eq, 0, mise, rep)
                else:
                    pts = int(input(f"Points obtenus par '{eq.nom_soiree}' : "))
                    soiree.enregistrer_score_equipe(eq, num_manche, pts)

            self.__sauvegarder_auto()
            if self.__classement_visible:
                self.__afficher_classement_soiree(soiree)
            else:
                print("[OK] Scores enregistrés (classement masqué).")

        elif choix == "2":
            eq = self.__choisir_equipe(soiree)
            num_manche = int(input("Numéro de la manche à corriger : "))
            nouveaux_pts = int(input("Nouveau score pour cette manche : "))
            self.__cafe.sauvegarder_etat_temporaire()
            soiree.modifier_score_equipe(eq, num_manche, nouveaux_pts)
            self.__sauvegarder_auto()
            if self.__classement_visible:
                self.__afficher_classement_soiree(soiree)

        elif choix == "3":
            self.__classement_visible = not self.__classement_visible
            print(f"[OK] Classement désormais {'VISIBLE' if self.__classement_visible else 'MASQUÉ'}.")
            if self.__classement_visible:
                self.__afficher_classement_soiree(soiree)

        elif choix == "4":
            self.__afficher_classement_soiree(soiree)
            print("Sélectionnez les deux équipes ex æquo :")
            e1 = self.__choisir_equipe(soiree)
            e2 = self.__choisir_equipe(soiree)
            gagnante_choix = input(f"Quelle équipe remporte la subsidiaire ? (1: {e1.nom_soiree} / 2: {e2.nom_soiree}) : ").strip()
            gagnante = e1 if gagnante_choix == "1" else e2
            self.__cafe.sauvegarder_etat_temporaire()
            soiree.departager_egalite(e1, e2, gagnante)
            self.__sauvegarder_auto()
            self.__afficher_classement_soiree(soiree)

    def __choisir_equipe(self, soiree: SoireeQuiz):
        for idx, eq in enumerate(soiree.equipes, start=1):
            print(f"  {idx}. {eq.nom_soiree} (Cap: {eq.capitaine.prenom} {eq.capitaine.nom})")
        choix = int(input("Numéro de l'équipe : ")) - 1
        if choix < 0 or choix >= len(soiree.equipes):
            raise ValueError("Numéro d'équipe invalide.")
        return soiree.equipes[choix]

    def __afficher_classement_soiree(self, soiree: SoireeQuiz) -> None:
        print(f"\n--- CLASSEMENT DE LA SOIRÉE ({soiree.date.isoformat()}) ---")
        classement = soiree.calculer_classement_soiree()
        for rang, eq in enumerate(classement, start=1):
            sub = " (Subsidiaire)" if eq.vainqueur_subsidiaire else ""
            print(f"  {rang}. {eq.nom_soiree} - {eq.calculer_score_total()} pts{sub}")

    # --- Clôture de soirée ---
    def __menu_cloturer_soiree(self) -> None:
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            raise ValueError("Aucune soirée active à clôturer.")

        self.__cafe.sauvegarder_etat_temporaire()
        soiree.cloturer_soiree()
        self.__sauvegarder_auto()
        self.__afficher_classement_soiree(soiree)
        print("\n[OK] Soirée clôturée et points attribués au championnat annuel (RM-13).")
        print("[Rappel RM-14] Pensez à effectuer une sauvegarde sur clé USB via le menu 8 !")

    # --- F-05 : Historique ---
    def __menu_historique(self) -> None:
        print("\n--- F-05 : RECHERCHE DANS L'HISTORIQUE ---")
        critere = input("Critère (date / equipe / capitaine) : ").strip()
        valeur = input("Valeur recherchée : ").strip()
        trouvees = self.__cafe.rechercher_soirees(critere, valeur)

        if not trouvees:
            print("Aucune soirée correspondante.")
            return

        for idx, s in enumerate(trouvees, start=1):
            print(f"  {idx}. Soirée du {s.date.isoformat()} ({len(s.equipes)} équipes)")
        choix = int(input("Numéro de la soirée à détailler : ")) - 1
        if 0 <= choix < len(trouvees):
            self.__afficher_classement_soiree(trouvees[choix])

    # --- F-06 : Championnat annuel ---
    def __menu_championnat(self) -> None:
        annee = int(input("\nAnnée du championnat à consulter (ex: 2026) : ") or str(date.today().year))
        champ = ChampionnatAnnuel(annee, self.__cafe.capitaines)
        classement = champ.calculer_classement_annuel()

        print(f"\n--- CHAMPIONNAT ANNUEL {annee} (TOP 10) ---")
        for rang, cap in enumerate(classement, start=1):
            print(f"  {rang}. {cap.prenom} {cap.nom} - {cap.calculer_points_top10()} pts ({len(cap.points_soirees)} soirées)")

        action = input("\nClôturer le championnat et remettre les points à zéro ? (o/n) : ").strip().lower()
        if action == "o":
            gagnant = champ.determiner_gagnant()
            if gagnant:
                print(f"Vainqueur du championnat {annee} : {gagnant.prenom} {gagnant.nom} ({gagnant.calculer_points_top10()} pts) !")
            confirm = input("Confirmer la remise à zéro définitive des points ? (OUI) : ").strip()
            if confirm == "OUI":
                self.__cafe.sauvegarder_etat_temporaire()
                champ.reinitialiser_points()
                self.__sauvegarder_auto()
                print("[OK] Points du championnat remis à zéro (EF-06.5).")

    # --- F-08 : Sauvegarde et restauration USB ---
    def __menu_sauvegarde_usb(self) -> None:
        print("\n--- F-08 : SAUVEGARDE / RESTAURATION USB ---")
        print("1. Sauvegarder les données sur clé USB")
        print("2. Restaurer depuis un fichier de sauvegarde")
        choix = input("Votre choix : ").strip()

        if choix == "1":
            chemin_usb = input("Chemin du dossier de la clé USB (ex: E:\\ ou /media/usb) : ").strip()
            self.__sauvegarde.exporter_donnees(self.__cafe, chemin_usb)
            print("[OK] Sauvegarde effectuée sur la clé USB.")
        elif choix == "2":
            chemin_fichier = input("Chemin complet du fichier .json à restaurer : ").strip()
            donnees = self.__sauvegarde.importer_donnees(chemin_fichier)
            self.__cafe.sauvegarder_etat_temporaire()
            self.__cafe.restaurer_etat(donnees)
            self.__sauvegarder_auto()
            print("[OK] Données restaurées avec succès.")