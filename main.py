import argparse
import os

from models.cafe import Cafe
from ui.interface_cli import InterfaceCLI


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Gestion des soirées quiz du Comptoir des Curieux.",
        allow_abbrev=False,
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--demo",
        action="store_true",
        help="lancer la démo simplifiée en ligne de commande",
    )
    modes.add_argument(
        "--demo-kivy",
        action="store_true",
        help="lancer la démo simplifiée dans une interface graphique Kivy",
    )
    arguments = parser.parse_args()

    cafe = Cafe("Le Comptoir des Curieux")
    if arguments.demo_kivy:
        os.environ["KIVY_NO_ARGS"] = "1"
        from ui.interface_demo_kivy import DemoQuizKivyApp

        DemoQuizKivyApp(cafe).run()
    elif arguments.demo:
        from ui.interface_demo import InterfaceDemo

        interface = InterfaceDemo(cafe)
        interface.lancer()
    else:
        InterfaceCLI(cafe).lancer()


if __name__ == "__main__":
    main()

"""
from ui.interface_graphique import ComptoirQuizApp


def main() -> None:
    ComptoirQuizApp().run()


if __name__ == "__main__":
    main()
"""