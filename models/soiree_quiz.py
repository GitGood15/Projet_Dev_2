from datetime import date
from models.equipe import Equipe
from models.manche import Manche


class SoireeQuiz:
    def __init__(self, date_soiree: date, nb_manches: int, nb_questions_par_manche: int, en_cours: bool = True):
        if nb_manches < 1:
            raise ValueError("Une soirée doit comporter au moins 1 manche.")
        if nb_questions_par_manche < 1:
            raise ValueError("Une manche doit comporter au moins 1 question.")

        self.__date = date_soiree
        self.__nb_manches = nb_manches
        self.__nb_questions_par_manche = nb_questions_par_manche
        self.__en_cours = en_cours


        self.__manches = []
        self.__equipes = []

    @property
    def date(self) -> date:
        return self.__date

    @property
    def nb_manches(self) -> int:
        return self.__nb_manches

    @property
    def nb_questions_par_manche(self) -> int:
        return self.__nb_questions_par_manche

    @property
    def en_cours(self) -> bool:
        return self.__en_cours

    @property
    def manches(self) -> list:
        return list(self.__manches)

    @property
    def equipes(self) -> list:
        return list(self.__equipes)

    @classmethod
    def creer_soiree(cls, date_soiree: date, nb_manches: int, nb_questions: int) -> 'SoireeQuiz':
        """Méthode statique de fabrique d'une soirée quiz."""
        return cls(date_soiree, nb_manches, nb_questions, True)

    def inscrire_equipe(self, e: Equipe) -> None:
        """Inscrit une équipe à la soirée en empêchant les doublons."""
        if e is None:
            raise ValueError("L'équipe ne peut pas être nulle.")

        for equipe_existante in self.__equipes:
            if equipe_existante.id == e.id or equipe_existante.capitaine.id == e.capitaine.id:
                raise ValueError("Cette équipe ou ce capitaine est déjà inscrit à la soirée.")

        self.__equipes.append(e)

    def ajouter_manche(self, m: Manche) -> None:
        """Ajoute une manche à la soirée."""
        if m is None:
            raise ValueError("La manche ne peut pas être nulle.")
        if len(self.__manches) >= self.__nb_manches:
            raise ValueError("Le nombre maximum de manches configuré pour la soirée est atteint.")

        self.__manches.append(m)

    def enregistrer_score_equipe(self, e: Equipe, manche_num: int, pts: int) -> None:
        """Enregistre le score d'une équipe pour une manche donnée."""
        if e not in self.__equipes:
            raise ValueError("L'équipe n'est pas inscrite à cette soirée.")

        manche_cible = None
        for m in self.__manches:
            if m.numero == manche_num:
                manche_cible = m
                break

        if manche_cible is None:
            raise ValueError(f"La manche numéro {manche_num} n'existe pas dans cette soirée.")

        manche_cible.enregistrer_score(e, pts, 0, True)

    def modifier_score_equipe(self, e: Equipe, manche_num: int, nouveaux_pts: int) -> None:
        """Corrige un score déjà encodé et met à jour le classement."""
        if e not in self.__equipes:
            raise ValueError("L'équipe n'est pas inscrite à cette soirée.")

        manche_cible = None
        for m in self.__manches:
            if m.numero == manche_num:
                manche_cible = m
                break

        if manche_cible is None:
            raise ValueError(f"La manche numéro {manche_num} n'existe pas dans cette soirée.")

        score_trouve = None
        for s in manche_cible.scores:
            if s in e.scores:
                score_trouve = s
                break

        if score_trouve is None:
            raise ValueError("Aucun score n'a encore été encodé pour cette équipe sur cette manche.")

        score_trouve.modifier_points(nouveaux_pts)

    def calculer_classement_soiree(self) -> list:
        """Calcule le classement selon les points cumulés et le départage subsidiaire."""
        return sorted(
            self.__equipes,
            key=lambda eq: (eq.calculer_score_total(), eq.vainqueur_subsidiaire),
            reverse=True
        )

    def departager_egalite(self, e1: Equipe, e2: Equipe, gagnante: Equipe) -> None:
        """Départage deux équipes ex æquo via la question subsidiaire."""
        if e1 not in self.__equipes or e2 not in self.__equipes:
            raise ValueError("Les deux équipes doivent participer à cette soirée.")
        if e1.calculer_score_total() != e2.calculer_score_total():
            raise ValueError("Les deux équipes ne sont pas à égalité de points.")
        if gagnante not in (e1, e2):
            raise ValueError("L'équipe gagnante doit être l'une des deux équipes à égalité.")

        e1.definir_vainqueur_subsidiaire(gagnante == e1)
        e2.definir_vainqueur_subsidiaire(gagnante == e2)

    def correspond_critere(self, critere: str, valeur: str) -> bool:
        """Vérifie si la soirée correspond à un critère de recherche."""
        crit = critere.strip().lower()
        val = valeur.strip().lower()

        if crit == "date":
            date_iso = self.__date.isoformat()
            date_fr = self.__date.strftime("%d/%m/%Y")
            return val in date_iso or val in date_fr

        if crit == "equipe":
            return any(val in eq.nom_soiree.lower() for eq in self.__equipes)

        if crit == "capitaine":
            for eq in self.__equipes:
                cap = eq.capitaine
                nom_complet = f"{cap.prenom} {cap.nom}".lower()
                if val in cap.nom.lower() or val in cap.prenom.lower() or val in nom_complet:
                    return True
            return False

        return False

    def obtenir_classement_detaille(self) -> list:
        """Retourne la liste des scores de toutes les équipes classées."""
        scores_detailles = []
        for eq in self.calculer_classement_soiree():
            scores_detailles.extend(eq.scores)
        return scores_detailles

    def cloturer_soiree(self) -> None:
        """Clôture la soirée et attribue les points de championnat aux capitaines."""
        if not self.__en_cours:
            raise ValueError("Cette soirée est déjà clôturée.")

        self.__en_cours = False
        classement_final = self.calculer_classement_soiree()

        for rang, eq in enumerate(classement_final):
            points_championnat = max(5, 20 - 2 * rang)
            eq.capitaine.ajouter_points_championnat(points_championnat)