_L’intelligence artificielle a été utilisée comme outil d’assistance pour contribuer à la structuration des diagrammes ainsi qu’à la reformulation de certaines phrases, dans le but d’améliorer la clarté et la cohérence du document._

# Diagramme 1 : Diagramme de Séquence — F-01 : Gérer les équipes

```mermaid

sequenceDiagram
    title Diagramme de Séquence — F-01 : Gérer les équipes (Auteur : Ilian Benzakour)

    actor M as M. Mertens
    participant UI as ui : Interface
    participant CAFE as cafe : Cafe
    participant CAP as cap : Capitaine
    participant EQ as eq : Equipe

    M->>UI: enregistrer_equipe(nom_cap, prenom_cap, tel, nom_soiree, nb_participants)
    activate UI

    UI->>CAFE: rechercher_capitaine(nom_cap, prenom_cap)
    activate CAFE
    CAFE-->>UI: cap_existant
    deactivate CAFE

    alt cap_existant == null (EF-01.0)
        UI->>CAFE: creer_capitaine(nom_cap, prenom_cap, tel)
        activate CAFE
        CAFE->>CAP: create(nom_cap, prenom_cap, tel)
        Note over CAFE,CAP: Création d'un nouveau capitaine
        CAFE-->>UI: cap
        deactivate CAFE
    else cap_existant != null (EF-01.1)
        Note over UI: Réutilisation du profil existant (RM-04)
    end

    UI->>CAFE: creer_equipe(cap, nom_soiree, nb_participants)
    activate CAFE
    CAFE->>EQ: create(nom_soiree, nb_participants)
    CAFE->>CAP: associer_equipe(eq)
    activate CAP
    CAP-->>CAFE: confirmation
    deactivate CAP
    CAFE-->>UI: eq
    deactivate CAFE

    UI-->>M: confirmation_enregistrement_equipe
    deactivate UI
```

- Différence entre Capitaine et Equipe : Pour respecter la règle RM-04, nous avons séparé les classes Capitaine et Equipe. Le capitaine reste le même au fil des soirées, ce qui permet de conserver son historique. L'équipe, quant à elle, est créée pour chaque soirée et possède un nom temporaire (nom_soiree).

- Gestion des deux possibilités EF-01.0 / EF-01.1 : Le bloc alt/else permet de représenter les deux situations possibles. Si le capitaine n'est pas encore connu du système, un nouveau profil est créé. Par contre, s'il est déjà inscrit, son profil existant est simplement réutilisé. Cela correspond aux deux cas prévus dans la fiche du Use Case.

# Diagramme 2 :  F‐02 — Gérer et importer les questions         (Auteur : Ismail Mehane)

<img width="1378" height="855" alt="image" src="https://github.com/user-attachments/assets/494d06c5-f0b8-42bc-89c4-53625b3db052" />

- Ce diagramme représente l'ajout des questions par M.mertens dans la base de données des questions.Le programme vérifie d'abord que aucune partie ne se joue car si une partie est active l'ajoute d'une question est impossible et l'ajout sera refusé(on peut encoder la difficulté de 1 à 3).
- j'ai également séparé les responsabilités entre les classes pour faciliter la gestion des questions.

# Diagramme 3 :  F-03 — Organiser une soirée         (Auteur: Ilian Benzakour)

<img width="521" height="594" alt="Capture d’écran, le 2026-11-02 à 21 46 34" src="https://github.com/user-attachments/assets/cce8be8b-3542-447b-9340-85639f6147bc" />


- Ce diagramme représente la création d'une partie par M.Mertens. Il peut ajuster le nombre de manches, de questions et de manches spéciales. Le programme vérifie si une équipe existe déjà en base de données ou s'il faut en créer une. Le programme fini par créer le partie

