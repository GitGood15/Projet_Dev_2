---
creation-date: 2026-10-11
---
# Cahier des charges - Application de gestion d'une soirée quiz

Certaines phrases de ce document ont été reformulées avec l’aide d’une intelligence artificielle afin d’améliorer leur clarté et leur formulation. Le contenu et les choix du projet restent le fruit de notre travail.

# Informations sur le document

- **Titre :** Application de gestion d'une soirée quiz
- **Auteurs :** 2TL1-1
- **Validation par le client :** xxx

| Version | Date | Modification |
| --- | --- | --- |
| 1.0 | 10/10 | Première version, après l'entretien avec le gérant du café |

## Conventions d'identification

| Élément | Format | Exemple |
| --- | --- | --- |
| Règle métier | RM-xx | RM-01 |
| Donnée | D-xx | D-02 |
| Fonctionnalité | F-xx | F-03 |
| Exigence fonctionnelle | EF-xx.y (xx = numéro de la fonctionnalité) | EF-03.2 |
| Exigence non fonctionnelle | ENF-xx | ENF-04 |

# 1. Contexte

## 1.1. Présentation du client / de l'entreprise

Le Comptoir des Curieux est un café situé à Louvain-la-Neuve, représenté par M. Mertens, qui organise chaque semaine des soirées quiz. Ces soirées réunissent généralement entre 10 et 16 équipes qui s'affrontent sur plusieurs manches.

M. Mertens prépare les questions, anime les soirées et assure le suivi des scores et du classement. Il souhaite simplifier l'organisation de ces événements tout en conservant leur ambiance conviviale et compétitive.

## 1.2. Présentation du projet

**Situation actuelle.** Les questions sont préparées et projetées avec PowerPoint. Les équipes inscrivent leurs réponses sur papier, puis corrigent celles des autres équipes. Gaët récupère les scores et établit manuellement le classement. La manche à miser nécessite également un suivi particulier des mises et des points gagnés ou perdus.

Cette organisation pose plusieurs problèmes :

* les calculs manuels entraînent des risques d'erreurs et ralentissent les soirées ;
* la préparation des questions est longue, notamment lorsqu'elles proviennent de fichiers PowerPoint ou Excel ;
* le suivi du championnat annuel, basé sur les dix meilleurs résultats de chaque équipe, demande du temps ;
* les changements de nom des équipes compliquent la conservation de leur historique.

**Parties prenantes**

| Parties prenantes | Rôle |
| --- | --- |
| M. Mertens, gérant du café | Client et utilisateur principal. Définit les besoins et valide la solution. |
| Équipes participantes | Bénéficiaires indirects du système, grâce à un suivi plus fiable des scores.  |
| Groupe 2TL1-1 (étudiants) | Prestataire. Réalise l'application. |

**Grandes lignes du projet.** Développer une application permettant de gérer les équipes, les scores, les mises et les classements. PowerPoint sera conservé pour projeter les questions, les images et la musique. L'application fonctionnera sur l'ordinateur du café, sans dépendre d'Internet, et permettra de sauvegarder les données sur une clé USB.

## 1.3. Objectifs du projet 

1. **Automatisation des scores :** calculer automatiquement les points des équipes, y compris ceux de la manche à miser.
2. **Classement automatique :** mettre à jour le classement de chaque soirée dès que les scores sont modifiés.
3. **Gestion des questions :** faciliter l'importation et l'organisation des questions et éviter leur réutilisation avant un an.
4. **Suivi des équipes :** conserver l'historique des résultats malgré les changements de nom des équipes.
5. **Gestion du championnat :** calculer automatiquement le classement annuel en retenant les dix meilleurs résultats de chaque équipe.
6. **Protection des données :** sauvegarder les données et permettre d'annuler la dernière modification en cas d'erreur.

**Plus-value attendue.** Réduction du temps consacré aux calculs et à la préparation, diminution des erreurs de classement et meilleure gestion du championnat annuel. Gaët pourra ainsi se concentrer davantage sur l'animation des soirées.

**Risques en cas de non-réalisation, alternatives.** Les calculs manuels, les risques d'erreurs et les difficultés de suivi du championnat persisteront. Le maintien de PowerPoint et des méthodes actuelles reste possible, mais ne résout pas ces problèmes.

# 2. Description générale

