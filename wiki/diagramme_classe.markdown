_L’intelligence artificielle a été utilisée comme outil d’assistance pour contribuer à la reformulation de certaines phrases, dans le but d’améliorer la clarté et la cohérence du document._
```mermaid
classDiagram
    class Cafe {
        -String nom
        -Object etat_precedent
        +rechercher_capitaine(String nom, String prenom) Capitaine
        +creer_capitaine(String nom, String prenom, String tel) Capitaine
        +creer_equipe(Capitaine cap, String nom_soiree, int nb_participants) Equipe
        +rechercher_soirees(String critere, String valeur) List~SoireeQuiz~
        +ajouter_question(Question q) void
        +supprimer_question(String id) void
        +importer_questions(String chemin_fichier) void
        +a_soiree_en_cours() bool
        +serialiser_etat() String
        +restaurer_etat(String donnees) void
        +sauvegarder_etat_temporaire() void
        +a_un_etat_precedent() bool
        +restaurer_etat_precedent() void
    }

    class Sauvegarde {
        -Date date_sauvegarde
        -String chemin_usb
        +verifier_support_externe(String chemin_usb) bool
        +exporter_donnees(Cafe cafe, String chemin_usb) void
        +importer_donnees(String chemin_fichier) String
    }

    class SoireeQuiz {
        -Date date
        -int nb_manches
        -int nb_questions_par_manche
        -bool en_cours
        +creer_soiree(Date date, int nb_manches, int nb_questions) SoireeQuiz$
        +inscrire_equipe(Equipe e) void
        +ajouter_manche(Manche m) void
        +enregistrer_score_equipe(Equipe e, int manche_num, int pts) void
        +modifier_score_equipe(Equipe e, int manche_num, int nouveaux_pts) void
        +calculer_classement_soiree() List~Equipe~
        +departager_egalite(Equipe e1, Equipe e2, Equipe gagnante) void
        +correspond_critere(String critere, String valeur) bool
        +obtenir_classement_detaille() List~Score~
        +cloturer_soiree() void
    }

    class Manche {
        -int numero
        -bool est_a_miser
        +enregistrer_score(Equipe e, int pts, int mise, bool correcte) Score
    }

    class Question {
        -String id
        -String enonce
        -String reponse
        -String theme
        -int niveau_difficulte
        -Date derniere_utilisation
        +est_disponible(Date date_soiree) bool
        +marquer_utilisee(Date date_soiree) void
    }

    class Capitaine {
        -String id
        -String nom
        -String prenom
        -String telephone
        -List~int~ points_soirees
        +associer_equipe(Equipe e) void
        +ajouter_points_championnat(int pts) void
        +calculer_points_top10() int
        +reinitialiser_points_saison() void
    }

    class Equipe {
        -String id
        -String nom_soiree
        -int nb_participants
        -bool vainqueur_subsidiaire
        +calculer_score_total() int
    }

    class Score {
        -int points_base
        -int mise
        -bool bonne_reponse_mise
        +calculer_points_manche() int
        +modifier_points(int nouveaux_points) void
        +calculer_score_miser(bool est_correcte, int valeur_mise) int
        +ajouter_points(int valeur_mise) void
        +retrancher_points(int valeur_mise) void
    }

    class ChampionnatAnnuel {
        -int annee
        +calculer_classement_annuel() List~Capitaine~
        +trier_capitaines_par_points() List~Capitaine~
        +determiner_gagnant() Capitaine
        +reinitialiser_points() void
    }

    Cafe "1" *-- "0..*" SoireeQuiz : organise
    Cafe "1" o-- "0..*" Capitaine : enregistre
    Cafe "1" o-- "0..*" Question : stocke
    Cafe "1" *-- "0..*" ChampionnatAnnuel : gere
    Cafe "1" ..> "0..*" Sauvegarde : utilise
    SoireeQuiz "1" *-- "1..*" Manche : compose
    SoireeQuiz "1" -- "0..*" Equipe : participe
    Capitaine "1" -- "0..*" Equipe : represente
    Equipe "1" -- "0..*" Score : obtient
    Manche "1" -- "0..*" Score : contient
    ChampionnatAnnuel "1" o-- "0..*" Capitaine : regroupe
    Manche "0..*" -- "0..*" Question : utilise
```
1. Classe principale Cafe et répartition des responsabilités : Nous avons ajouté la classe Cafe comme point d'entrée principal du programme. Elle permet de centraliser l'accès aux données générales et de gérer les sauvegardes temporaires (F-09). Nous avons également ajouté la classe Sauvegarde, issue de D-06, qui s'occupe de l'exportation et de la restauration des données sur une clé USB. Cependant, nous avons préféré répartir les autres fonctionnalités dans les classes qui leur correspondent, comme SoireeQuiz, Capitaine, Score et ChampionnatAnnuel, plutôt que de tout regrouper dans une seule classe.

2. Séparation entre Capitaine et Equipe : Pour respecter la règle RM-04, qui demande de conserver l'historique même lorsqu'une équipe change de nom, nous avons séparé les classes Capitaine et Equipe. Une Equipe représente une participation à une soirée précise. Elle possède donc un nom temporaire (nom_soiree) ainsi qu'un indicateur permettant de départager les égalités (vainqueur_subsidiaire), conformément à la règle RM-08. Le Capitaine, quant à lui, reste enregistré d'une soirée à l'autre et conserve l'historique de ses points (points_soirees). Ces informations permettent notamment de calculer le Top 10 annuel (RM-12).

3. Compositions, agrégations et dépendances :
- Cafe → SoireeQuiz et ChampionnatAnnuel / SoireeQuiz → Manche : Nous avons utilisé des relations de composition (losange plein), car une soirée et un championnat sont liés au café, tandis qu'une manche dépend directement de la soirée à laquelle elle appartient. Leur existence est donc liée à celle de leur élément parent.
- Cafe → Capitaine et Question / ChampionnatAnnuel → Capitaine : Nous avons utilisé des relations d'agrégation (losange vide), car un capitaine ou une question peuvent exister indépendamment d'un championnat annuel.
- Cafe ..> Sauvegarde : Nous avons utilisé une relation de dépendance pour montrer que la classe Cafe fait appel à Sauvegarde lorsqu'il faut exporter ou restaurer les données.
4. Multiplicités : Nous avons ajouté des multiplicités sur les associations pour préciser combien d'objets peuvent être liés entre eux. Par exemple, chaque Equipe appartient à une seule SoireeQuiz, tandis qu'une soirée peut contenir plusieurs équipes (1 vers 0..*). Une équipe peut également avoir zéro ou plusieurs Score.

5. Répartition des responsabilités : Nous avons attribué les méthodes aux classes en fonction de leur rôle et des informations qu'elles possèdent. Par exemple, calculer_points_top10() se trouve dans Capitaine, calculer_score_miser() dans Score, est_disponible() dans Question et exporter_donnees() dans Sauvegarde. Nous avons également tenu compte des diagrammes de séquence pour garder une bonne cohérence entre les différents diagrammes. Cette organisation permet de mieux répartir le travail entre les classes et d'éviter qu'une seule classe ait trop de responsabilités.
