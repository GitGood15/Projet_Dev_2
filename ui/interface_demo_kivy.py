"""Interface graphique Kivy réduite pour une démonstration du quiz."""

import os
from datetime import date

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput

from models.cafe import Cafe
from models.manche import Manche
from models.soiree_quiz import SoireeQuiz


class DemoQuizLayout(BoxLayout):
    def __init__(self, cafe: Cafe, chemin_local: str = "data/donnees_cafe.json", **kwargs):
        super().__init__(orientation="vertical", padding=16, spacing=10, **kwargs)
        self.__cafe = cafe
        self.__chemin_local = chemin_local
        self.__message = "Prêt."
        self.__message_erreur = False

        self.__charger_donnees_locales()
        self.__construire_interface()
        self.__afficher_accueil()

    def __charger_donnees_locales(self) -> None:
        if not os.path.isfile(self.__chemin_local):
            return
        try:
            with open(self.__chemin_local, "r", encoding="utf-8") as fichier:
                donnees = fichier.read()
            if not donnees.strip():
                self.__message = "Fichier de données vide : démarrage avec des données vierges."
                return
            self.__cafe.restaurer_etat(donnees)
        except (OSError, ValueError, KeyError, TypeError) as erreur:
            self.__message = f"Chargement local impossible : {erreur}"
            self.__message_erreur = True

    def __sauvegarder_auto(self) -> None:
        dossier = os.path.dirname(self.__chemin_local)
        if dossier:
            os.makedirs(dossier, exist_ok=True)
        with open(self.__chemin_local, "w", encoding="utf-8") as fichier:
            fichier.write(self.__cafe.serialiser_etat())

    def __soiree_active(self) -> SoireeQuiz | None:
        return next((soiree for soiree in self.__cafe.soirees if soiree.en_cours), None)

    def __construire_interface(self) -> None:
        entete = BoxLayout(size_hint_y=None, height=54, spacing=12)
        titre = Label(
            text=f"[b]{self.__cafe.nom} — DÉMO QUIZ[/b]",
            markup=True,
            font_size="22sp",
            halign="left",
            valign="middle",
        )
        titre.bind(size=titre.setter("text_size"))
        self.__statut = Label(text="", size_hint_x=None, width=260, font_size="15sp")
        entete.add_widget(titre)
        entete.add_widget(self.__statut)
        self.add_widget(entete)

        navigation = BoxLayout(size_hint_y=None, height=44, spacing=8)
        for texte, callback in (
            ("Accueil", self.__afficher_accueil),
            ("Créer soirée", self.__afficher_creation),
            ("Équipes", self.__afficher_equipes),
            ("Scores", self.__afficher_scores),
            ("Classement", self.__afficher_classement),
            ("Terminer soirée", self.__afficher_fin_soiree),
        ):
            bouton = Button(text=texte)
            bouton.bind(on_press=lambda _, action=callback: action())
            navigation.add_widget(bouton)
        self.add_widget(navigation)

        self.__contenu = BoxLayout(orientation="vertical", padding=12, spacing=10)
        self.add_widget(self.__contenu)

        self.__notification = Label(
            text=self.__message,
            size_hint_y=None,
            height=32,
            halign="left",
        )
        self.__notification.bind(size=self.__notification.setter("text_size"))
        self.__notification.color = (1, 0.35, 0.35, 1) if self.__message_erreur else (0.25, 0.8, 0.4, 1)
        self.add_widget(self.__notification)
        self.__rafraichir_entete()

    def __rafraichir_entete(self) -> None:
        soiree = self.__soiree_active()
        self.__statut.text = (
            f"Soirée active · {soiree.date:%d/%m/%Y}" if soiree else "Aucune soirée active"
        )

    def __notifier(self, texte: str, erreur: bool = False) -> None:
        self.__notification.text = texte
        self.__notification.color = (1, 0.35, 0.35, 1) if erreur else (0.25, 0.8, 0.4, 1)

    def __vider_contenu(self, titre: str) -> None:
        self.__contenu.clear_widgets()
        self.__contenu.add_widget(
            Label(
                text=f"[b]{titre}[/b]",
                markup=True,
                font_size="19sp",
                size_hint_y=None,
                height=38,
            )
        )

    @staticmethod
    def __champ(placeholder: str, valeur: str = "", numerique: bool = False) -> TextInput:
        return TextInput(
            hint_text=placeholder,
            text=valeur,
            input_filter="int" if numerique else None,
            multiline=False,
        )

    @staticmethod
    def __ajouter_champ(grille: GridLayout, libelle: str, champ: TextInput) -> None:
        grille.add_widget(Label(text=libelle, halign="left"))
        grille.add_widget(champ)

    @staticmethod
    def __entier(champ: TextInput, libelle: str, minimum: int, maximum: int | None = None) -> int:
        try:
            valeur = int(champ.text)
        except ValueError as erreur:
            raise ValueError(f"{libelle} doit être un nombre entier.") from erreur
        if valeur < minimum or (maximum is not None and valeur > maximum):
            limite = f"entre {minimum} et {maximum}" if maximum is not None else f"au moins {minimum}"
            raise ValueError(f"{libelle} doit être {limite}.")
        return valeur

    def __afficher_accueil(self) -> None:
        self.__vider_contenu("PARCOURS DE DÉMONSTRATION")
        soiree = self.__soiree_active()
        texte = (
            "Créez une soirée, inscrivez les équipes, saisissez les scores puis consultez le classement."
        )
        if soiree:
            texte += (
                f"\n\nSoirée du {soiree.date:%d/%m/%Y} · {len(soiree.manches)} manche(s) · "
                f"{len(soiree.equipes)} équipe(s)"
            )
        self.__contenu.add_widget(Label(text=texte, font_size="17sp", halign="left"))
        self.__rafraichir_entete()

    def __afficher_creation(self) -> None:
        self.__vider_contenu("CRÉER UNE SOIRÉE")
        if self.__cafe.a_soiree_en_cours():
            self.__contenu.add_widget(Label(text="Une soirée est déjà en cours."))
            return

        grille = GridLayout(cols=2, spacing=10, size_hint_y=None, height=120)
        manches = self.__champ("Nombre de manches", "3", numerique=True)
        questions = self.__champ("Questions par manche", "5", numerique=True)
        self.__ajouter_champ(grille, "Nombre de manches :", manches)
        self.__ajouter_champ(grille, "Questions par manche :", questions)
        self.__contenu.add_widget(grille)

        bouton = Button(text="Créer la soirée", size_hint_y=None, height=48)

        def creer(_):
            try:
                nb_manches = self.__entier(manches, "Le nombre de manches", 1)
                nb_questions = self.__entier(questions, "Le nombre de questions", 1)
                soiree = SoireeQuiz.creer_soiree(date.today(), nb_manches, nb_questions)
                for numero in range(1, nb_manches + 1):
                    soiree.ajouter_manche(Manche(numero, False))
                self.__cafe.ajouter_soiree(soiree)
                self.__sauvegarder_auto()
                self.__rafraichir_entete()
                self.__notifier("Soirée créée. Vous pouvez inscrire les équipes.")
                self.__afficher_equipes()
            except (ValueError, OSError, KeyError, TypeError) as erreur:
                self.__notifier(str(erreur), erreur=True)

        bouton.bind(on_press=creer)
        self.__contenu.add_widget(bouton)

    def __afficher_equipes(self) -> None:
        self.__vider_contenu("INSCRIRE UNE ÉQUIPE")
        soiree = self.__soiree_active()
        if soiree is None:
            self.__contenu.add_widget(Label(text="Créez d'abord une soirée pour inscrire des équipes."))
            return

        grille = GridLayout(cols=2, spacing=8, size_hint_y=None, height=245)
        nom_capitaine = self.__champ("Nom du capitaine")
        prenom_capitaine = self.__champ("Prénom du capitaine")
        telephone = self.__champ("Facultatif")
        nom_equipe = self.__champ("Nom de l'équipe")
        participants = self.__champ("4", "4", numerique=True)
        for libelle, champ in (
            ("Nom du capitaine :", nom_capitaine),
            ("Prénom du capitaine :", prenom_capitaine),
            ("Téléphone (facultatif) :", telephone),
            ("Nom de l'équipe :", nom_equipe),
            ("Nombre de participants :", participants),
        ):
            self.__ajouter_champ(grille, libelle, champ)
        self.__contenu.add_widget(grille)

        bouton = Button(text="Inscrire l'équipe", size_hint_y=None, height=46)

        def inscrire(_):
            try:
                nom = nom_capitaine.text.strip()
                prenom = prenom_capitaine.text.strip()
                nom_eq = nom_equipe.text.strip()
                if not nom or not prenom or not nom_eq:
                    raise ValueError("Le nom du capitaine, son prénom et le nom de l'équipe sont obligatoires.")
                nombre = self.__entier(participants, "Le nombre de participants", 1)
                capitaine = self.__cafe.rechercher_capitaine(nom, prenom)
                if capitaine is not None and any(
                    equipe.capitaine.id == capitaine.id for equipe in soiree.equipes
                ):
                    raise ValueError("Ce capitaine a déjà une équipe inscrite à cette soirée.")
                if capitaine is None:
                    capitaine = self.__cafe.creer_capitaine(nom, prenom, telephone.text.strip())
                equipe = self.__cafe.creer_equipe(capitaine, nom_eq, nombre)
                soiree.inscrire_equipe(equipe)
                self.__sauvegarder_auto()
                self.__notifier(f"Équipe « {equipe.nom_soiree} » inscrite.")
                self.__afficher_equipes()
            except (ValueError, OSError, KeyError, TypeError) as erreur:
                self.__notifier(str(erreur), erreur=True)

        self.__contenu.add_widget(bouton)
        bouton.bind(on_press=inscrire)

        liste = "\n".join(
            f"• {equipe.nom_soiree} — {equipe.nb_participants} participant(s)"
            for equipe in soiree.equipes
        )
        if liste:
            self.__contenu.add_widget(Label(text=f"Équipes inscrites :\n{liste}", halign="left"))

    def __afficher_scores(self) -> None:
        self.__vider_contenu("SAISIR LES SCORES")
        soiree = self.__soiree_active()
        if soiree is None:
            self.__contenu.add_widget(Label(text="Créez d'abord une soirée."))
            return
        if not soiree.equipes:
            self.__contenu.add_widget(Label(text="Inscrivez d'abord au moins une équipe."))
            return

        manches = [str(manche.numero) for manche in soiree.manches]
        selecteur = Spinner(
            text=manches[0],
            values=manches,
            size_hint_y=None,
            height=42,
        )
        self.__contenu.add_widget(Label(text="Choisissez la manche :", size_hint_y=None, height=30))
        self.__contenu.add_widget(selecteur)

        scroll = ScrollView()
        grille_scores = GridLayout(cols=2, spacing=8, size_hint_y=None)
        grille_scores.bind(minimum_height=grille_scores.setter("height"))
        champs: dict[str, TextInput] = {}

        def afficher_champs(_, numero_texte: str) -> None:
            grille_scores.clear_widgets()
            champs.clear()
            numero = int(numero_texte)
            manche = soiree.obtenir_manche(numero)
            for equipe in soiree.equipes:
                grille_scores.add_widget(Label(text=equipe.nom_soiree, halign="left", size_hint_y=None, height=42))
                score_existant = manche.score_pour(equipe)
                champ = self.__champ(
                    "Déjà saisi" if score_existant is not None else f"0 à {soiree.nb_questions_par_manche}",
                    str(score_existant.points_base) if score_existant is not None else "",
                    numerique=True,
                )
                champ.disabled = score_existant is not None
                champ.size_hint_y = None
                champ.height = 42
                champs[equipe.id] = champ
                grille_scores.add_widget(champ)

        selecteur.bind(text=afficher_champs)
        afficher_champs(selecteur, manches[0])
        scroll.add_widget(grille_scores)
        self.__contenu.add_widget(scroll)

        bouton = Button(text="Enregistrer les scores", size_hint_y=None, height=46)

        def enregistrer(_):
            try:
                numero = int(selecteur.text)
                valeurs = []
                for equipe in soiree.equipes:
                    manche = soiree.obtenir_manche(numero)
                    if manche.score_pour(equipe) is not None:
                        continue
                    champ = champs[equipe.id]
                    valeurs.append(
                        (equipe, self.__entier(champ, f"Le score de {equipe.nom_soiree}", 0, soiree.nb_questions_par_manche))
                    )
                if not valeurs:
                    raise ValueError("Les scores de cette manche ont déjà été saisis.")
                for equipe, points in valeurs:
                    soiree.enregistrer_score_equipe(equipe, numero, points)
                self.__sauvegarder_auto()
                self.__rafraichir_entete()
                self.__notifier("Scores enregistrés. Le classement a été mis à jour.")
                self.__afficher_classement()
            except (ValueError, OSError, KeyError, TypeError) as erreur:
                self.__notifier(str(erreur), erreur=True)

        bouton.bind(on_press=enregistrer)
        self.__contenu.add_widget(bouton)

    def __afficher_fin_soiree(self) -> None:
        self.__vider_contenu("TERMINER LA SOIRÉE")
        soiree = self.__soiree_active()
        if soiree is None:
            self.__contenu.add_widget(Label(text="Aucune soirée n'est en cours."))
            return

        self.__contenu.add_widget(
            Label(
                text=(
                    f"Terminer la soirée du {soiree.date:%d/%m/%Y} ?\n"
                    "Le classement sera figé et les points de championnat attribués."
                ),
                font_size="16sp",
            )
        )
        actions = BoxLayout(size_hint_y=None, height=48, spacing=10)
        annuler = Button(text="Annuler")
        confirmer = Button(text="Confirmer la fin de la soirée")
        annuler.bind(on_press=lambda _: self.__afficher_accueil())

        def terminer(_):
            try:
                soiree.cloturer_soiree()
                self.__sauvegarder_auto()
                self.__rafraichir_entete()
                self.__notifier("Soirée terminée et points de championnat attribués.")
                self.__afficher_classement(soiree)
            except (ValueError, OSError, KeyError, TypeError) as erreur:
                self.__notifier(str(erreur), erreur=True)

        confirmer.bind(on_press=terminer)
        actions.add_widget(annuler)
        actions.add_widget(confirmer)
        self.__contenu.add_widget(actions)

    def __afficher_classement(self, soiree: SoireeQuiz | None = None) -> None:
        self.__vider_contenu("CLASSEMENT")
        soiree = soiree or self.__soiree_active()
        if soiree is None:
            self.__contenu.add_widget(Label(text="Aucune soirée active."))
            return
        if not soiree.equipes:
            self.__contenu.add_widget(Label(text="Aucune équipe inscrite à cette soirée."))
            return

        self.__contenu.add_widget(Label(text=f"Soirée du {soiree.date:%d/%m/%Y}", size_hint_y=None, height=34))
        for rang, equipe in enumerate(soiree.calculer_classement_soiree(), start=1):
            ligne = BoxLayout(size_hint_y=None, height=48, spacing=12)
            ligne.add_widget(Label(text=f"{rang}.", size_hint_x=None, width=50))
            ligne.add_widget(Label(text=equipe.nom_soiree, halign="left"))
            ligne.add_widget(Label(text=f"{equipe.calculer_score_total()} point(s)", size_hint_x=None, width=160))
            self.__contenu.add_widget(ligne)


class DemoQuizKivyApp(App):
    def __init__(self, cafe: Cafe, **kwargs):
        super().__init__(**kwargs)
        self.__cafe = cafe

    def build(self):
        self.title = "Le Comptoir des Curieux — Démo Quiz"
        Window.size = (1000, 680)
        return DemoQuizLayout(self.__cafe)