## 2.1. Vue d'ensemble du produit et de son environnement

L'application sera utilisée par M. Mertens depuis l'ordinateur du Comptoir des Curieux. Elle permettra de gérer les équipes, les questions, les scores des soirées et le classement du championnat annuel.

Le café utilise actuellement PowerPoint pour préparer et projeter les questions. Celui-ci sera conservé pour afficher les questions, les images et diffuser la musique. L'application fonctionnera localement, sans connexion Internet obligatoire. Les données seront enregistrées automatiquement sur l'ordinateur et pourront être sauvegardées sur clé USB.

## 2.2. Profils utilisateurs (acteurs)

| Acteur | Description |
| --- | --- |
| M. Mertens | Responsable du café et utilisateur principal. Prépare et anime les quiz, encode les scores et consulte les classements. |
| Équipes participantes | Participent aux soirées quiz. Elles bénéficient d'un calcul plus fiable des scores et d'un suivi du championnat.  |
| Groupe 2TL1-1 (étudiants) | Conçoit, développe et teste l'application selon les besoins exprimés par M. Mertens. |

## 2.3. Périmètre

**Inclus :**
* La gestion des équipes et de leurs capitaines.
* La gestion et l’importation des questions depuis des fichiers.
* Le suivi de l’historique des questions et la prévention de leur réutilisation pendant un an.
* L’encodage et le calcul automatique des scores, y compris ceux de la manche à miser.
* L’affichage du classement de chaque soirée.
* Le calcul du classement annuel en retenant les dix meilleurs résultats de chaque équipe.
* La sauvegarde des données et l’annulation de la dernière modification.

**Exclus :**
* Le remplacement de PowerPoint pour la projection des questions, des images et de la musique.
* La nécessité d’une connexion Internet ou d’un service en ligne pour utiliser l’application.

## 2.4. Règles métier

- *RM-01 : Une partie dure environ 2 h 30, cette partie est divisée en 6 manches de 8 questions.*
- *RM-02 : La soirée quiz se déroulera chaque mardi de 20 h à 22 h 30.*
- *RM-03 : Une équipe est représentée par un nom ainsi qu'un capitaine.*
- *RM-04 : Une équipe peut changer de nom, elle reste la même équipe et son historique est conservé.*
- *RM-05 : Une question a un délai d'un an avant de pouvoir être reposée.*
- *RM-06 : Les équipes corrigent les réponses des autres et les scores sont ensuite encodés dans l'application.*
- *RM-07 : Le classement final est établi selon le nombre de points accumulés à chaque manche.*
- *RM-08 : Si 2 équipes sont à égalité, une question subsidiaire sort pour départager les équipes.*
- *RM-09 : Une bonne réponse rapporte 1 point. Une mauvaise réponse ne fait perdre aucun point, sauf dans les manches à miser.*
- *RM-10 : Lors de la manche à miser, chaque équipe mise entre 1 et 5 points par question. Une bonne réponse rapporte le montant misé et une mauvaise réponse le fait perdre.*
- *RM-11 : Le nombre d'équipes participantes est généralement compris entre 10 et 16. Des équipes peuvent être ajoutées en cours de soirée.*
- *RM-12 : Le classement du championnat annuel est calculé à partir des dix meilleurs résultats de chaque équipe.*
- *RM-13 : Le classement d’une soirée attribue des points de championnat selon la position obtenue. Le premier reçoit 20 points, puis les points diminuent de 2 en 2 jusqu’à atteindre un minimum de 5 points pour la dernière place. La répartition exacte lorsque le nombre d’équipes varie reste à confirmer avec le client.*
- *RM-14 : Les données doivent être enregistrées automatiquement pendant l’utilisation. Une sauvegarde manuelle sur clé USB doit également être possible, avec un rappel à la fin de chaque soirée.*
- *RM-15 : L’utilisateur doit pouvoir annuler sa dernière modification en cas d’erreur d’encodage.*


## 2.5. Données

**D-01 Équipe**

* _Contenu :_ identifiant unique, nom de l’équipe pour la soirée, chef d’équipe et nombre de participants.
* _Volume :_ environ 10 à 16 équipes par soirée.
* _Origine :_ chefs d’équipe déjà enregistrés ou créés par M. Mertens au début de leur participation.
* _Conservation :_ les informations permettent de conserver l’historique des résultats d’un chef d’équipe, même si le nom de son équipe change.

