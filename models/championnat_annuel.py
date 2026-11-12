from models.capitaine import Capitaine


class ChampionnatAnnuel:
    def __init__(self, annee: int, capitaines: list = None):
        if annee < 2000:
            raise ValueError("L'année du championnat est invalide.")

        self.__annee = annee

        self.__capitaines = capitaines if capitaines is not None else []

    @property
    def annee(self) -> int:
        return self.__annee

    @property
    def capitaines(self) -> list:
        return list(self.__capitaines)

    def calculer_classement_annuel(self) -> list:
        """Calcule le classement annuel sur base des 10 meilleurs scores de chaque capitaine."""
        for cap in self.__capitaines:
            cap.calculer_points_top10()

        return self.trier_capitaines_par_points()

    def trier_capitaines_par_points(self) -> list:
        """Trie les capitaines par ordre décroissant de leurs points Top 10."""
        return sorted(
            self.__capitaines,
            key=lambda cap: cap.calculer_points_top10(),
            reverse=True
        )

    def determiner_gagnant(self) -> Capitaine:
        """Retourne le capitaine en tête du classement annuel."""
        classement = self.calculer_classement_annuel()
        if not classement:
            return None
        return classement[0]

    def reinitialiser_points(self) -> None:
        """Remet à zéro les points de tous les capitaines après validation de fin de saison."""
        for cap in self.__capitaines:
            cap.reinitialiser_points_saison()