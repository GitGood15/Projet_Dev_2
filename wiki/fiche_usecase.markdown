# Fiche F-01 : Gérer les équipes


| Rubrique | F-01 Gérer les équipes | Réf. CdC |
| -------- | ------- | ------- |
| Acteur | M. Mertens | F-01 |
| Précondition | L'application est ouverte (au début ou en dehors d'une soirée). | EF-01.0 |
| Scénario nominal | 1. M. Mertens identifie le chef d'équipe qui se présente. | EF-01.1 |
|  | 2. Le système affiche le profil du chef d'équipe. | EF-01.1 |
|  | 3. M. Mertens encode le nom de l'équipe choisi pour la soirée. | EF-01.2 |
|  | 4. M. Mertens encode le nombre de participants présent dans l'équipe (chef d'équipe inclus). | EF-01.3 |
|  | 5. Le système enregistre l'équipe et la rattache au profil du chef d'équipe. | D-01 |
| Alternative 1a | Le chef d'équipe n'est pas encore inscrit : M. Mertens enregistre d'abord son nouveau profil avant d'encoder l'équipe. | EF-01.0 |

| Alternative 3a | L'équipe change de nom par rapport à une soirée précédente : le système associe le nouveau nom au chef d'équipe existant pour préserver son historique. | RM-04, D-01 |

| Postcondition | L'équipe est enregistrée avec son nom de soirée, son nombre de joueurs et est associée de manière durable au profil du capitaine. | D-01 |

# Fiche F-02 : Gérer et importer les questions (Auteur : Ismail Mehane)

| Rubrique | F-02 Gérer et importer les questions | Réf. CdC |
| -------- | ------- | ------- |
Acteur | M. Mertens | F-02
Précondition | Aucune partie n'est en cours. | EF-02.1
Scénario nominal | 1. M. Mertens demande l'ajout d'une question au programme. | EF-02.1
| | 2. Le système affiche un formulaire permettant d'encoder une nouvelle question. | EF-02.1
|  | 3. M. Mertens encode la question, sa réponse et son niveau de difficulté (de 1 à 3). | EF-02.1
|  | 4. Le système vérifie si les informations saisies sont valides. | EF-02.1
|  | 5. Le système enregistre la question dans la banque de questions. | D-02
|  | 6. Le système confirme que la question est bien enregistrée. | EF-02.1
Alternative 1a | Une partie est en cours : le système refuse l'ajout et affiche un message demandant d'attendre la fin de la partie. | EF-02.1
Alternative 4a | Les informations saisies sont incorrectes : le système affiche un message d'erreur et demande de les corriger. | EF-02.1
Postcondition | La question, sa réponse et son niveau de difficulté sont enregistrés dans la banque de questions. | D-02


# Fiche F-03 : Organiser une soirée (Ilian Benzakour)

| Rubrique | F-03 — Organiser une soirée | Réf. CdC |
| -------- | ------- | ------- |
| **Acteur** | M. Mertens | F-03 |
| **Précondition** | Les équipes participantes sont enregistrées dans l'application et disposent d'un nom et d'un capitaine. | RM-03 |
| **Scénario nominal** | 1. M. Mertens ouvre la fonctionnalité « Organiser une soirée ». | F-03 |
|  | 2. Le système affiche le formulaire de création d'une soirée quiz. | F-03 |
|  | 3. M. Mertens définit le nombre de manches de la partie. | EF-03.1 |
|  | 4. M. Mertens définit le nombre de questions par manche. | EF-03.2 |
|  | 5. M. Mertens sélectionne les éventuelles manches spéciales. | F-03 |
|  | 6. M. Mertens sélectionne les équipes participantes à la partie. | EF-03.3, RM-03 |
|  | 7. Le système vérifie que les paramètres sont valides et qu'aucune équipe n'est inscrite deux fois à la même soirée. | EF-03.1, EF-03.2, EF-03.3 |
|  | 8. Le système crée la partie et enregistre les équipes participantes. | EF-03.3, RM-14 |
|  | 9. Le système confirme la création de la soirée à M. Mertens. | F-03 |
| **Alternative 7a** | Paramètres invalides : le système détecte des paramètres incorrects et affiche un message d'erreur à M. Mertens. Celui-ci corrige les informations et valide à nouveau. | EF-03.1, EF-03.2 |
| **Alternative 7b** | Équipe déjà inscrite : le système détecte qu'une équipe est déjà inscrite à la même soirée et affiche un message d'erreur à M. Mertens. Celui-ci doit modifier sa sélection avant de valider à nouveau. | EF-03.3 |
| **Postcondition** | La partie est créée et ses paramètres ainsi que les équipes participantes sont enregistrés dans la base de données. | EF-03.1, EF-03.2, EF-03.3, RM-14 |