| *Opération* | *Acteur* | *Fonctionnalité* |
| --- | --- | --- |
| Créer un chef d’équipe | M. Mertens | F-01 |
| Identifier un chef d’équipe | M. Mertens | F-01 |
| Encoder le nom de l’équipe | M. Mertens | F-01 |
| Encoder le nombre de participants | M. Mertens | F-01 |
| Consulter l’historique des résultats | M. Mertens | F-05, F-06 |

**D-02 Question**

* _Contenu :_ énoncé, réponse attendue, thème, niveau de difficulté de 1 à 3 et historique d’utilisation.
* _Origine :_ questions créées par M. Mertens ou reçues dans des fichiers PowerPoint ou Excel.
* _Conservation :_ les questions utilisées sont conservées dans l’historique afin d’éviter leur réutilisation pendant un an.

| Opération | Acteur | Fonctionnalité |
|---|---|---|
| Ajouter une question | M. Mertens | F-02 |
| Consulter les questions | M. Mertens | F-02 |
| Retirer une question du programme | M. Mertens | F-02 |
| Importer des questions | M. Mertens | F-02 |
| Enregistrer l’utilisation d’une question | Automatique | F-02 |

**D-03 Soirée quiz**

* _Contenu :_ date, équipes participantes, nombre de manches, nombre de questions par manche et résultats de la soirée.
* _Origine :_ soirées créées et configurées par M. Mertens.
* _Conservation :_ les soirées sont conservées pour permettre la consultation de l’historique et le suivi du championnat annuel.

| *Opération* | *Acteur* | *Fonctionnalité* |
| --- | --- | --- |
| Créer une soirée | M. Mertens | F-03 |
| Configurer le nombre de manches | M. Mertens | F-03 |
| Configurer le nombre de questions par manche | M. Mertens | F-03 |
| Inscrire les équipes participantes | M. Mertens | F-01, F-03 |
| Consulter l’historique des soirées | M. Mertens | F-05 |
| Rechercher une soirée par date | M. Mertens | F-05 |
| Consulter les équipes et leurs résultats | M. Mertens | F-05 |

**D-04 Score**

* _Contenu :_ équipe concernée, soirée, manche, points obtenus et, pour la manche à miser, mise et résultat de la question.
* _Origine :_ scores encodés par M. Mertens à la fin de chaque manche après la correction des réponses.
* _Particularité :_ le classement peut être affiché ou masqué pendant la soirée. Les scores peuvent être corrigés en cas d’erreur.

| *Opération* | *Acteur* | *Fonctionnalité* |
| --- | --- | --- |
| Encoder les scores | M. Mertens | F-04 |
| Calculer les scores | Automatique | F-04, F-07 |
| Consulter les résultats | M. Mertens | F-04, F-05 |
| Modifier un score | M. Mertens | F-04 |
| Afficher ou masquer le classement | M. Mertens | F-04 |
| Ajouter les points au profil du chef d’équipe | Automatique | F-01, F-04, F-06 |
| Ajouter ou retirer les points liés à une mise | Automatique | F-07 |

**D-05 Championnat annuel**

* _Contenu :_ chefs d’équipe, résultats des soirées et total des points du championnat.
* _Calcul :_ le classement est établi à partir des points accumulés par les chefs d’équipe au cours de l’année, selon les règles définies pour le championnat.
* _Conservation :_ les résultats sont conservés pour permettre le suivi du championnat annuel.

| *Opération* | *Acteur* | *Fonctionnalité* |
| --- | --- | --- |
| Mettre à jour les points du championnat | Automatique | F-06 |
| Comparer les points des chefs d’équipe | Automatique | F-06 |
| Consulter l’historique des résultats | M. Mertens | F-05, F-06 |
| Déterminer le gagnant du championnat | M. Mertens | F-06 |
| Remettre les points à zéro à la fin du championnat | Automatique, après validation | F-06 |

**D-06 Sauvegarde**

* _Contenu :_ données de l’application, notamment les équipes, les questions, les soirées, les scores et les résultats du championnat.
* _Destination :_ clé USB connectée à l’ordinateur du café.
* _Fonctionnement :_ M. Mertens peut effectuer une sauvegarde quand il le souhaite et autant de fois que nécessaire.

