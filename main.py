import random as rd
import json

if __name__ == "__main__":
    team = input("Entrez le nom de l'équipe : ")
    seed = int(input("Entrez la seed : "))
    score = 0
    streak = 1

    while seed < 1000 or seed > 9999:
        print("La seed doit être composée de 4 chiffres.")
        seed = int(input("Entrez la seed : "))

    rd.seed(seed)
    nbquestion = (seed % 10 + 1) * 10 #determination du nombre de questions à partir de la seed
    score_max = 100 * (1.1 ** nbquestion - 1)
    
    # Extraction, randomisation et coupure du questionnaire
    with open("questionnaire.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    rd.shuffle(data)
    data = data[:nbquestion]

    for i in range(len(data)):

        print(f"\nQuestion {i+1} : {data[i]['difficulte']}, {data[i]['domaine']}")
        print(f"{data[i]['question']}")
        print(f"A : {data[i]['a']}")
        print(f"B : {data[i]['b']}")
        print(f"C : {data[i]['c']}")
        print(f"D : {data[i]['d']}")
        answer = input("Entrez réponse (A, B, C ou D) : ").lower()

        while answer not in ['a', 'b', 'c', 'd']:
            print("Réponse invalide. Veuillez entrer A, B, C ou D.")
            answer = input("Entrez réponse (A, B, C ou D) : ").lower()

        if answer == data[i]['reponse']:
            print("Bonne réponse !\n")
            score += 10 * (1.1 ** (streak - 1))  
            streak += 1
        else:
            print(f"Mauvaise réponse. La bonne réponse était : {data[i]['reponse']}\n")
            streak = 1


    print(f"\nPartie terminée\nScore final de l'équipe \"{team}\" : {int(score)}/{int(score_max)} points.")