# Diagramme 4 :  F-04 - Encoder les scores et résultats
```mermaid
sequenceDiagram
    actor M as M. Mertens
    participant UI as ui : Interface
    participant S as s : SoireeQuiz
    participant MANCHE as m : Manche
    participant SC as sc : Score
    participant CAP as cap : Capitaine

    alt Nouvel encodage de manche (EF-04.1)
        M->>UI: encoder_score(equipe, manche_num, nb_bonnes_reponses)
        activate UI
        UI->>S: enregistrer_score_equipe(equipe, manche_num, nb_bonnes_reponses)
        activate S
        S->>MANCHE: enregistrer_score(equipe, nb_bonnes_reponses, 0, true)
        activate MANCHE
        MANCHE->>SC: create(nb_bonnes_reponses)
        Note right of SC: 1 bonne réponse = 1 pt (RM-09)
        MANCHE-->>S: sc
        deactivate MANCHE
    else Correction d'une erreur de saisie (EF-04.2)
        M->>UI: modifier_score(equipe, manche_num, nouveaux_points)
        activate UI
        UI->>S: modifier_score_equipe(equipe, manche_num, nouveaux_points)
        activate S
        S->>SC: modifier_points(nouveaux_points)
        activate SC
        SC-->>S: confirmation_modification
        deactivate SC
    end

    S->>S: calculer_classement_soiree() (RM-07)
    S-->>UI: classement_actualise
    deactivate S

    alt classement_visible == true (EF-04.3)
        UI-->>M: afficher_classement_soiree(classement_actualise)
    else classement_visible == false (EF-04.3)
        UI-->>M: confirmer_sauvegarde_score()
    end
    deactivate UI

    opt Fin de la soirée quiz (EF-04.4, EF-01.4)
        M->>UI: cloturer_soiree()
        activate UI
        UI->>S: cloturer_soiree()
        activate S
        loop Pour chaque équipe participante
            S->>CAP: ajouter_points_championnat(points_soiree)
            activate CAP
            CAP-->>S: historique_mis_a_jour
            deactivate CAP
        end
        S-->>UI: classement_final
        deactivate S
        UI-->>M: afficher_classement_final(classement_final)
        deactivate UI
    end
```
- Respect des lignes de vie du modèle : Nous avons repris uniquement des objets qui existent déjà dans notre diagramme de classes, à savoir SoireeQuiz, Manche, Score et Capitaine. Nous n'avons donc pas ajouté de classe générale comme « Système » ou « Base de données », afin de rester cohérents avec notre modèle.

- Lien avec les exigences de F-04 :
- EF-04.1 et RM-09 : Lorsqu'un score est encodé, une nouvelle instance de Score est créée et associée à la manche ainsi qu'à l'équipe concernée.
- EF-04.2 : Le premier bloc alt représente le cas où un score doit être corrigé. Une fois la modification effectuée, le classement de la soirée est directement recalculé grâce à la méthode calculer_classement_soiree() (RM-07).
- EF-04.3 : Le deuxième bloc alt permet de montrer les deux possibilités : afficher le classement au public ou le garder masqué pendant la soirée. Cette responsabilité est confiée à Interface pour éviter de mélanger la gestion des données avec leur affichage.
- EF-04.4 et EF-01.4 : Le bloc opt représente l'enregistrement des résultats à la fin de la soirée dans l'objet Capitaine. Cela permet de conserver l'historique des résultats, même si le nom de l'équipe change d'une soirée à l'autre, comme demandé dans la règle RM-04.
- Mise à jour du diagramme de classes : En réalisant ce diagramme de séquence, nous avons identifié deux méthodes supplémentaires : modifier_score_equipe(...) dans SoireeQuiz et modifier_points(...) dans Score. Il faudra donc les ajouter au diagramme de classes pour que les deux diagrammes restent cohérents. Cela fait partie de la démarche progressive de conception vue au cours.