| *Opération* | *Acteur* | *Fonctionnalité* |
| --- | --- | --- |
| Créer une sauvegarde | M. Mertens | F-08 |
| Enregistrer la sauvegarde sur une clé USB | Automatique | F-08 |
| Annuler la dernière modification | M. Mertens | F-09 |

# 3. Exigences

## 3.1. Exigences fonctionnelles

| ID     | Fonctionnalité            | Acteur(s) | Priorité        |
| ------ | ------------------------- | --------- | --------------- |
| *F-01* | *Gérer les équipes*       | *M. Mertens* | *Indispensable* |
| *F-02* | *Gérer et importer les questions* | *M. Mertens*| *Indispensable*|
| *F-03* | *Organiser une soirée*    | *M. Mertens*| *Souhaitable*|
| *F-04* | *Encoder les scores ainsi que les résultats*| *M. Mertens*| *Indispensable*|
| *F-05* | *Consulter le classement d'une soirée*| *M. Mertens*| *Indispensable* |
| *F-06* | *Gérer le championnat annuel*| *M. Mertens*| *Indispensable* |
| *F-07* | *Gérer les manches à miser*| *M. Mertens*| *Indispensable* |
| *F-08* | *Sauvegarder et restaurer les données*| *M. Mertens*| *Indispensable* |
| *F-09* | *Annuler la dernière modification* | *M. Mertens*| *Souhaitable* |

### F-01 — Gérer les équipes (Ilian Benzakour)

**Acteur(s) :** *M. Mertens* 

**Priorité :** *indispensable*

#### Description

*Au début de chaque soirée quiz, les chefs d'équipe viendront s'identifier chez M. Mertens et donneront leur nom d'équipe du soir. Ils devront aussi indiquer le nombre de participants dans leur équipe (sans oublier de se compter eux-mêmes). À la fin de chaque soirée, le nombre de points accumulés par l'équipe sera ajouté au profil du chef d'équipe. Ainsi, le suivi des équipes sera moins hasardeux.*

#### Exigences
- *EF-01.0 Les chefs d'équipe non inscrits dans le programme vont chez M. Mertens pour qu'il les enregistre dans le système.*
- *EF-01.1 Les chefs d'équipe vont s'identifier chez M. Mertens.*
- *EF-01.2 M. Mertens encode le nom de l'équipe pour la soirée.*
- *EF-01.3 M. Mertens encode le nombre de joueurs présents dans l'équipe (ne pas oublier de compter le chef).*
- *EF-01.4 À la fin de la partie, les points des équipes sont ajoutés aux profils des chefs d'équipe.*

#### Critères d'acceptation

- *EF-01.0 : Une personne non inscrite souhaiterait participer à la soirée quiz avec son équipe. Elle se rend chez M. Mertens et il l'enregistre dans le programme.*
- *EF-01.1 : Un chef d'équipe déjà inscrit se rend chez M. Mertens et s'identifie chez lui.*
#### Données impliquées


__*La fonctionnalité F-01*__
- *Créer un nouveau chef d'équipe (D-01) ;*
- *Identifier un chef d'équipe (D-01) ;*
- *Changer le nom de l'équipe (D-01).*


### F-02 — Gérer et importer les questions (Ismail Mehane)

**M. Mertens :** **Indispensable :**

#### Description
*Permet à M. Mertens d'encoder ses questions dans le programme ou de les retirer si besoin. Les réponses aussi doivent être encodées avec la question. On demande aussi le niveau de difficulté de la question, de 1 à 3. Aussi, lorsqu'une question est posée, elle ne pourra plus être choisie avant 1 an.*
#### Exigences
- *EF-02.1 M. Mertens doit pouvoir encoder des questions ainsi que leur réponse, en précisant le niveau de difficulté allant de 1 à 3, en dehors d'une partie.*
- *EF-02.2 M. Mertens doit pouvoir supprimer une question du programme en dehors d'une partie.*
- *EF-02.3 Une question posée ne peut plus revenir avant 1 an.*
#### Critères d'acceptation
- *EF-02.1 Si M. Mertens tente d'ajouter une question au programme durant une partie, le programme l'en empêchera et lui rappellera qu'il faut attendre la fin de la partie avant de pouvoir en ajouter une.*
- *EF-02.2 Si M. Mertens tente de supprimer une question du programme durant une partie, le programme l'en empêchera et lui rappellera qu'il faut attendre la fin de la partie avant de pouvoir en supprimer une.*
- *EF-02.3 Si une question est posée, elle sera retenue par le programme et ne sera plus posée avant 1 an.*
#### Données impliquées
__*La fonctionnalité F-02*__
- *Ajouter une question au programme (D-02).*
- *Retirer une question du programme (D-02).*
- *Retenir les questions posées et ne plus les utiliser avant 1 an (D-02).*
#### Maquettes



