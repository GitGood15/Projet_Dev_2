from models.cafe import Cafe
from ui.interface_cli import InterfaceCLI


def main() -> None:
    cafe = Cafe("Le Comptoir des Curieux")
    interface = InterfaceCLI(cafe)
    interface.lancer()


if __name__ == "__main__":
    main()

"""
from ui.interface_graphique import ComptoirQuizApp


def main() -> None:
    ComptoirQuizApp().run()


if __name__ == "__main__":
    main()
"""