# Diagramme 5 :  F-05 - Consulter le classement d'une soirée
```mermaid
sequenceDiagram
    actor M as M. Mertens
    participant UI as ui : Interface
    participant CAFE as cafe : Cafe
    participant S as s : SoireeQuiz
    participant EQ as eq : Equipe

    M->>UI: rechercher_historique(critere, valeur)
    activate UI

    UI->>CAFE: rechercher_soirees(critere, valeur)
    activate CAFE

    loop Pour chaque soirée s enregistrée (EF-05.2, EF-05.3, EF-05.4)
        CAFE->>S: correspond_critere(critere, valeur)
        activate S
        S-->>CAFE: bool_correspond
        deactivate S
    end

    CAFE-->>UI: liste_soirees_trouvees
    deactivate CAFE

    alt liste_soirees_trouvees est vide (EF-05.1)
        UI-->>M: message("Aucune soirée correspondante")
    else Au moins une soirée trouvée
        UI-->>M: affiche_liste_soirees
        M->>UI: selectionner_soiree(s)
        UI->>S: obtenir_classement_detaille()
        activate S

        loop Pour chaque équipe eq participante
            S->>EQ: calculer_score_total()
            activate EQ
            EQ-->>S: total_points
            deactivate EQ
        end

        S-->>UI: classement_detaille (D-04)
        deactivate S
        UI-->>M: affiche_classement_et_scores
    end

    deactivate UI
```
- Respect du principe d'expert en information : Nous avons confié la recherche à l'objet SoireeQuiz, qui vérifie si une soirée correspond aux critères demandés. Ces critères peuvent être la date (EF-05.2), l'équipe (EF-05.3) ou le capitaine (EF-05.4). De son côté, chaque objet Equipe calcule lui-même son total de points grâce à la méthode calculer_score_total(). Cela permet de donner chaque responsabilité à la classe qui possède les informations nécessaires.

- Séparation entre l'interface et la logique métier : Nous avons choisi de laisser l'objet Interface s'occuper uniquement des actions de l'utilisateur, comme la sélection des critères et l'affichage des résultats. Le filtrage et le tri des données sont réalisés par les objets du domaine afin de ne pas mélanger l'affichage avec le fonctionnement du programme.

# Diagramme 6 : F-06 Calcul du classement du championnat (Auteur : Florent Chiappelloni)
```mermaid
sequenceDiagram
    actor M as M. Mertens
    participant UI as ui : Interface
    participant C as champ : ChampionnatAnnuel
    participant CAP as cap : Capitaine

    M->>UI: consulter_championnat_annuel()
    activate UI
    UI->>C: calculer_classement_annuel()
    activate C

    loop Pour chaque Capitaine du championnat
        C->>CAP: calculer_points_top10() (RM-12, EF-06.3)
        activate CAP
        CAP-->>C: total_10_meilleurs_points
        deactivate CAP
    end

    C->>C: trier_capitaines_par_points()
    C-->>UI: liste_capitaines_classee
    deactivate C
    UI-->>M: affichage_classement_annuel
    deactivate UI
```
- **Fragment loop :** Nous avons utilisé un fragment loop pour montrer que le programme répète la même opération pour chaque capitaine enregistré afin de récupérer ses résultats.

- **Application de la règle métier RM-12 :** Le message calculer_points_top10() est envoyé à la classe Capitaine, car c'est elle qui possède l'historique des scores. Il est donc logique que ce soit cette classe qui s'occupe de calculer le total en prenant uniquement les 10 meilleurs résultats de chaque capitaine. Cela permet de respecter la règle métier RM-12.

# Diagramme 7 : F-07 Traitement d'une manche à miser (Auteur : Gildas Kockerols)
```mermaid
sequenceDiagram
    actor M as M. Mertens
    participant UI as ui : Interface
    participant MANCHE as m : Manche
    participant SC as sc : Score

    M->>UI: enregistrer_mise(equipe, valeur_mise, est_correcte)
    activate UI
    UI->>MANCHE: enregistrer_score(equipe, 0, valeur_mise, est_correcte)
    activate MANCHE
    MANCHE->>SC: calculer_score_miser(est_correcte, valeur_mise)
    activate SC

    alt est_correcte == true (EF-07.3)
        SC->>SC: ajouter_points(valeur_mise)
    else est_correcte == false (EF-07.4)
        SC->>SC: retrancher_points(valeur_mise)
        Note over SC: Le solde peut devenir négatif (EF-07.4)
    end

    SC-->>MANCHE: score_manche_calcule
    deactivate SC
    MANCHE-->>UI: confirmation_mise_enregistree
    deactivate MANCHE
    UI-->>M: affichage_score_mis_a_jour
    deactivate UI
```
- **Gestion des différents cas :** Le fragment alt permet de montrer les deux situations possibles : lorsque le joueur gagne des points ou lorsqu'il en perd. La note explicative précise également que le score peut être négatif, comme indiqué dans l'exigence EF-07.4 et dans le critère d'acceptation de la manche à miser.

