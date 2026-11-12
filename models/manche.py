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
        return list(self.__scores.values())

    @property
    def questions(self) -> list:
        return list(self.__questions)
    
    def enregistrer_score(self, e: Equipe, pts: int, mise: int, correcte: bool) -> Score:
        if e is None:
            raise ValueError("L'équipe ne peut pas être nulle.")

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