class Score:
    def __init__(self, points_base: int = 0, mise: int = 0, bonne_reponse_mise: bool = False):
        self.__points_base = points_base
        self.__mise = mise
        self.__bonne_reponse_mise = bonne_reponse_mise

    @property
    def points_base(self) -> int:
        return self.__points_base

    @property
    def mise(self) -> int:
        return self.__mise

    @property
    def bonne_reponse_mise(self) -> bool:
        return self.__bonne_reponse_mise

    def calculer_points_manche(self) -> int:
        return self.__points_base

    def modifier_points(self, nouveaux_points: int) -> None:
        self.__points_base = nouveaux_points

    def calculer_score_miser(self, est_correcte: bool, valeur_mise: int) -> int:
        if valeur_mise < 1 or valeur_mise > 5:
            raise ValueError("La mise doit être comprise entre 1 et 5 points.")

        self.__mise = valeur_mise
        self.__bonne_reponse_mise = est_correcte
        self.__points_base = 0

        if est_correcte:
            self.ajouter_points(valeur_mise)
        else:
            self.retrancher_points(valeur_mise)

        return self.calculer_points_manche()

    def ajouter_points(self, valeur_mise: int) -> None:
        self.__points_base += valeur_mise

    def retrancher_points(self, valeur_mise: int) -> None:
        self.__points_base -= valeur_mise