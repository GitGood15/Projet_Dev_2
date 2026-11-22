"""Interface en ligne de commande pour la gestion des soirées quiz."""

import os
from datetime import date

from models.cafe import Cafe
from models.championnat_annuel import ChampionnatAnnuel
from models.manche import Manche
from models.question import Question
from models.soiree_quiz import SoireeQuiz
from services.sauvegarde import Sauvegarde


class InterfaceCLI:
	"""Présente les menus et délègue les opérations aux modèles du domaine."""

	def __init__(self, cafe: Cafe, chemin_donnees_locales: str = "data/donnees_cafe.json"):
		self.__cafe = cafe
		self.__sauvegarde = Sauvegarde()
		self.__chemin_local = chemin_donnees_locales
		self.__classement_visible = True
		self.__charger_donnees_locales()

	def __charger_donnees_locales(self) -> None:
		if not os.path.isfile(self.__chemin_local):
			return
		try:
			with open(self.__chemin_local, "r", encoding="utf-8") as fichier:
				self.__cafe.restaurer_etat(fichier.read())
		except (OSError, ValueError, KeyError, TypeError) as erreur:
			print(f"[Avertissement] Chargement des données impossible : {erreur}")

	def __sauvegarder_auto(self) -> None:
		dossier = os.path.dirname(self.__chemin_local)
		if dossier:
			os.makedirs(dossier, exist_ok=True)
		with open(self.__chemin_local, "w", encoding="utf-8") as fichier:
			fichier.write(self.__cafe.serialiser_etat())

	def __obtenir_soiree_active(self) -> SoireeQuiz | None:
		return next((soiree for soiree in self.__cafe.soirees if soiree.en_cours), None)

	@staticmethod
	def __lire_entier(message: str, minimum: int | None = None, maximum: int | None = None,
					   defaut: int | None = None) -> int:
		while True:
			valeur = input(message).strip()
			if not valeur and defaut is not None:
				return defaut
			try:
				nombre = int(valeur)
				if minimum is not None and nombre < minimum:
					raise ValueError
				if maximum is not None and nombre > maximum:
					raise ValueError
				return nombre
			except ValueError:
				limites = f" (entre {minimum} et {maximum})" if minimum is not None and maximum is not None else ""
				print(f"Veuillez saisir un nombre entier valide{limites}.")

	@staticmethod
	def __confirmer(message: str) -> bool:
		return input(f"{message} (o/n) : ").strip().lower() in ("o", "oui")

	def lancer(self) -> None:
		actions = {"1": self.__menu_equipes, "2": self.__menu_questions,
				   "3": self.__menu_organiser_soiree, "4": self.__menu_scores,
				   "5": self.__menu_cloturer_soiree, "6": self.__menu_historique,
				   "7": self.__menu_championnat, "8": self.__menu_sauvegarde,
				   "9": self.__annuler}
		while True:
			active = self.__obtenir_soiree_active()
			statut = f"En cours ({active.date:%d/%m/%Y})" if active else "Aucune"
			print(f"\n=== {self.__cafe.nom.upper()} — GESTION QUIZ ===")
			print(f"Soirée active : {statut}")
			print("1. Gérer les équipes")
			print("2. Gérer / importer les questions")
			print("3. Organiser une soirée")
			print("4. Encoder / corriger les scores et mises")
			print("5. Clôturer la soirée et attribuer les points")
			print("6. Consulter l'historique")
			print("7. Consulter / clôturer le championnat")
			print("8. Sauvegarder / restaurer")
			print("9. Annuler la dernière modification")
			print("0. Quitter")
			choix = input("Votre choix : ").strip()
			if choix == "0":
				self.__sauvegarder_auto()
				print("Données enregistrées localement. Au revoir !")
				return
			action = actions.get(choix)
			if action is None:
				print("[Erreur] Choix invalide.")
				continue
			try:
				action()
			except (ValueError, OSError, KeyError, TypeError) as erreur:
				print(f"[Erreur] {erreur}")

	def __annuler(self) -> None:
		self.__cafe.restaurer_etat_precedent()
		self.__sauvegarder_auto()
		print("[OK] Dernière modification annulée.")

	def __menu_equipes(self) -> None:
		print("\n--- INSCRIPTION D'UNE ÉQUIPE ---")
		soiree = self.__obtenir_soiree_active()
		if soiree is None:
			raise ValueError("Organisez d'abord une soirée (menu 3) : les équipes sont enregistrées dans la soirée.")
		nom = input("Nom du capitaine : ").strip()
		prenom = input("Prénom du capitaine : ").strip()
		capitaine = self.__cafe.rechercher_capitaine(nom, prenom)
		if capitaine is None:
			capitaine = self.__cafe.creer_capitaine(nom, prenom, input("Téléphone : ").strip())
			print("Nouveau capitaine enregistré.")
		else:
			print(f"Profil retrouvé : {capitaine.prenom} {capitaine.nom}.")
		equipe = self.__cafe.creer_equipe(
			capitaine, input("Nom de l'équipe pour cette soirée : ").strip(),
			self.__lire_entier("Nombre de participants, capitaine inclus : ", minimum=1))
		soiree.inscrire_equipe(equipe)
		self.__sauvegarder_auto()
		print(f"[OK] Équipe « {equipe.nom_soiree} » enregistrée.")

	def __menu_questions(self) -> None:
		print("\n--- BANQUE DE QUESTIONS ---")
		print("1. Ajouter")
		print("2. Supprimer")
		print("3. Importer CSV/JSON")
		print("4. Lister")
		choix = input("Votre choix : ").strip()
		if choix == "1":
			question = Question(input("Énoncé : ").strip(), input("Réponse attendue : ").strip(),
								input("Thème : ").strip(), self.__lire_entier("Difficulté (1 à 3) : ", 1, 3))
			self.__cafe.ajouter_question(question)
			self.__sauvegarder_auto()
			print(f"[OK] Question ajoutée (ID : {question.id}).")
		elif choix == "2":
			self.__lister_questions()
			self.__cafe.supprimer_question(input("ID à supprimer : ").strip())
			self.__sauvegarder_auto()
			print("[OK] Question supprimée.")
		elif choix == "3":
			chemin = input("Chemin du fichier .csv ou .json : ").strip().strip('"')
			self.__cafe.importer_questions(chemin)
			self.__sauvegarder_auto()
			print("[OK] Questions importées.")
		elif choix == "4":
			self.__lister_questions()
		else:
			print("Choix invalide.")

	def __lister_questions(self) -> None:
		if not self.__cafe.questions:
			print("Aucune question enregistrée.")
			return
		for question in self.__cafe.questions:
			statut = "disponible" if question.est_disponible(date.today()) else "utilisée depuis moins d'un an"
			print(f"[{question.id}] {question.theme} | niv. {question.niveau_difficulte} | {statut} : {question.enonce}")

	def __menu_organiser_soiree(self) -> None:
		if self.__cafe.a_soiree_en_cours():
			raise ValueError("Une soirée est déjà en cours. Clôturez-la avant d'en créer une autre.")
		nb_manches = self.__lire_entier("Nombre de manches [6] : ", minimum=1, defaut=6)
		nb_questions = self.__lire_entier("Questions par manche [8] : ", minimum=1, defaut=8)
		defaut_mise = 6 if nb_manches >= 6 else 0
		num_mise = self.__lire_entier("Numéro de la manche à miser (0 = aucune) : ", 0, nb_manches, defaut_mise)
		soiree = SoireeQuiz.creer_soiree(date.today(), nb_manches, nb_questions)
		for numero in range(1, nb_manches + 1):
			soiree.ajouter_manche(Manche(numero, numero == num_mise))
		self.__cafe.ajouter_soiree(soiree)
		self.__sauvegarder_auto()
		print(f"[OK] Soirée créée : {nb_manches} manches de {nb_questions} questions.")

	@staticmethod
	def __score_deja_saisi(equipe, manche: Manche) -> bool:
		return any(score in equipe.scores for score in manche.scores)

	def __menu_scores(self) -> None:
		soiree = self.__obtenir_soiree_active()
		if soiree is None:
			raise ValueError("Aucune soirée n'est en cours.")
		if not soiree.equipes:
			raise ValueError("Aucune équipe n'est inscrite à la soirée.")
		print("\n--- SCORES ---")
		print("1. Encoder les scores d'une manche")
		print("2. Corriger un score")
		print(f"3. {'Masquer' if self.__classement_visible else 'Afficher'} le classement")
		print("4. Départager une égalité")
		choix = input("Votre choix : ").strip()
		if choix == "1":
			for manche in soiree.manches:
				print(f"Manche {manche.numero}{' (À MISER)' if manche.est_a_miser else ''}")
			numero = self.__lire_entier("Numéro de manche : ", 1, soiree.nb_manches)
			manche = next((m for m in soiree.manches if m.numero == numero), None)
			if manche is None:
				raise ValueError("Cette manche n'existe pas.")
			if all(self.__score_deja_saisi(eq, manche) for eq in soiree.equipes):
				raise ValueError("Les scores de cette manche ont déjà été encodés.")
			self.__cafe.sauvegarder_etat_temporaire()
			for equipe in soiree.equipes:
				if self.__score_deja_saisi(equipe, manche):
					continue
				if manche.est_a_miser:
					mise = self.__lire_entier(f"Mise de {equipe.nom_soiree} (1 à 5) : ", 1, 5)
					manche.enregistrer_score(equipe, 0, mise, self.__confirmer("Bonne réponse ?"))
				else:
					points = self.__lire_entier(f"Points de {equipe.nom_soiree} : ", 0, soiree.nb_questions_par_manche)
					soiree.enregistrer_score_equipe(equipe, numero, points)
			self.__sauvegarder_auto()
			if self.__classement_visible:
				self.__afficher_classement(soiree)
			else:
				print("[OK] Scores enregistrés ; classement masqué.")
		elif choix == "2":
			equipe = self.__choisir_equipe(soiree)
			numero = self.__lire_entier("Numéro de manche à corriger : ", 1, soiree.nb_manches)
			manche = next((m for m in soiree.manches if m.numero == numero), None)
			if manche is None or not self.__score_deja_saisi(equipe, manche):
				raise ValueError("Aucun score trouvé pour cette équipe et cette manche.")
			points = self.__lire_entier("Nouveau score (une mise peut donner un score négatif) : ")
			self.__cafe.sauvegarder_etat_temporaire()
			soiree.modifier_score_equipe(equipe, numero, points)
			self.__sauvegarder_auto()
			if self.__classement_visible:
				self.__afficher_classement(soiree)
		elif choix == "3":
			self.__classement_visible = not self.__classement_visible
			print(f"Classement {'visible' if self.__classement_visible else 'masqué'}.")
			if self.__classement_visible:
				self.__afficher_classement(soiree)
		elif choix == "4":
			self.__afficher_classement(soiree)
			e1, e2 = self.__choisir_equipe(soiree), self.__choisir_equipe(soiree)
			gagnante = e1 if self.__lire_entier("Laquelle gagne ? (1 ou 2) : ", 1, 2) == 1 else e2
			self.__cafe.sauvegarder_etat_temporaire()
			soiree.departager_egalite(e1, e2, gagnante)
			self.__sauvegarder_auto()
			self.__afficher_classement(soiree)
		else:
			print("Choix invalide.")

	@staticmethod
	def __choisir_equipe(soiree: SoireeQuiz):
		for index, equipe in enumerate(soiree.equipes, start=1):
			print(f"{index}. {equipe.nom_soiree} — {equipe.capitaine.prenom} {equipe.capitaine.nom}")
		choix = InterfaceCLI.__lire_entier("Numéro de l'équipe : ", 1, len(soiree.equipes))
		return soiree.equipes[choix - 1]

	@staticmethod
	def __afficher_classement(soiree: SoireeQuiz) -> None:
		print(f"\n--- CLASSEMENT DU {soiree.date:%d/%m/%Y} ---")
		for rang, equipe in enumerate(soiree.calculer_classement_soiree(), start=1):
			sub = " (subsidiaire)" if equipe.vainqueur_subsidiaire else ""
			print(f"{rang}. {equipe.nom_soiree} — {equipe.calculer_score_total()} point(s){sub}")

	def __menu_cloturer_soiree(self) -> None:
		soiree = self.__obtenir_soiree_active()
		if soiree is None:
			raise ValueError("Aucune soirée active à clôturer.")
		if not self.__confirmer("Clôturer définitivement cette soirée ?"):
			return
		self.__cafe.sauvegarder_etat_temporaire()
		soiree.cloturer_soiree()
		self.__sauvegarder_auto()
		self.__afficher_classement(soiree)
		print("[OK] Soirée clôturée et points de championnat attribués. Pensez à sauvegarder sur un support externe.")

	def __menu_historique(self) -> None:
		critere = input("Rechercher par date, equipe ou capitaine : ").strip().lower()
		if critere not in {"date", "equipe", "capitaine"}:
			raise ValueError("Critère invalide. Choisissez date, equipe ou capitaine.")
		soirees = self.__cafe.rechercher_soirees(critere, input("Valeur recherchée : ").strip())
		if not soirees:
			print("Aucune soirée correspondante.")
			return
		for index, soiree in enumerate(soirees, start=1):
			print(f"{index}. {soiree.date:%d/%m/%Y} — {len(soiree.equipes)} équipe(s)")
		choix = self.__lire_entier("Soirée à consulter : ", 1, len(soirees))
		self.__afficher_classement(soirees[choix - 1])

	def __menu_championnat(self) -> None:
		annee = self.__lire_entier(f"Année du championnat [{date.today().year}] : ", 2000, defaut=date.today().year)
		championnat = ChampionnatAnnuel(annee, self.__cafe.capitaines)
		classement = championnat.calculer_classement_annuel()
		print(f"\n--- CHAMPIONNAT {annee} (TOP 10) ---")
		if not classement:
			print("Aucun capitaine enregistré.")
			return
		for rang, capitaine in enumerate(classement, start=1):
			print(f"{rang}. {capitaine.prenom} {capitaine.nom} — {capitaine.calculer_points_top10()} points")
		if self.__confirmer("Clôturer le championnat et remettre les points à zéro ?"):
			gagnant = championnat.determiner_gagnant()
			if gagnant:
				print(f"Vainqueur : {gagnant.prenom} {gagnant.nom} ({gagnant.calculer_points_top10()} points).")
			if input("Confirmer la remise à zéro en tapant OUI : ").strip() == "OUI":
				self.__cafe.sauvegarder_etat_temporaire()
				championnat.reinitialiser_points()
				self.__sauvegarder_auto()
				print("[OK] Points de championnat réinitialisés.")

	def __menu_sauvegarde(self) -> None:
		print("\n--- SAUVEGARDE / RESTAURATION ---")
		print("1. Sauvegarder sur un support externe")
		print("2. Restaurer depuis un fichier JSON")
		choix = input("Votre choix : ").strip()
		if choix == "1":
			chemin = input("Dossier du support externe (ex. E:\\) : ").strip().strip('"')
			self.__sauvegarde.exporter_donnees(self.__cafe, chemin)
			print("[OK] Sauvegarde créée.")
		elif choix == "2":
			chemin = input("Chemin du fichier JSON : ").strip().strip('"')
			donnees = self.__sauvegarde.importer_donnees(chemin)
			self.__cafe.sauvegarder_etat_temporaire()
			self.__cafe.restaurer_etat(donnees)
			self.__sauvegarder_auto()
			print("[OK] Données restaurées.")
		else:
			print("Choix invalide.")


if __name__ == "__main__":
	InterfaceCLI(Cafe()).lancer()