### F-03 — Organiser une soirée (Ilian Benzakour)

**M. Mertens :** **Souhaitable :**

#### Description
*Pouvoir personnaliser une partie de quiz en modifiant le nombre de manches, le nombre de questions par manche et quelles manches spéciales seront choisies. Choisir quelles équipes jouent la partie.*
#### Exigences
- *EF-03.1 M. Mertens peut décider du nombre de manches par partie.*
- *EF-03.2 M. Mertens peut décider du nombre de questions par manche.*
- *EF-03.3 M. Mertens note les équipes participantes à la partie.*

#### Critères d'acceptation
- *EF-03.1 : Vérifier que M. Mertens peut définir le nombre de manches d’une soirée.*
- *EF-03.2 : Vérifier que M. Mertens peut définir le nombre de questions par manche.*
- *EF-03.3 : Vérifier qu’une équipe ne peut pas être inscrite deux fois à la même soirée.*

#### Données impliquées
__*La fonctionnalité F-03*__
- *Paramétrer le nombre de manches (D-03).*
- *Paramétrer le nombre de questions par manche (D-03).*
- *Inscrire les équipes participantes à la partie (D-01).*
- *Créer une partie (D-03).*


#### Maquettes


### F-04 — Encoder les scores (Ilian Benzakour)

**M. Mertens :** **Indispensable :**

#### Description
*Les scores de chaque équipe seront encodés par M. Mertens à la fin de chaque manche après la correction par les équipes elles-mêmes. M. Mertens aura le pouvoir d'afficher ou non le classement quand il le souhaite.*
#### Exigences
- *EF-04.1 M. Mertens encode les scores de chaque équipe à la fin de chaque manche.*
- *EF-04.2 M. Mertens doit pouvoir modifier les scores après les avoir entrés en cas d'erreurs.*
- *EF-04.3 M. Mertens doit pouvoir afficher/cacher le classement quand il le souhaite durant la partie.*
- *EF-04.4 À la fin de la partie, les points accumulés par les équipes sont ajoutés au profil du chef d'équipe pour les sauvegarder.*


#### Critères d'acceptation
- *EF-04.1 : Vérifier que les scores encodés sont enregistrés pour la bonne équipe et la bonne manche.*
- *EF-04.2 : Vérifier qu’une modification de score entraîne la mise à jour du classement.*
- *EF-04.3 : Vérifier que M. Mertens peut afficher et masquer le classement pendant la soirée.*
- *EF-04.4 : Vérifier que le résultat de la soirée est enregistré dans l’historique de l’équipe concernée.*

#### Données impliquées
__*La fonctionnalité F-04*__
- *Comptabiliser les scores des équipes (D-04).*
- *Modifier les scores en cas d'erreur lors de l'encodage (D-04).*
- *Ajouter le score total de l'équipe au profil du chef d'équipe pour le sauvegarder (D-01).*
- *Montrer/cacher le classement durant la partie (D-04).*


#### Maquettes

### F-05 — Consulter le classement d'une soirée (Ilian Benzakour)

**M. Mertens :** **Indispensable :**

#### Description
*M. Mertens pourra consulter l'historique de ses soirées quiz. Il pourra voir quelles équipes y ont participé, et combien de points ont eu ces équipes.*
#### Exigences
- *EF-05.1 L'historique des parties sera disponible via une interface.*
- *EF-05.2 M. Mertens pourra effectuer ses recherches avec une date.*
- *EF-05.3 M. Mertens pourra effectuer ses recherches avec le nom d'une équipe.*
- *EF-05.4 M. Mertens pourra effectuer ses recherches avec le profil d'un chef d'équipe.*