# Fiche F-04 : Encoder les scores ainsi que les résultats

| Rubrique | F-04 Encoder les scores ainsi que les résultats | Réf. CdC |
| -------- | ------- | ------- |
Acteur | M. Mertens | F-04
Précondition | Une soirée quiz est en cours et une manche vient d'être corrigée par les équipes. | F-03, RM-06
Scénario nominal | 1. M. Mertens sélectionne une équipe et la manche correspondante. | EF-04.1
|  | 2. M. Mertens encode le score obtenu par l'équipe (1 point par bonne réponse). | EF-04.1, RM-09
|  | 3. Le système enregistre le score et met à jour le total de points de l'équipe. | D-04
|  | 4. Le système recalcule et met à jour automatiquement le classement provisoire de la soirée. | RM-07
|  | 5. À la fin de la soirée, le système ajoute le résultat global au profil du chef d'équipe. | EF-04.4, EF-01.4
Alternative 2a | Erreur de saisie : M. Mertens modifie un score déjà encodé ; le système valide la correction et actualise immédiatement le classement. | EF-04.2
Alternative 4a | Masquage du classement : M. Mertens choisit de masquer le classement durant la soirée ; le système enregistre les points sans les projeter. | EF-04.3
Postcondition | Les scores de la manche sont sauvegardés et le classement général de la soirée est à jour. | D-04, RM-07

# Fiche F-05 : Consulter le classement d'une soirée

