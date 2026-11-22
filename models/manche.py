from models.equipe import Equipe
from models.score import Score

class Manche:
    def __init__(self, numero : int, est_a_miser : bool):
        if numero < 1:
            raise ValueError("Le numéro de la manche doit être supérieur ou égal à 1.")
        self.__numero = numero
        self.__est_a_miser = est_a_miser
        
        self.__scores = []
        self.__questions = []
        
    @property
    def numero(self) -> int:
        return self.__numero
    
    @property
    def est_a_miser(self) -> bool:
        return self.__est_a_miser
    
    @property
    def scores(self) -> list:
        return list(self.__scores)

    @property
    def questions(self) -> list:
        return list(self.__questions)
    
    def definir_est_a_miser(self, est_a_miser: bool) -> None:
        """Désigne ou retire cette manche comme manche à miser."""
        self.__est_a_miser = est_a_miser

    def score_pour(self, e: Equipe):
        """Retourne le score déjà encodé pour cette équipe, s'il existe."""
        if e is None:
            return None
        for score in self.__scores:
            if score in e.scores:
                return score
        return None

    def poser_question(self, question, date_soiree) -> None:
        """Associe une question à la manche et bloque sa réutilisation pendant un an."""
        if question is None:
            raise ValueError("La question ne peut pas être nulle.")
        if any(q.id == question.id for q in self.__questions):
            raise ValueError("Cette question est déjà posée dans cette manche.")
        if not question.est_disponible(date_soiree):
            raise ValueError("Cette question ne peut pas être reposée avant un an.")
        question.marquer_utilisee(date_soiree)
        self.__questions.append(question)

    def lier_question(self, question) -> None:
        """Rattache une question déjà enregistrée, sans modifier sa date d'utilisation."""
        if question is not None and all(q.id != question.id for q in self.__questions):
            self.__questions.append(question)

    def enregistrer_score(self, e: Equipe, pts: int, mise: int, correcte: bool) -> Score:
        if e is None:
            raise ValueError("L'équipe ne peut pas être nulle.")
        if self.score_pour(e) is not None:
            raise ValueError(
                "Un score est déjà encodé pour cette équipe sur cette manche. Modifiez le score existant."
            )

        if self.__est_a_miser:
            score = Score(0, mise, correcte)
            score.calculer_score_miser(correcte, mise)
        else:
            if pts < 0:
                raise ValueError("Dans une manche classique, le score ne peut pas être négatif.")
            score = Score(pts, 0, correcte)

        self.__scores.append(score)
        e.ajouter_score(score)
        return score