#### Critères d'acceptation
- *EF-05.1 : Vérifier que M. Mertens peut consulter l’historique des soirées.*
- *EF-05.2 : Vérifier qu’une recherche par date affiche les soirées correspondantes.*
- *EF-05.3 : Vérifier qu’une recherche par nom d’équipe affiche les résultats correspondants.*
- *EF-05.4 : Vérifier qu’une recherche par profil de capitaine affiche l’historique associé.*

#### Données impliquées
__*La fonctionnalité F-05*__
- *EF-05.1 Recherche via une interface (D-03).*
- *EF-05.2 Recherche via une date (D-03).*
- *EF-05.3 Recherche via le nom d'une équipe (D-03).*
- *EF-05.4 Recherche via le profil d'un chef d'équipe (D-03).*



#### Maquettes


### F-06 — Gérer le championnat annuel (Chiappelloni Florent)

**M. Mertens :** **Indispensable :**

#### Description
*M. Mertens souhaite organiser un championnat annuel afin de récompenser l’équipe ayant obtenu les meilleurs résultats au cours de l’année. Le classement annuel est calculé à partir des dix meilleurs résultats de chaque équipe. Les points de championnat attribués à chaque soirée dépendent de la position finale obtenue. Le gagnant du championnat est déterminé à la fin de l’année.*
#### Exigences
- *EF-06.1 À la fin d’une soirée quiz, le système enregistre le résultat de chaque équipe.*
- *EF-06.2 Le système attribue les points de championnat selon le classement final de la soirée.*
- *EF-06.3 Le système calcule le classement annuel en retenant les dix meilleurs résultats de chaque équipe.*
- *EF-06.4 M. Mertens peut consulter le classement du championnat annuel.*
- *EF-06.5 À la fin du championnat, le système permet de déterminer l’équipe gagnante et de remettre à zéro les points du championnat après validation.*

#### Critères d'acceptation
- *EF-06.2 : Vérifier que les points de championnat attribués correspondent à la position obtenue lors de la soirée.*
- *EF-06.3 : Vérifier que seuls les dix meilleurs résultats sont retenus dans le calcul du classement annuel.*
- *EF-06.4 : Vérifier que M. Mertens peut consulter les équipes classées selon leurs points de championnat.*
- *EF-06.5 : Vérifier que le gagnant peut être déterminé une seule fois par année et que la remise à zéro intervient après validation.*

#### Données impliquées
__*La fonctionnalité F-06*__
- *Résultats des soirées (D-03).*
- *Scores des équipes (D-04).*
- *Résultats et points du championnat annuel (D-05).*

### F-07 — Gérer les manches à miser (Gildas Kockerols)

**M. Mertens :** **Indispensable :**

#### Description
*M. Mertens a mis en place cette manche pour ajouter du piment. Il n'y en a qu'une par soirée et elle consiste à ce que chaque équipe mise entre 1 et 5 points avant de pouvoir répondre à la question. Si elle gagne, elle gagne le nombre de points qu'elle a misés, sinon elle les perd. Cela implique qu'une équipe peut tomber en négatif.*
#### Exigences
- *EF-07.1 M. Mertens doit pouvoir lancer cette manche quand il le souhaite durant la soirée.*
- *EF-07.2 Chaque équipe mise entre 1 et 5 points.*
- *EF-07.3 L'équipe qui répond correctement gagne sa mise.*
- *EF-07.4 L'équipe qui ne répond pas correctement perd sa mise.*

#### Critères d'acceptation
- *EF-07.2 Une équipe ayant 2 points peut quand même miser 5 points.*
- *EF-07.4 Si l'équipe perd plus de points que ce qu'elle avait déjà, elle sera en négatif.*

#### Données impliquées
__*La fonctionnalité F-07*__
- *Ajouter ou retirer les points liés à une mise (D-04).*

### F-08 — Sauvegarder et restaurer les données (Ilian Benzakour)
**M. Mertens :** **Indispensable :**

#### Description
*M. Mertens souhaite faire une sauvegarde quand il le souhaite et la mettre sur une clé USB. Cette sauvegarde prend en compte toutes les stats des équipes, les scores, le classement, etc.*
#### Exigences
- *EF-08.1 M. Mertens doit pouvoir effectuer une sauvegarde de toutes les données de l’application quand il le souhaite et autant de fois qu’il le souhaite.*
- *EF-08.2 Le système doit enregistrer la sauvegarde sur une clé USB connectée à l’ordinateur.*
- *EF-08.3 M. Mertens doit pouvoir restaurer les données de l’application à partir d’une sauvegarde existante.*

