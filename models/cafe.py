import csv
import json
from datetime import date
from models.capitaine import Capitaine
from models.equipe import Equipe
from models.question import Question
from models.soiree_quiz import SoireeQuiz
from models.manche import Manche
from models.championnat_annuel import ChampionnatAnnuel


class Cafe:
    def __init__(self, nom: str = "Le Comptoir des Curieux"):
        self.__nom = nom
        self.__etat_precedent = None

        self.__soirees = []
        self.__capitaines = []
        self.__questions = []
        self.__championnats = []

    @property
    def nom(self) -> str:
        return self.__nom

    @property
    def soirees(self) -> list:
        return list(self.__soirees)

    @property
    def capitaines(self) -> list:
        return list(self.__capitaines)

    @property
    def questions(self) -> list:
        return list(self.__questions)

    @property
    def championnats(self) -> list:
        return list(self.__championnats)

    # --- Gestion des capitaines et équipes ---

    def rechercher_capitaine(self, nom: str, prenom: str) -> Capitaine:
        """Recherche un capitaine existant par nom et prénom."""
        nom_clean = nom.strip().lower()
        prenom_clean = prenom.strip().lower()
        for cap in self.__capitaines:
            if cap.nom.lower() == nom_clean and cap.prenom.lower() == prenom_clean:
                return cap
        return None

    def creer_capitaine(self, nom: str, prenom: str, tel: str) -> Capitaine:
        """Crée et enregistre un nouveau profil de capitaine."""
        if self.rechercher_capitaine(nom, prenom) is not None:
            raise ValueError(f"Le capitaine {prenom} {nom} est déjà enregistré.")

        self.sauvegarder_etat_temporaire()
        nouveau_cap = Capitaine(nom.strip(), prenom.strip(), tel.strip())
        self.__capitaines.append(nouveau_cap)
        return nouveau_cap

    def creer_equipe(self, cap: Capitaine, nom_soiree: str, nb_participants: int) -> Equipe:
        """Crée une équipe pour la soirée et l'associe à son capitaine."""
        if cap is None:
            raise ValueError("Un capitaine est obligatoire pour créer une équipe.")

        self.sauvegarder_etat_temporaire()
        equipe = Equipe(nom_soiree, nb_participants, cap)
        cap.associer_equipe(equipe)
        return equipe

    # --- Gestion et recherche des soirées ---

    def ajouter_soiree(self, soiree: SoireeQuiz) -> None:
        """Enregistre une soirée quiz dans l'historique du café."""
        if soiree is not None and soiree not in self.__soirees:
            self.sauvegarder_etat_temporaire()
            self.__soirees.append(soiree)

    def rechercher_soirees(self, critere: str, valeur: str) -> list:
        """Filtre les soirées selon la date, le nom d'équipe ou le capitaine."""
        resultats = []
        for s in self.__soirees:
            if s.correspond_critere(critere, valeur):
                resultats.append(s)
        return resultats

    def a_soiree_en_cours(self) -> bool:
        """Indique si une soirée quiz est actuellement active."""
        return any(s.en_cours for s in self.__soirees)

    # --- Gestion et importation des questions  ---

    def ajouter_question(self, q: Question) -> None:
        """Ajoute une question à la banque en dehors d'une partie."""
        if self.a_soiree_en_cours():
            raise ValueError("Impossible d'ajouter une question pendant qu'une partie est en cours.")
        if q is None:
            raise ValueError("La question ne peut pas être nulle.")

        self.sauvegarder_etat_temporaire()
        self.__questions.append(q)

    def supprimer_question(self, id: str) -> None:
        """Supprime une question de la banque en dehors d'une partie."""
        if self.a_soiree_en_cours():
            raise ValueError("Impossible de supprimer une question pendant qu'une partie est en cours.")

        for q in self.__questions:
            if q.id == id:
                self.sauvegarder_etat_temporaire()
                self.__questions.remove(q)
                return

        raise ValueError(f"Aucune question trouvée avec l'identifiant '{id}'.")

    def importer_questions(self, chemin_fichier: str) -> None:
        """Importe des questions depuis un fichier CSV ou JSON en dehors d'une partie."""
        if self.a_soiree_en_cours():
            raise ValueError("Impossible d'importer des questions pendant qu'une partie est en cours.")

        questions_importees = []

        if chemin_fichier.lower().endswith(".json"):
            with open(chemin_fichier, "r", encoding="utf-8") as f:
                donnees = json.load(f)
                for item in donnees:
                    q = Question(
                        enonce=item["enonce"],
                        reponse=item["reponse"],
                        theme=item.get("theme", "Général"),
                        niveau_difficulte=int(item["niveau_difficulte"])
                    )
                    questions_importees.append(q)
        else:
            # Lecture CSV (format standard exporté depuis Excel avec séparateur ';' ou ',')
            with open(chemin_fichier, "r", encoding="utf-8-sig") as f:
                premiere_ligne = f.readline()
                separateur = ";" if ";" in premiere_ligne else ","
                f.seek(0)
                lecteur = csv.DictReader(f, delimiter=separateur)
                for ligne in lecteur:
                    q = Question(
                        enonce=ligne["enonce"],
                        reponse=ligne["reponse"],
                        theme=ligne.get("theme", "Général"),
                        niveau_difficulte=int(ligne["niveau_difficulte"])
                    )
                    questions_importees.append(q)

        self.sauvegarder_etat_temporaire()
        self.__questions.extend(questions_importees)

    # --- Sérialisation, sauvegarde et annulation ---

    def serialiser_etat(self) -> str:
        """Sérialise l'ensemble des données du café au format JSON."""
        donnees = {
            "nom": self.__nom,
            "capitaines": [
                {
                    "id": c.id,
                    "nom": c.nom,
                    "prenom": c.prenom,
                    "telephone": c.telephone,
                    "points_soirees": c.points_soirees
                }
                for c in self.__capitaines
            ],
            "questions": [
                {
                    "id": q.id,
                    "enonce": q.enonce,
                    "reponse": q.reponse,
                    "theme": q.theme,
                    "niveau_difficulte": q.niveau_difficulte,
                    "derniere_utilisation": (
                        q.derniere_utilisation.isoformat() if q.derniere_utilisation else None
                    )
                }
                for q in self.__questions
            ],
            "soirees": [
                {
                    "date": s.date.isoformat(),
                    "nb_manches": s.nb_manches,
                    "nb_questions_par_manche": s.nb_questions_par_manche,
                    "en_cours": s.en_cours,
                    "equipes": [
                        {
                            "id": eq.id,
                            "nom_soiree": eq.nom_soiree,
                            "nb_participants": eq.nb_participants,
                            "vainqueur_subsidiaire": eq.vainqueur_subsidiaire,
                            "capitaine_id": eq.capitaine.id
                        }
                        for eq in s.equipes
                    ],
                    "manches": [
                        {
                            "numero": m.numero,
                            "est_a_miser": m.est_a_miser,
                            "questions_ids": [q.id for q in m.questions],
                            "scores": [
                                {
                                    "equipe_id": eq.id,
                                    "points_base": sc.points_base,
                                    "mise": sc.mise,
                                    "bonne_reponse_mise": sc.bonne_reponse_mise
                                }
                                for eq in s.equipes
                                for sc in m.scores
                                if sc in eq.scores
                            ]
                        }
                        for m in s.manches
                    ]
                }
                for s in self.__soirees
            ],
            "championnats": [
                {
                    "annee": ch.annee,
                    "capitaines_ids": [c.id for c in ch.capitaines]
                }
                for ch in self.__championnats
            ]
        }
        return json.dumps(donnees, ensure_ascii=False, indent=2)

    def restaurer_etat(self, donnees: str) -> None:
        """Reconstruit intégralement l'état du café depuis une chaîne JSON."""
        contenu = json.loads(donnees)
        self.__nom = contenu.get("nom", self.__nom)

        nouveaux_capitaines = []
        capitaines_par_id = {}
        for c_data in contenu.get("capitaines", []):
            cap = Capitaine(
                c_data["nom"], c_data["prenom"], c_data.get("telephone", ""), c_data.get("id")
            )
            for pts in c_data.get("points_soirees", []):
                cap.ajouter_points_championnat(pts)
            nouveaux_capitaines.append(cap)
            capitaines_par_id[c_data["id"]] = cap

        nouvelles_questions = []
        for q_data in contenu.get("questions", []):
            derniere_util = (
                date.fromisoformat(q_data["derniere_utilisation"])
                if q_data.get("derniere_utilisation") else None
            )
            q = Question(
                enonce=q_data["enonce"],
                reponse=q_data["reponse"],
                theme=q_data.get("theme", "Général"),
                niveau_difficulte=q_data["niveau_difficulte"],
                derniere_utilisation=derniere_util,
                id=q_data.get("id")
            )
            nouvelles_questions.append(q)
        questions_par_id = {q.id: q for q in nouvelles_questions}

        nouvelles_soirees = []
        for s_data in contenu.get("soirees", []):
            soiree = SoireeQuiz(
                date_soiree=date.fromisoformat(s_data["date"]),
                nb_manches=s_data["nb_manches"],
                nb_questions_par_manche=s_data["nb_questions_par_manche"],
                en_cours=s_data["en_cours"]
            )
            equipes_par_id = {}
            for eq_data in s_data.get("equipes", []):
                cap = capitaines_par_id.get(eq_data["capitaine_id"])
                if cap is not None:
                    eq = Equipe(
                        eq_data["nom_soiree"], eq_data["nb_participants"], cap, eq_data.get("id")
                    )
                    eq.definir_vainqueur_subsidiaire(eq_data.get("vainqueur_subsidiaire", False))
                    soiree.inscrire_equipe(eq)
                    equipes_par_id[eq.id] = eq

            for m_data in s_data.get("manches", []):
                manche = Manche(m_data["numero"], m_data["est_a_miser"])
                soiree.ajouter_manche(manche)
                for qid in m_data.get("questions_ids", []):
                    question = questions_par_id.get(qid)
                    if question is not None:
                        manche.lier_question(question)
                for sc_data in m_data.get("scores", []):
                    eq = equipes_par_id.get(sc_data["equipe_id"])
                    if eq is not None:
                        if manche.est_a_miser:
                            sc = manche.enregistrer_score(
                                eq, 0, sc_data["mise"], sc_data["bonne_reponse_mise"]
                            )
                            sc.modifier_points(sc_data["points_base"])
                        else:
                            manche.enregistrer_score(
                                eq, sc_data["points_base"], 0, sc_data["bonne_reponse_mise"]
                            )

            nouvelles_soirees.append(soiree)

        nouveaux_championnats = []
        for ch_data in contenu.get("championnats", []):
            caps_ch = [
                capitaines_par_id[cid]
                for cid in ch_data.get("capitaines_ids", [])
                if cid in capitaines_par_id
            ]
            nouveaux_championnats.append(ChampionnatAnnuel(ch_data["annee"], caps_ch))

        self.__capitaines = nouveaux_capitaines
        self.__questions = nouvelles_questions
        self.__soirees = nouvelles_soirees
        self.__championnats = nouveaux_championnats

    def sauvegarder_etat_temporaire(self) -> None:
        """Conserve une copie de l'état actuel avant toute modification."""
        self.__etat_precedent = self.serialiser_etat()

    def a_un_etat_precedent(self) -> bool:
        """Vérifie si une modification récente peut être annulée."""
        return self.__etat_precedent is not None

    def restaurer_etat_precedent(self) -> None:
        """Annule la dernière modification en rétablissant l'état précédent."""
        if not self.a_un_etat_precedent():
            raise ValueError("Aucune modification récente à annuler.")

        etat_a_restaurer = self.__etat_precedent
        self.__etat_precedent = None
        self.restaurer_etat(etat_a_restaurer)