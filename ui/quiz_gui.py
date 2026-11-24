import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

FICHIER = "soiree_quiz.json"  # sauvegarde automatique à côté du script


class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Comptoir des Curieux - Soirée quiz")
        self.geometry("720x500")
        self.equipes = {}  # nom de l'équipe -> score
        self.manche = 1
        self.creer_widgets()
        self.charger(FICHIER, silencieux=True)
        self.rafraichir()

    # ---------- Construction de l'interface ----------
    def creer_widgets(self):
        # Haut : manche en cours
        haut = ttk.Frame(self, padding=10)
        haut.pack(fill="x")
        self.label_manche = ttk.Label(haut, text="", font=("Arial", 16, "bold"))
        self.label_manche.pack(side="left")
        ttk.Button(haut, text="Manche suivante", command=self.manche_suivante).pack(side="right")

        # Milieu : classement
        milieu = ttk.Frame(self, padding=10)
        milieu.pack(fill="both", expand=True)
        colonnes = ("rang", "equipe", "score")
        self.tableau = ttk.Treeview(milieu, columns=colonnes, show="headings", height=10)
        self.tableau.heading("rang", text="Rang")
        self.tableau.heading("equipe", text="Équipe")
        self.tableau.heading("score", text="Score")
        self.tableau.column("rang", width=80, anchor="center")
        self.tableau.column("equipe", width=350)
        self.tableau.column("score", width=100, anchor="center")
        self.tableau.pack(fill="both", expand=True)

        # Ajout / suppression d'équipe
        bloc_equipe = ttk.LabelFrame(self, text="Équipes", padding=10)
        bloc_equipe.pack(fill="x", padx=10, pady=5)
        self.entree_nom = ttk.Entry(bloc_equipe, width=30)
        self.entree_nom.pack(side="left")
        self.entree_nom.bind("<Return>", lambda e: self.ajouter_equipe())
        ttk.Button(bloc_equipe, text="Ajouter", command=self.ajouter_equipe).pack(side="left", padx=5)
        ttk.Button(bloc_equipe, text="Supprimer l'équipe sélectionnée",
                   command=self.supprimer_equipe).pack(side="left", padx=5)

        # Points
        bloc_points = ttk.LabelFrame(self, text="Points (équipe sélectionnée)", padding=10)
        bloc_points.pack(fill="x", padx=10, pady=5)
        ttk.Label(bloc_points, text="Points :").pack(side="left")
        self.entree_points = ttk.Entry(bloc_points, width=6)
        self.entree_points.insert(0, "1")
        self.entree_points.pack(side="left", padx=5)
        ttk.Button(bloc_points, text="+ Ajouter",
                   command=lambda: self.modifier_score(+1)).pack(side="left", padx=5)
        ttk.Button(bloc_points, text="- Retirer",
                   command=lambda: self.modifier_score(-1)).pack(side="left", padx=5)

        # Manche à miser
        bloc_mise = ttk.LabelFrame(self, text="Manche à miser (équipe sélectionnée)", padding=10)
        bloc_mise.pack(fill="x", padx=10, pady=5)
        ttk.Label(bloc_mise, text="Mise :").pack(side="left")
        self.entree_mise = ttk.Entry(bloc_mise, width=6)
        self.entree_mise.insert(0, "2")
        self.entree_mise.pack(side="left", padx=5)
        ttk.Button(bloc_mise, text="Bonne réponse (+mise)",
                   command=lambda: self.miser(True)).pack(side="left", padx=5)
        ttk.Button(bloc_mise, text="Mauvaise réponse (-mise)",
                   command=lambda: self.miser(False)).pack(side="left", padx=5)

        # Sauvegarde
        bas = ttk.Frame(self, padding=10)
        bas.pack(fill="x")
        ttk.Button(bas, text="Enregistrer sous... (clé USB)",
                   command=self.enregistrer_sous).pack(side="left")
        ttk.Button(bas, text="Ouvrir une soirée...",
                   command=self.ouvrir).pack(side="left", padx=5)

    # ---------- Actions ----------
    def ajouter_equipe(self):
        nom = self.entree_nom.get().strip()
        if not nom:
            return
        if nom in self.equipes:
            messagebox.showwarning("Doublon", "Cette équipe existe déjà.")
            return
        self.equipes[nom] = 0
        self.entree_nom.delete(0, "end")
        self.mettre_a_jour()

    def equipe_selectionnee(self):
        selection = self.tableau.selection()
        if not selection:
            messagebox.showinfo("Info", "Sélectionne d'abord une équipe dans le tableau.")
            return None
        return self.tableau.item(selection[0])["values"][1]

    def supprimer_equipe(self):
        nom = self.equipe_selectionnee()
        if nom is not None and messagebox.askyesno("Confirmer", f"Supprimer {nom} ?"):
            del self.equipes[str(nom)]
            self.mettre_a_jour()

    def lire_entier(self, entree):
        try:
            return int(entree.get())
        except ValueError:
            messagebox.showerror("Erreur", "Entre un nombre entier.")
            return None

    def modifier_score(self, signe):
        nom = self.equipe_selectionnee()
        points = self.lire_entier(self.entree_points)
        if nom is None or points is None:
            return
        self.equipes[str(nom)] += signe * points
        self.mettre_a_jour()

    def miser(self, gagne):
        nom = self.equipe_selectionnee()
        mise = self.lire_entier(self.entree_mise)
        if nom is None or mise is None:
            return
        self.equipes[str(nom)] += mise if gagne else -mise
        self.mettre_a_jour()

    def manche_suivante(self):
        self.manche += 1
        self.mettre_a_jour()

    # ---------- Affichage ----------
    def rafraichir(self):
        self.label_manche.config(text=f"Manche {self.manche}")
        self.tableau.delete(*self.tableau.get_children())
        classement = sorted(self.equipes.items(), key=lambda x: x[1], reverse=True)
        rang = 0
        score_precedent = None
        for i, (nom, score) in enumerate(classement, start=1):
            if score != score_precedent:  # nouveau rang seulement si le score change
                rang = i
                score_precedent = score
            ex_aequo = sum(1 for _, s in classement if s == score) > 1
            texte_rang = f"{rang} (ex æquo)" if ex_aequo else str(rang)
            self.tableau.insert("", "end", values=(texte_rang, nom, score))

    def mettre_a_jour(self):
        self.rafraichir()
        self.sauvegarder(FICHIER)

    # ---------- Sauvegarde ----------
    def sauvegarder(self, chemin):
        donnees = {"manche": self.manche, "equipes": self.equipes}
        with open(chemin, "w", encoding="utf-8") as f:
            json.dump(donnees, f, ensure_ascii=False, indent=2)

    def charger(self, chemin, silencieux=False):
        try:
            with open(chemin, "r", encoding="utf-8") as f:
                donnees = json.load(f)
            self.manche = donnees["manche"]
            self.equipes = donnees["equipes"]
        except FileNotFoundError:
            if not silencieux:
                messagebox.showerror("Erreur", "Fichier introuvable.")
        except (json.JSONDecodeError, KeyError):
            messagebox.showerror("Erreur", "Fichier de sauvegarde invalide.")

    def enregistrer_sous(self):
        chemin = filedialog.asksaveasfilename(defaultextension=".json",
                                              filetypes=[("Soirée quiz", "*.json")])
        if chemin:
            self.sauvegarder(chemin)

    def ouvrir(self):
        chemin = filedialog.askopenfilename(filetypes=[("Soirée quiz", "*.json")])
        if chemin:
            self.charger(chemin)
            self.mettre_a_jour()


if __name__ == "__main__":
    App().mainloop()