#### Critères d'acceptation
- *EF-08.1 : Vérifier qu’une sauvegarde peut être effectuée à la demande de M. Mertens.*
- *EF-08.2 : Vérifier qu’une sauvegarde est créée sur la clé USB et qu’un message indique si la clé USB n’est pas connectée.*
- *EF-08.3 : Restaurer une sauvegarde et vérifier que les équipes, questions, soirées, scores et résultats du championnat sont récupérés.*


#### Données impliquées
__*La fonctionnalité F-08*__ 
- *Faire une sauvegarde de toutes les données (D-01, D-02, D-03, D-04, D-05).*

### F-09 — Annuler la dernière modification (Ilian Benzakour)

**M. Mertens :** **Souhaitable :**

#### Description
*En cas d'erreur de manipulation, M. Mertens va pouvoir annuler la dernière modification et restaurer la version précédente.*
#### Exigences
- *EF-09.1 En cas d'erreur de manipulation, M. Mertens doit être capable d'annuler sa modification et de restaurer l'état précédent du programme.*

#### Critères d'acceptation


#### Données impliquées
__*La fonctionnalité F-09*__
- *État précédent des données de l’application, conservé temporairement afin de permettre l’annulation de la dernière modification.*

## 3.2. Exigences non fonctionnelles

| ID | Exigence | Vérification |
| --- | --- | --- |
| ENF-01 | **Fonctionnement hors ligne :** l’application fonctionne sans connexion Internet et permet d’utiliser ses fonctionnalités principales pendant une soirée quiz. | Déconnecter l’ordinateur d’Internet et tester la gestion des équipes, l’encodage des scores et la consultation du classement. |
| ENF-02 | **Installation locale :** l’application est installée et utilisable sur l’ordinateur du café, sans dépendre d’un serveur distant. | Installer et lancer l’application sur l’ordinateur prévu pour les soirées quiz, sans connexion Internet. |
| ENF-03 | **Sauvegarde automatique :** les modifications apportées aux données sont enregistrées automatiquement afin de limiter les pertes en cas de fermeture de l’application. | Modifier un score, fermer puis relancer l’application et vérifier que la modification est conservée. |
| ENF-04 | **Sauvegarde externe :** l’utilisateur peut sauvegarder les données sur une clé USB et reçoit un rappel à la fin de chaque soirée quiz. | Réaliser une sauvegarde sur une clé USB et vérifier que le rappel apparaît à la fin d’une soirée. |
| ENF-05 | **Fiabilité des calculs :** les calculs des scores et des classements sont corrects, y compris lors de la manche à miser lorsque le score d’une équipe devient négatif. | Tester plusieurs situations avec des réponses correctes et incorrectes, différentes mises et des scores positifs ou négatifs, puis comparer les résultats obtenus aux résultats attendus. |
| ENF-06 | **Facilité d’utilisation :** M. Mertens doit pouvoir encoder les scores d’une manche et consulter le classement sans assistance après une courte présentation de l’application. | Faire réaliser ces opérations à M. Mertens lors de la recette du MVP et vérifier qu’il peut les terminer sans aide. |
| ENF-07 | **Compatibilité avec PowerPoint :** l’application peut être utilisée en parallèle de PowerPoint, qui reste nécessaire pour projeter les questions, les images et les contenus audio. | Lancer l’application et un fichier PowerPoint sur l’ordinateur du café, puis vérifier que les deux peuvent être utilisés pendant une soirée quiz. |
| ENF-08 | **Intégrité des données :** les informations relatives aux équipes, aux questions, aux scores et au championnat restent cohérentes après une modification, une sauvegarde ou une restauration. | Effectuer des modifications, sauvegarder les données, les restaurer et vérifier que les informations conservées sont cohérentes et complètes. |

# 4. Contraintes

Le projet doit respecter les contraintes suivantes :
* L’application doit fonctionner localement sur l’ordinateur du café, sans dépendre d’une connexion Internet.
* PowerPoint doit rester utilisable pour projeter les questions, les images et diffuser la musique.
* Les données doivent pouvoir être sauvegardées sur une clé USB.

# 5. Budget

Le développement de ce projet se fait dans le cadre d'un projet étudiant, il n'y a donc pas de coût à prévoir pour le gérant du bar. La charge de travail est encore à déterminer.

