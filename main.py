import sys

QUESTIONNAIRES = {
    "QUIZ-MERTENS": [
        {
            "question": "Combien de points rapporte une bonne réponse en temps normal ?", 
            "reponse": "1"
        },
        {
            "question": "Quel est le nom du café où se déroule le quiz ?", 
            "reponse": "Comptoir des Curieux"
        },
        {
            "question": "Combien d'années faut-il attendre avant de réutiliser une question ?", 
            "reponse": "1"
        }
    ]
}

def main():
    print("==================================================")
    print("   Bienvenue au Quiz du Comptoir des Curieux !    ")
    print("==================================================\n")
    
    nom_equipe = input("Veuillez entrer le nom de votre équipe : ")
    
    cle_soiree = input("Veuillez entrer la clé donnée par M. Mertens : ")
    
    if cle_soiree not in QUESTIONNAIRES:
        print("\nClé invalide. Veuillez vérifier la clé avec le gérant et relancer le programme.")
        sys.exit()
        
    questions = QUESTIONNAIRES[cle_soiree]
    score = 0
    
    print(f"\n--- Début du Quiz pour l'équipe '{nom_equipe}' ! ---")
    print("Lisez attentivement et tapez votre réponse.\n")
    
    for idx, q in enumerate(questions, 1):
        print(f"Question {idx} : {q['question']}")
        reponse_utilisateur = input("Votre réponse : ")
        
        if reponse_utilisateur.strip().lower() == q['reponse'].strip().lower():
            score += 1 
        print("-" * 50)
            
    print("\n==================================================")
    print("                 FIN DE LA MANCHE                 ")
    print("==================================================")
    
    print(f"\nL'équipe '{nom_equipe}' a obtenu un score de : {score} point(s) !")
    print("M. Mertens va maintenant comparer les scores pour désigner le gagnant.")
    print("\nMerci d'avoir participé !")

if __name__ == "__main__":
    main()