| Rubrique | F-05 Consulter le classement d'une soirée | Réf. CdC |
| -------- | ------- | ------- |
Acteur | M. Mertens | F-05
Précondition | Au moins une soirée quiz est enregistrée dans le système. | D-03
Scénario nominal | 1. M. Mertens accède au module d'historique des soirées. | EF-05.1
|  | 2. M. Mertens saisit un critère de recherche (date, nom d'équipe ou nom d'un chef d'équipe). | EF-05.2, EF-05.3, EF-05.4
|  | 3. Le système filtre les enregistrements et affiche les soirées et équipes correspondantes. | EF-05.1
|  | 4. M. Mertens sélectionne une soirée pour consulter son classement détaillé et les scores par manche. | EF-05.1, D-04
Alternative 3a | Aucun résultat trouvé : le système affiche un message indiquant l'absence d'enregistrement correspondant aux critères de recherche. | EF-05.1
Postcondition | L'historique et les classements recherchés sont consultés sans altération des données enregistrées. | D-03, D-04

# Fiche F-06 : Gérer le championnat annuel (Auteur : Florent Chiappelloni)

| Rubrique | F-06 Gérer le championnat annuel | Réf. CdC |
| -------- | ------- | ------- |
| **Acteur** | M. Mertens | F-06 |
| **Précondition** | Une soirée quiz vient de se terminer et son classement final est validé. | F-04, EF-06.1 |
| **Scénario nominal** | 1. Le système attribue automatiquement les points de championnat à chaque équipe selon sa position finale lors de la soirée. | EF-06.2, RM-13 |
|  | 2. Le système associe ces points au capitaine représentatif de l'équipe. | RM-03, D-01 |
|  | 3. Le système filtre l'historique annuel de chaque capitaine pour ne conserver que ses 10 meilleurs scores. | EF-06.3, RM-12 |
|  | 4. Le système calcule la somme des 10 meilleurs résultats et met à jour le classement général du championnat. | EF-06.4 |
| **Alternative 4a** | Fin de saison / Clôture du championnat : M. Mertens demande la désignation du vainqueur. Le système affiche le capitaine en tête du classement annuel puis demande confirmation avant de remettre les points de championnat à zéro. | EF-06.5 |
| **Postcondition** | Le classement du championnat annuel est recalculé et sauvegardé dans le profil des capitaines. | D-05 |

# Fiche F-07 : Gérer les manches à miser (Auteur : Gildas Kockerols)

| Rubrique | F-07 Gérer les manches à miser | Réf. CdC |
| -------- | ------- | ------- |
| **Acteur** | M. Mertens | F-07 |
| **Précondition** | La soirée est en cours et M. Mertens lance la manche spéciale à miser. | EF-07.1, RM-10 |
| **Scénario nominal** | 1. M. Mertens sélectionne une équipe et saisit sa mise pour la question (valeur entre 1 et 5 points). | EF-07.2, RM-10 |
|  | 2. Il indique si la réponse donnée par l'équipe est correcte ou incorrecte. | RM-06 |
|  | 3. En cas de bonne réponse, le système ajoute le montant de la mise au score de la manche. | EF-07.3 |
|  | 4. En cas de mauvaise réponse, le système retranche le montant de la mise du score de l'équipe. | EF-07.4 |
|  | 5. Le système enregistre le nouveau solde et met à jour le classement. | D-04 |
| **Alternative 1a** | Mise supérieure au capital de points : L'équipe possède 2 points et mise 5 points. Le système accepte la mise sans restriction. | EF-07.2 |
| **Alternative 4a** | Basculement en score négatif : L'équipe échoue sur sa mise et la déduction rend son total inférieur à zéro. Le système autorise le résultat négatif et l'affiche au classement. | EF-07.4 |
| **Postcondition** | Les points de la manche à miser sont comptabilisés dans le total de la soirée pour chaque équipe participante. | D-04, ENF-05 |

# Fiche F-08 : Sauvegarder et restaurer les données

| Rubrique | F-08 Sauvegarder et restaurer les données | Réf. CdC |
| -------- | ------- | ------- |
Acteur | M. Mertens | F-08
Précondition | L'application est en cours d'exécution. | F-08
Scénario nominal | 1. M. Mertens demande la sauvegarde complète des données. | EF-08.1
|  | 2. Le système détecte la présence de la clé USB connectée à l'ordinateur. | EF-08.2
|  | 3. Le système génère une copie des données (équipes, questions, soirées, scores, championnat). | EF-08.1, D-06
|  | 4. Le système enregistre le fichier de sauvegarde sur la clé USB. | EF-08.2
|  | 5. Le système confirme à M. Mertens le succès de la sauvegarde. | EF-08.2
Alternative 2a | Clé USB non détectée : le système affiche un message d'erreur et interrompt la sauvegarde sur le support externe. | EF-08.2
Alternative 1a | Restauration des données : M. Mertens sélectionne une sauvegarde sur la clé USB ; le système restaure l'ensemble des données sélectionnées. | EF-08.3
Postcondition | Une copie de sauvegarde à jour des données de l'application est enregistrée sur la clé USB. | D-06, ENF-04

# Fiche F-09 : Annuler la dernière modification (Ilian Benzakour)

| Rubrique | F-09 Annuler la dernière modification | Réf. CdC |
| -------- | ------- | ------- |
Acteur | M. Mertens | F-09
Précondition | Au moins une modification de données a été effectuée durant la session active. | F-09, RM-15
Scénario nominal | 1. M. Mertens demande l'annulation de la dernière manipulation. | EF-09.1
|  | 2. Le système récupère l'état des données précédent la modification. | D-06
|  | 3. Le système restaure les données à cet état antérieur. | EF-09.1
|  | 4. Le système réactualise l'affichage et confirme le rétablissement de l'état précédent. | EF-09.1
Alternative 1a | Aucune modification récente : le système signale à M. Mertens qu'aucune action ne peut être annulée. | EF-09.1
Postcondition | L'application est rétablie exactement dans l'état où elle se trouvait avant la dernière modification. | RM-15, D-06