# 6. Livrables et planning

## 6.1. Livrables

Le MVP est un programme en ligne de commandes destiné aux participants qui permet d'indiquer leurs équipe(F-01), une clé donnée par le gérant permettrait a tout le monde d'avoir le même questionnaire (F-03), répondre a une série de questions(F-02) et afficher les points (F-04), le gérant n'aurais plus qu'a comparer les points pour designer le gagnant

En fin de compte le client, M. Mertens, souhaite avoir un exécutable prêt à l'emploi .

## 6.2. Échéances

Le client récupèrera la version finale du projet courant la semaine du 7 décembre.

## 6.3. Retours vers le client

Le client veut juste être tenu au courant de l'évolution du projet sur un rythme bimensuel.

# 7. Validation du projet

Le client nous laissant carte blanche sur l'avancement, la validation de la version finale est effectuée par M. Mertens le 8 décembre.
Les retours de M. Mertens des réunions bimensuelles sont traités en interne et discutés avec le client lors de la prochaine réunion.

Les principaux éléments vérifiés seront la gestion des équipes et des questions, l’encodage des scores, le calcul des classements, la gestion du championnat annuel, la sauvegarde des données et le fonctionnement hors ligne de l’application.


# 8. Maintenance *(optionnel)*

Aucune maintenance prévue étant donné la nature du projet.

# 9. Questions ouvertes

| *ID* | *Question* | *À poser à* | *Éléments impactés* | *Statut* |
| --- | --- | --- | --- | --- |
| Q-01 | Le championnat annuel est-il calculé sur les 10 meilleurs résultats de chaque équipe ou sur l’ensemble des résultats de l’année ?                                  | M. Mertens | RM-12, D-05, F-06              | Ouverte |
| Q-02 | Quel est le barème exact des points attribués selon le classement d’une soirée, en fonction du nombre d’équipes participantes ?                                    | M. Mertens | RM-13, D-05, F-06              | Ouverte |
| Q-03 | Comment conserver l’historique et les points lorsqu’une équipe change de nom ou de capitaine ?                                                                     | M. Mertens | RM-03, RM-04, D-01, F-01, F-06 | Ouverte |
| Q-04 | Quels formats de fichiers doivent être pris en charge pour les questions : PowerPoint, Excel ou les deux ?                                                         | M. Mertens | D-02, F-02, F-03               | Ouverte |
| Q-05 | Faut-il permettre de restaurer une sauvegarde depuis une clé USB, ou uniquement de sauvegarder les données sur celle-ci ?                                          | M. Mertens | D-06, F-08, ENF-04, ENF-08     | Ouverte |
| Q-06 | Lorsqu’une équipe rejoint le quiz en cours de soirée, comment son score et son classement final sont-ils calculés si elle n’a pas participé à toutes les manches ? | M. Mertens | RM-11, D-03, D-04, F-03, F-04  | Ouverte |

# 10. Glossaire

| *Terme* | *Définition* |
| --- | --- |
| Quiz | Soirée de questions-réponses organisée au Comptoir des Curieux. |
| Manche | Partie du quiz composée d’un ensemble de questions. Une soirée comporte généralement six manches de huit questions. |
| Équipe | Groupe de participants qui répond ensemble aux questions et dont les résultats sont enregistrés pour chaque soirée. |
| Capitaine | Personne représentant une équipe et permettant de retrouver son historique et ses résultats. |
| Manche de pari | Manche spéciale durant laquelle une équipe mise entre 1 et 5 points sur une réponse. Elle gagne sa mise si sa réponse est correcte et la perd dans le cas contraire. |
| Difficulté | Niveau attribué à une question, compris entre 1 et 3. |
| Classement de la soirée | Classement des équipes établi selon le total de points obtenu pendant une soirée. |
| Championnat annuel | Classement général établi à partir des résultats des soirées organisées au cours de l’année, selon les règles définies par le client. |
| Sauvegarde | Copie des données de l’application permettant de conserver les informations et de les protéger contre une perte de données. |
| Annulation d’une modification | Fonction permettant de revenir sur la dernière modification effectuée dans l’application. |

# Annexes

Maquettes détaillées, exemples de données, schémas, comptes rendus ou transcripts des échanges avec le client, ...
