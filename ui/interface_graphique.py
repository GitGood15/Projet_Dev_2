import os
from datetime import date

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.core.window import Window

from models.cafe import Cafe
from models.question import Question
from models.soiree_quiz import SoireeQuiz
from models.manche import Manche
from models.championnat_annuel import ChampionnatAnnuel
from services.sauvegarde import Sauvegarde

Window.size = (1100, 720)


class ComptoirQuizLayout(BoxLayout):
    def __init__(self, cafe: Cafe, chemin_local: str = "data/donnees_cafe.json", **kwargs):
        super().__init__(orientation="vertical", padding=12, spacing=10, **kwargs)
        self.__cafe = cafe
        self.__sauvegarde = Sauvegarde()
        self.__chemin_local = chemin_local
        self.__classement_visible = True

        self.__charger_donnees_locales()
        self.__construire_interface()
        self.__afficher_accueil()

    # --- Persistance locale automatique (ENF-03) ---

    def __charger_donnees_locales(self) -> None:
        if os.path.isfile(self.__chemin_local):
            try:
                contenu = self.__sauvegarde.importer_donnees(self.__chemin_local)
                self.__cafe.restaurer_etat(contenu)
            except Exception as e:
                print(f"[Avertissement] Chargement local impossible : {e}")

    def __sauvegarder_auto(self) -> None:
        dossier = os.path.dirname(self.__chemin_local)
        if dossier and not os.path.exists(dossier):
            os.makedirs(dossier)
        with open(self.__chemin_local, "w", encoding="utf-8") as f:
            f.write(self.__cafe.serialiser_etat())
        self.__rafraichir_entete()

    def __equipe_par_nom(self, soiree: SoireeQuiz, nom: str):
        nom_clean = nom.strip().lower()
        if not nom_clean:
            raise ValueError("Indiquez le nom de l'équipe.")
        for equipe in soiree.equipes:
            if equipe.nom_soiree.lower() == nom_clean:
                return equipe
        raise ValueError(f"Aucune équipe nommée « {nom.strip()} » dans cette soirée.")

    def __obtenir_soiree_active(self) -> SoireeQuiz:
        for s in self.__cafe.soirees:
            if s.en_cours:
                return s
        return None

    # --- Structure principale de la fenêtre ---

    def __construire_interface(self) -> None:
        # Bandeau supérieur
        entete = BoxLayout(size_hint_y=None, height=55, spacing=10)
        self.__lbl_titre = Label(
            text=f"[b]{self.__cafe.nom.upper()}[/b]",
            markup=True,
            font_size="20sp",
            halign="left",
            valign="middle"
        )
        self.__lbl_titre.bind(size=self.__lbl_titre.setter("text_size"))

        self.__lbl_statut = Label(
            text="",
            markup=True,
            font_size="15sp",
            size_hint_x=None,
            width=360
        )

        btn_annuler = Button(
            text="Annuler dernière action (F-09)",
            size_hint_x=None,
            width=230,
            background_color=(0.75, 0.35, 0.15, 1)
        )
        btn_annuler.bind(on_press=self.__action_annuler)

        entete.add_widget(self.__lbl_titre)
        entete.add_widget(self.__lbl_statut)
        entete.add_widget(btn_annuler)
        self.add_widget(entete)

        # Corps : Menu latéral gauche + Zone de contenu droite
        corps = BoxLayout(spacing=12)

        menu_gauche = BoxLayout(orientation="vertical", size_hint_x=None, width=250, spacing=6)
        boutons_nav = [
            ("Tableau de bord", self.__afficher_accueil),
            ("F-01 : Équipes & Capitaines", self.__afficher_equipes),
            ("F-02 : Banque de Questions", self.__afficher_questions),
            ("F-03 : Organiser une Soirée", self.__afficher_organiser_soiree),
            ("F-04 / F-07 : Scores & Mises", self.__afficher_scores),
            ("Clôturer la soirée (RM-13)", self.__afficher_cloture),
            ("F-05 : Historique Soirées", self.__afficher_historique),
            ("F-06 : Championnat Annuel", self.__afficher_championnat),
            ("F-08 : Sauvegarde USB", self.__afficher_sauvegarde),
        ]
        for libelle, callback in boutons_nav:
            btn = Button(text=libelle, font_size="14sp")
            btn.bind(on_press=lambda _, cb=callback: cb())
            menu_gauche.add_widget(btn)

        self.__zone_contenu = BoxLayout(orientation="vertical", padding=10, spacing=8)

        corps.add_widget(menu_gauche)
        corps.add_widget(self.__zone_contenu)
        self.add_widget(corps)

        # Barre de notification en bas
        self.__lbl_message = Label(
            text="Prêt.",
            size_hint_y=None,
            height=34,
            font_size="14sp",
            color=(0.3, 0.9, 0.4, 1)
        )
        self.add_widget(self.__lbl_message)
        self.__rafraichir_entete()

    def __rafraichir_entete(self) -> None:
        soiree = self.__obtenir_soiree_active()
        if soiree:
            self.__lbl_statut.text = f"[color=44ff66]Soirée EN COURS ({soiree.date.isoformat()})[/color]"
        else:
            self.__lbl_statut.text = "[color=cccccc]Aucune soirée active[/color]"

    def __notifier(self, texte: str, erreur: bool = False) -> None:
        self.__lbl_message.color = (1, 0.35, 0.35, 1) if erreur else (0.3, 0.95, 0.45, 1)
        self.__lbl_message.text = texte

    def __vider_contenu(self, titre_section: str) -> None:
        self.__zone_contenu.clear_widgets()
        titre = Label(
            text=f"[b]{titre_section}[/b]",
            markup=True,
            font_size="18sp",
            size_hint_y=None,
            height=38
        )
        self.__zone_contenu.add_widget(titre)

    def __action_annuler(self, _) -> None:
        try:
            self.__cafe.restaurer_etat_precedent()
            self.__sauvegarder_auto()
            self.__notifier("Dernière modification annulée (RM-15).")
            self.__afficher_accueil()
        except Exception as e:
            self.__notifier(str(e), erreur=True)

    # --- Écran 0 : Tableau de bord ---

    def __afficher_accueil(self) -> None:
        self.__vider_contenu("TABLEAU DE BORD")
        soiree = self.__obtenir_soiree_active()

        resume = (
            f"Capitaines enregistrés : {len(self.__cafe.capitaines)}\n"
            f"Questions en banque : {len(self.__cafe.questions)}\n"
            f"Soirées archivées : {len(self.__cafe.soirees)}\n"
        )
        if soiree:
            resume += (
                f"\nSoirée active du {soiree.date.isoformat()} : "
                f"{len(soiree.equipes)} équipe(s) inscrite(s), "
                f"{len(soiree.manches)} manche(s) configurée(s)."
            )

        lbl = Label(text=resume, font_size="16sp", halign="center")
        self.__zone_contenu.add_widget(lbl)

    # --- F-01 : Gestion des équipes ---

    def __afficher_equipes(self) -> None:
        self.__vider_contenu("F-01 : INSCRIPTION D'UNE ÉQUIPE")

        grille = GridLayout(cols=2, spacing=8, size_hint_y=None, height=230)
        in_nom_cap = TextInput(hint_text="Nom du capitaine", multiline=False)
        in_prenom_cap = TextInput(hint_text="Prénom du capitaine", multiline=False)
        in_tel = TextInput(hint_text="Téléphone (si nouveau capitaine)", multiline=False)
        in_nom_eq = TextInput(hint_text="Nom de l'équipe pour ce soir", multiline=False)
        in_nb = TextInput(hint_text="Nombre de joueurs (min 1)", text="4", input_filter="int", multiline=False)

        grille.add_widget(Label(text="Nom du capitaine :"))
        grille.add_widget(in_nom_cap)
        grille.add_widget(Label(text="Prénom du capitaine :"))
        grille.add_widget(in_prenom_cap)
        grille.add_widget(Label(text="Téléphone :"))
        grille.add_widget(in_tel)
        grille.add_widget(Label(text="Nom de l'équipe ce soir :"))
        grille.add_widget(in_nom_eq)
        grille.add_widget(Label(text="Nombre de participants :"))
        grille.add_widget(in_nb)

        self.__zone_contenu.add_widget(grille)

        soiree_active = self.__obtenir_soiree_active()
        if soiree_active is None:
            self.__zone_contenu.add_widget(Label(
                text="Aucune soirée en cours. Créez-en une dans F-03 avant d'inscrire une équipe.",
                size_hint_y=None,
                height=36
            ))

        btn_valider = Button(text="Créer et inscrire l'équipe", size_hint_y=None, height=45)

        def valider(_):
            try:
                soiree = self.__obtenir_soiree_active()
                if soiree is None:
                    raise ValueError(
                        "Aucune soirée en cours. Organisez d'abord une soirée (F-03) : l'équipe doit y être inscrite."
                    )

                nom_c = in_nom_cap.text.strip()
                prenom_c = in_prenom_cap.text.strip()
                cap = self.__cafe.rechercher_capitaine(nom_c, prenom_c)
                if cap is not None and any(eq.capitaine.id == cap.id for eq in soiree.equipes):
                    raise ValueError("Ce capitaine a déjà une équipe inscrite ce soir.")
                if cap is None:
                    cap = self.__cafe.creer_capitaine(nom_c, prenom_c, in_tel.text.strip())

                nb_p = int(in_nb.text or "1")
                equipe = self.__cafe.creer_equipe(cap, in_nom_eq.text.strip(), nb_p)
                soiree.inscrire_equipe(equipe)

                self.__sauvegarder_auto()
                self.__notifier(f"Équipe '{equipe.nom_soiree}' enregistrée (Capitaine : {cap.prenom} {cap.nom}).")
                self.__afficher_equipes()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        btn_valider.bind(on_press=valider)
        self.__zone_contenu.add_widget(btn_valider)

        # Liste des équipes de la soirée active
        soiree = self.__obtenir_soiree_active()
        if soiree and soiree.equipes:
            texte_eq = "Équipes inscrites ce soir :\n" + "\n".join(
                f"• {eq.nom_soiree} ({eq.nb_participants} joueurs) - Cap. {eq.capitaine.prenom} {eq.capitaine.nom}"
                for eq in soiree.equipes
            )
            self.__zone_contenu.add_widget(Label(text=texte_eq, font_size="14sp"))

    # --- F-02 : Banque de questions ---

    def __afficher_questions(self) -> None:
        self.__vider_contenu("F-02 : BANQUE DE QUESTIONS")

        grille = GridLayout(cols=2, spacing=6, size_hint_y=None, height=175)
        in_enonce = TextInput(hint_text="Énoncé de la question", multiline=False)
        in_reponse = TextInput(hint_text="Réponse attendue", multiline=False)
        in_theme = TextInput(hint_text="Thème (ex: Histoire, Cinéma)", multiline=False)
        in_diff = TextInput(hint_text="Difficulté (1, 2 ou 3)", text="1", input_filter="int", multiline=False)

        grille.add_widget(Label(text="Énoncé :"))
        grille.add_widget(in_enonce)
        grille.add_widget(Label(text="Réponse :"))
        grille.add_widget(in_reponse)
        grille.add_widget(Label(text="Thème :"))
        grille.add_widget(in_theme)
        grille.add_widget(Label(text="Difficulté (1-3) :"))
        grille.add_widget(in_diff)
        self.__zone_contenu.add_widget(grille)

        barre_actions = BoxLayout(size_hint_y=None, height=42, spacing=8)
        btn_ajouter = Button(text="Ajouter la question")
        in_fichier = TextInput(hint_text="Chemin fichier .csv ou .json")
        btn_importer = Button(text="Importer fichier", size_hint_x=None, width=160)

        def ajouter(_):
            try:
                q = Question(in_enonce.text, in_reponse.text, in_theme.text, int(in_diff.text or "1"))
                self.__cafe.ajouter_question(q)
                self.__sauvegarder_auto()
                self.__notifier(f"Question '{q.id}' ajoutée.")
                self.__afficher_questions()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        def importer(_):
            try:
                self.__cafe.importer_questions(in_fichier.text.strip())
                self.__sauvegarder_auto()
                self.__notifier("Importation des questions terminée.")
                self.__afficher_questions()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        btn_ajouter.bind(on_press=ajouter)
        btn_importer.bind(on_press=importer)
        barre_actions.add_widget(btn_ajouter)
        barre_actions.add_widget(in_fichier)
        barre_actions.add_widget(btn_importer)
        self.__zone_contenu.add_widget(barre_actions)

        soiree_active = self.__obtenir_soiree_active()
        in_manche_posee = TextInput(text="1", input_filter="int", multiline=False, size_hint_x=None, width=70)
        if soiree_active is not None:
            barre_posee = BoxLayout(size_hint_y=None, height=36, spacing=8)
            barre_posee.add_widget(Label(
                text="Pour appliquer le délai d'un an, indiquez la manche où la question est posée ce soir :",
                font_size="13sp"
            ))
            barre_posee.add_widget(in_manche_posee)
            self.__zone_contenu.add_widget(barre_posee)

        # Liste défilante des questions
        scroll = ScrollView()
        liste_box = BoxLayout(orientation="vertical", size_hint_y=None, spacing=4)
        liste_box.bind(minimum_height=liste_box.setter("height"))

        aujourd_hui = date.today()
        for q in self.__cafe.questions:
            ligne = BoxLayout(size_hint_y=None, height=36, spacing=6)
            dispo = "DISPO" if q.est_disponible(aujourd_hui) else "BLOQUÉE (<1 an)"
            lbl_q = Label(
                text=f"[{q.id}] ({q.theme} | Niv.{q.niveau_difficulte} | {dispo}) {q.enonce}",
                font_size="13sp",
                halign="left"
            )
            lbl_q.bind(size=lbl_q.setter("text_size"))
            btn_suppr = Button(text="Supprimer", size_hint_x=None, width=100)
            btn_suppr.bind(on_press=lambda _, q_id=q.id: self.__supprimer_question(q_id))
            ligne.add_widget(lbl_q)
            if soiree_active is not None and q.est_disponible(soiree_active.date):
                btn_posee = Button(text="Posée ce soir", size_hint_x=None, width=130)
                btn_posee.bind(on_press=lambda _, q_id=q.id, champ=in_manche_posee: self.__poser_question(q_id, champ.text))
                ligne.add_widget(btn_posee)
            ligne.add_widget(btn_suppr)
            liste_box.add_widget(ligne)

        scroll.add_widget(liste_box)
        self.__zone_contenu.add_widget(scroll)

    def __poser_question(self, q_id: str, numero_manche: str) -> None:
        try:
            soiree = self.__obtenir_soiree_active()
            if soiree is None:
                raise ValueError("Aucune soirée en cours. Une question n'est marquée utilisée que lorsqu'elle est posée.")
            question = next((q for q in self.__cafe.questions if q.id == q_id), None)
            if question is None:
                raise ValueError("Question introuvable.")
            manche = soiree.obtenir_manche(int(numero_manche or "1"))
            self.__cafe.sauvegarder_etat_temporaire()
            manche.poser_question(question, soiree.date)
            self.__sauvegarder_auto()
            self.__notifier("Question marquée comme posée. Elle ne pourra pas revenir avant un an (RM-05).")
            self.__afficher_questions()
        except Exception as e:
            self.__notifier(str(e), erreur=True)

    def __supprimer_question(self, q_id: str) -> None:
        try:
            self.__cafe.supprimer_question(q_id)
            self.__sauvegarder_auto()
            self.__notifier(f"Question {q_id} supprimée.")
            self.__afficher_questions()
        except Exception as e:
            self.__notifier(str(e), erreur=True)

    # --- F-03 : Organiser une soirée ---

    def __afficher_organiser_soiree(self) -> None:
        self.__vider_contenu("F-03 : ORGANISER UNE NOUVELLE SOIRÉE")

        grille = GridLayout(cols=2, spacing=8, size_hint_y=None, height=150)
        in_manches = TextInput(text="6", input_filter="int", multiline=False)
        in_questions = TextInput(text="8", input_filter="int", multiline=False)
        in_miser = TextInput(text="6", input_filter="int", multiline=False)

        grille.add_widget(Label(text="Nombre de manches :"))
        grille.add_widget(in_manches)
        grille.add_widget(Label(text="Questions par manche :"))
        grille.add_widget(in_questions)
        grille.add_widget(Label(text="Numéro manche à miser (0 = aucune) :"))
        grille.add_widget(in_miser)
        self.__zone_contenu.add_widget(grille)

        btn_creer = Button(text="Lancer la soirée du jour", size_hint_y=None, height=48)

        def creer(_):
            try:
                if self.__cafe.a_soiree_en_cours():
                    raise ValueError("Une soirée est déjà en cours.")
                nb_m = int(in_manches.text or "6")
                nb_q = int(in_questions.text or "8")
                num_miser = int(in_miser.text or "0")

                soiree = SoireeQuiz.creer_soiree(date.today(), nb_m, nb_q)
                for i in range(1, nb_m + 1):
                    soiree.ajouter_manche(Manche(i, est_a_miser=(i == num_miser)))

                self.__cafe.ajouter_soiree(soiree)
                self.__sauvegarder_auto()
                self.__notifier("Nouvelle soirée créée ! Inscrivez les équipes dans F-01.")
                self.__afficher_accueil()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        btn_creer.bind(on_press=creer)
        self.__zone_contenu.add_widget(btn_creer)

    # --- F-04 & F-07 : Scores, manches à miser et classement ---

    def __afficher_scores(self) -> None:
        self.__vider_contenu("F-04 / F-07 : ENCODAGE DES SCORES ET CLASSEMENT")
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            self.__zone_contenu.add_widget(Label(text="Aucune soirée en cours."))
            return

        # Barre de contrôle supérieure
        barre = BoxLayout(size_hint_y=None, height=42, spacing=8)
        in_num_manche = TextInput(hint_text="N° Manche", text="1", input_filter="int", size_hint_x=None, width=110)
        chk_miser = CheckBox(size_hint_x=None, width=40)
        lbl_miser = Label(text="Manche à miser", size_hint_x=None, width=130)

        btn_visibilite = Button(
            text="Masquer classement" if self.__classement_visible else "Afficher classement"
        )

        def basculer_visibilite(_):
            self.__classement_visible = not self.__classement_visible
            self.__afficher_scores()

        btn_visibilite.bind(on_press=basculer_visibilite)
        barre.add_widget(Label(text="Manche :", size_hint_x=None, width=80))
        barre.add_widget(in_num_manche)
        barre.add_widget(chk_miser)
        barre.add_widget(lbl_miser)
        barre.add_widget(btn_visibilite)
        self.__zone_contenu.add_widget(barre)

        # Saisie par équipe
        scroll = ScrollView(size_hint_y=0.55)
        grille_saisie = GridLayout(cols=4, spacing=6, size_hint_y=None)
        grille_saisie.bind(minimum_height=grille_saisie.setter("height"))

        champs_equipes = []
        for eq in soiree.equipes:
            lbl_eq = Label(text=f"{eq.nom_soiree}", size_hint_y=None, height=36)
            in_pts = TextInput(hint_text="Pts ou Mise (1-5)", input_filter="int", size_hint_y=None, height=36)
            chk_ok = CheckBox(active=True, size_hint_y=None, height=36)
            lbl_ok = Label(text="Bonne rép. (si mise)", size_hint_y=None, height=36)

            grille_saisie.add_widget(lbl_eq)
            grille_saisie.add_widget(in_pts)
            grille_saisie.add_widget(chk_ok)
            grille_saisie.add_widget(lbl_ok)
            champs_equipes.append((eq, in_pts, chk_ok))

        scroll.add_widget(grille_saisie)
        self.__zone_contenu.add_widget(scroll)

        btn_enregistrer = Button(text="Valider les scores de la manche", size_hint_y=None, height=44)

        def enregistrer(_):
            try:
                num_m = int(in_num_manche.text)
                manche_cible = next((m for m in soiree.manches if m.numero == num_m), None)
                if manche_cible is None:
                    raise ValueError(f"Manche {num_m} introuvable.")

                self.__cafe.sauvegarder_etat_temporaire()
                for eq, in_pts, chk_ok in champs_equipes:
                    if not in_pts.text.strip():
                        continue
                    val = int(in_pts.text)
                    if manche_cible.est_a_miser or chk_miser.active:
                        manche_cible.enregistrer_score(eq, 0, val, chk_ok.active)
                    else:
                        soiree.enregistrer_score_equipe(eq, num_m, val)

                self.__sauvegarder_auto()
                self.__notifier(f"Scores de la manche {num_m} enregistrés.")
                self.__afficher_scores()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        btn_enregistrer.bind(on_press=enregistrer)
        self.__zone_contenu.add_widget(btn_enregistrer)

        # Affichage du classement temps réel (EF-04.3)
        if self.__classement_visible:
            classement = soiree.calculer_classement_soiree()
            lignes = ["CLASSEMENT ACTUEL :"]
            for rang, eq in enumerate(classement, start=1):
                sub = " [Subsidiaire]" if eq.vainqueur_subsidiaire else ""
                lignes.append(f"{rang}. {eq.nom_soiree} — {eq.calculer_score_total()} pts{sub}")
            self.__zone_contenu.add_widget(Label(text="\n".join(lignes), font_size="15sp"))
        else:
            self.__zone_contenu.add_widget(Label(text="[Classement masqué avant la fin du quiz]"))

    # --- Clôture de soirée ---

    def __afficher_cloture(self) -> None:
        self.__vider_contenu("CLÔTURE DE LA SOIRÉE ET ATTRIBUTION DES POINTS")
        soiree = self.__obtenir_soiree_active()
        if soiree is None:
            self.__zone_contenu.add_widget(Label(text="Aucune soirée active à clôturer."))
            return

        classement = soiree.calculer_classement_soiree()
        texte = "Classement prêt à être figé :\n\n" + "\n".join(
            f"{i}. {eq.nom_soiree} ({eq.capitaine.prenom} {eq.capitaine.nom}) : {eq.calculer_score_total()} pts -> +{max(5, 20 - 2*(i-1))} pts championnat"
            for i, eq in enumerate(classement, start=1)
        )
        self.__zone_contenu.add_widget(Label(text=texte, font_size="15sp"))

        btn_cloturer = Button(text="Clôturer définitivement la soirée", size_hint_y=None, height=48)

        def cloturer(_):
            try:
                self.__cafe.sauvegarder_etat_temporaire()
                soiree.cloturer_soiree()
                self.__sauvegarder_auto()
                self.__notifier("Soirée clôturée ! Pensez à effectuer une sauvegarde USB (RM-14).")
                self.__afficher_accueil()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        btn_cloturer.bind(on_press=cloturer)
        self.__zone_contenu.add_widget(btn_cloturer)

    # --- F-05 : Historique ---

    def __afficher_historique(self) -> None:
        self.__vider_contenu("F-05 : HISTORIQUE DES SOIRÉES")

        barre = BoxLayout(size_hint_y=None, height=42, spacing=8)
        in_critere = TextInput(text="date", hint_text="date / equipe / capitaine", size_hint_x=None, width=160)
        in_valeur = TextInput(hint_text="Valeur recherchée (ex: 2026-11)")
        btn_chercher = Button(text="Rechercher", size_hint_x=None, width=140)
        barre.add_widget(in_critere)
        barre.add_widget(in_valeur)
        barre.add_widget(btn_chercher)
        self.__zone_contenu.add_widget(barre)

        lbl_resultats = Label(text="Saisissez un critère pour filtrer les soirées.", font_size="14sp")
        self.__zone_contenu.add_widget(lbl_resultats)

        def rechercher(_):
            soirees = self.__cafe.rechercher_soirees(in_critere.text, in_valeur.text)
            if not soirees:
                lbl_resultats.text = "Aucune soirée trouvée."
                return
            blocs = []
            for s in soirees:
                cl = s.calculer_classement_soiree()
                podium = ", ".join(f"{eq.nom_soiree} ({eq.calculer_score_total()} pts)" for eq in cl)
                blocs.append(f"• Soirée du {s.date.isoformat()} : {podium}")
            lbl_resultats.text = "\n".join(blocs)

        btn_chercher.bind(on_press=rechercher)

    # --- F-06 : Championnat annuel ---

    def __afficher_championnat(self) -> None:
        annee = date.today().year
        self.__vider_contenu(f"F-06 : CHAMPIONNAT ANNUEL {annee} (TOP 10)")

        champ = ChampionnatAnnuel(annee, self.__cafe.capitaines)
        classement = champ.calculer_classement_annuel()

        if not classement:
            self.__zone_contenu.add_widget(Label(text="Aucun capitaine classé pour le moment."))
            return

        lignes = [
            f"{rang}. {cap.prenom} {cap.nom} — {cap.calculer_points_top10()} pts ({len(cap.points_soirees)} soirées jouées)"
            for rang, cap in enumerate(classement, start=1)
        ]
        self.__zone_contenu.add_widget(Label(text="\n".join(lignes), font_size="15sp"))

        btn_reset = Button(text="Clôturer la saison et réinitialiser les points", size_hint_y=None, height=45)

        def reset(_):
            try:
                gagnant = champ.determiner_gagnant()
                self.__cafe.sauvegarder_etat_temporaire()
                champ.reinitialiser_points()
                self.__sauvegarder_auto()
                nom_g = f"{gagnant.prenom} {gagnant.nom}" if gagnant else "Aucun"
                self.__notifier(f"Saison clôturée (Vainqueur : {nom_g}). Points remis à zéro.")
                self.__afficher_championnat()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        btn_reset.bind(on_press=reset)
        self.__zone_contenu.add_widget(btn_reset)

    # --- F-08 : Sauvegarde / Restauration USB ---

    def __afficher_sauvegarde(self) -> None:
        self.__vider_contenu("F-08 : SAUVEGARDE ET RESTAURATION USB")

        grille = GridLayout(cols=2, spacing=8, size_hint_y=None, height=110)
        in_usb = TextInput(hint_text="Dossier clé USB (ex: E:\\ ou /media/usb)", multiline=False)
        in_fichier = TextInput(hint_text="Chemin complet du fichier .json à restaurer", multiline=False)

        grille.add_widget(Label(text="Chemin clé USB :"))
        grille.add_widget(in_usb)
        grille.add_widget(Label(text="Fichier à restaurer :"))
        grille.add_widget(in_fichier)
        self.__zone_contenu.add_widget(grille)

        barre = BoxLayout(size_hint_y=None, height=46, spacing=10)
        btn_export = Button(text="Exporter sur clé USB")
        btn_import = Button(text="Restaurer depuis fichier")

        def exporter(_):
            try:
                self.__sauvegarde.exporter_donnees(self.__cafe, in_usb.text.strip())
                self.__notifier("Sauvegarde exportée avec succès sur la clé USB.")
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        def importer(_):
            try:
                donnees = self.__sauvegarde.importer_donnees(in_fichier.text.strip())
                self.__cafe.sauvegarder_etat_temporaire()
                self.__cafe.restaurer_etat(donnees)
                self.__sauvegarder_auto()
                self.__notifier("Données restaurées avec succès.")
                self.__afficher_accueil()
            except Exception as e:
                self.__notifier(str(e), erreur=True)

        btn_export.bind(on_press=exporter)
        btn_import.bind(on_press=importer)
        barre.add_widget(btn_export)
        barre.add_widget(btn_import)
        self.__zone_contenu.add_widget(barre)


class ComptoirQuizApp(App):
    def build(self):
        self.title = "Le Comptoir des Curieux - Gestion Quiz"
        cafe = Cafe("Le Comptoir des Curieux")
        return ComptoirQuizLayout(cafe)