- **Responsabilité du calcul :** Nous avons placé la méthode calculer_score_miser dans la classe Score, car c'est cette classe qui est directement liée au résultat obtenu. Cela permet de garder le calcul au bon endroit et d'éviter de répartir cette logique dans plusieurs classes.

# Diagramme 8 : F-08 - Sauvegarder et restaurer les données
```mermaid
sequenceDiagram
    actor M as M. Mertens
    participant UI as ui : Interface
    participant SAUV as sauv : Sauvegarde
    participant CAFE as cafe : Cafe

    alt Action == Sauvegarder (EF-08.1)
        M->>UI: demander_sauvegarde(chemin_usb)
        activate UI
        UI->>SAUV: verifier_support_externe(chemin_usb)
        activate SAUV
        SAUV-->>UI: usb_disponible
        deactivate SAUV

        alt usb_disponible == false (EF-08.2)
            UI-->>M: message_erreur("Clé USB non connectée")
        else usb_disponible == true (EF-08.2, D-06)
            UI->>SAUV: exporter_donnees(cafe, chemin_usb)
            activate SAUV
            SAUV->>CAFE: serialiser_etat()
            activate CAFE
            CAFE-->>SAUV: donnees_completes (D-01 à D-05)
            deactivate CAFE
            SAUV-->>UI: confirmation_sauvegarde
            deactivate SAUV
            UI-->>M: message_succes("Sauvegarde effectuée sur clé USB")
        end
        deactivate UI

    else Action == Restaurer (EF-08.3)
        M->>UI: demander_restauration(chemin_fichier)
        activate UI
        UI->>SAUV: importer_donnees(chemin_fichier)
        activate SAUV
        SAUV->>CAFE: restaurer_etat(donnees_importees)
        activate CAFE
        CAFE-->>SAUV: confirmation_integrite (ENF-08)
        deactivate CAFE
        SAUV-->>UI: confirmation_restauration
        deactivate SAUV
        UI-->>M: message_succes("Données restaurées")
        deactivate UI
    end
```

- Utilisation de la classe Sauvegarde (D-06) : Nous avons choisi d'utiliser la classe Sauvegarde pour gérer l'importation et l'exportation des données. Elle provient directement de la section D-06 du cahier des charges. Cela permet d'éviter d'ajouter des éléments techniques comme « Système » ou « Système de fichiers » qui ne font pas partie de notre modèle.

- Vérification de la clé USB (EF-08.2) : Le bloc alt avec la condition usb_disponible == false permet de représenter le cas où aucune clé USB n'est détectée. Le programme affiche alors un message d'erreur pour prévenir l'utilisateur. Cette vérification permet de respecter l'exigence EF-08.2.

# Diagramme 9 : F-09 - Annuler la dernière modification
```mermaid
sequenceDiagram
    actor M as M. Mertens
    participant UI as ui : Interface
    participant CAFE as cafe : Cafe

    M->>UI: annuler_derniere_modification()
    activate UI

    UI->>CAFE: a_un_etat_precedent()
    activate CAFE
    CAFE-->>UI: bool_annulation_possible
    deactivate CAFE

    alt bool_annulation_possible == false (EF-09.1)
        UI-->>M: message_info("Aucune modification récente à annuler")
    else bool_annulation_possible == true (EF-09.1, RM-15)
        UI->>CAFE: restaurer_etat_precedent()
        activate CAFE
        Note over CAFE: Rétablissement de la copie temporaire (D-06)
        CAFE-->>UI: confirmation_annulation
        deactivate CAFE
        UI-->>M: actualiser_affichage_et_confirmer()
    end

    deactivate UI
```
- Gestion de l'historique temporaire (D-06, RM-15) : Nous avons choisi de confier cette responsabilité à l'objet principal Cafe. Avant chaque modification importante, il conserve une copie de l'état précédent grâce à la méthode sauvegarder_etat_temporaire(). Cela permet ensuite de revenir à la version précédente avec restaurer_etat_precedent() en cas d'erreur. De cette manière, l'interface n'a pas besoin de connaître la façon dont les données sont organisées pour effectuer un retour en arrière.