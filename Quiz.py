import time
import random
import json
import os
import sys

# --- 1. OUTILS VISUELS (COULEURS) ---
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

def clear_screen():
    """Nettoie la console pour faire propre."""
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter(text, speed=0.02):
    """Affiche le texte lettre par lettre pour un effet rétro."""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    print()

# --- 2. GESTION DES SCORES (SAUVEGARDE) ---
FICHIER_SCORES = "football_scores.json"

def charger_scores():
    if os.path.exists(FICHIER_SCORES):
        with open(FICHIER_SCORES, 'r') as f:
            return json.load(f)
    return []

def sauvegarder_score(nom, score):
    scores = charger_scores()
    scores.append({"nom": nom, "score": score, "date": time.strftime("%Y-%m-%d %H:%M")})
    # On trie pour garder les meilleurs en premier
    scores = sorted(scores, key=lambda x: x['score'], reverse=True)[:5] # Top 5
    with open(FICHIER_SCORES, 'w') as f:
        json.dump(scores, f)

# --- 3. BASE DE DONNÉES MASSIVE ---
questions_base = [
    # --- FACILE ---
    {"q": "Qui est surnommé 'Zizou' ?", "choix": ["A) Zidane", "B) Zlatan", "C) Zola", "D) Zouma"], "rep": "A", "lvl": "Facile", "pts": 10},
    {"q": "Quelle est la forme du ballon ?", "choix": ["A) Ovale", "B) Carré", "C) Sphérique", "D) Triangulaire"], "rep": "C", "lvl": "Facile", "pts": 10},
    {"q": "Un match dure combien de temps (hors arrêts de jeu) ?", "choix": ["A) 45 min", "B) 60 min", "C) 90 min", "D) 100 min"], "rep": "C", "lvl": "Facile", "pts": 10},
    {"q": "Quel carton expulse un joueur ?", "choix": ["A) Vert", "B) Jaune", "C) Rouge", "D) Bleu"], "rep": "C", "lvl": "Facile", "pts": 10},
    {"q": "Dans quel pays est la Liga ?", "choix": ["A) France", "B) Espagne", "C) Italie", "D) Angleterre"], "rep": "B", "lvl": "Facile", "pts": 10},
    
    # --- MOYEN ---
    {"q": "Quel club a remporté la C1 en 1993 ?", "choix": ["A) PSG", "B) Marseille", "C) Monaco", "D) Bordeaux"], "rep": "B", "lvl": "Moyen", "pts": 20},
    {"q": "Qui a gagné le Ballon d'Or 2022 ?", "choix": ["A) Messi", "B) Mbappé", "C) Benzema", "D) Haaland"], "rep": "C", "lvl": "Moyen", "pts": 20},
    {"q": "Quel est le stade du FC Barcelone ?", "choix": ["A) Santiago Bernabeu", "B) Camp Nou", "C) San Siro", "D) Old Trafford"], "rep": "B", "lvl": "Moyen", "pts": 20},
    {"q": "Combien de Coupes du Monde la France a-t-elle ?", "choix": ["A) 1", "B) 2", "C) 3", "D) 4"], "rep": "B", "lvl": "Moyen", "pts": 20},
    {"q": "Quel pays a organisé le Mondial 2014 ?", "choix": ["A) Afrique du Sud", "B) Russie", "C) Brésil", "D) Allemagne"], "rep": "C", "lvl": "Moyen", "pts": 20},

    # --- DIFFICILE ---
    {"q": "Qui est le meilleur buteur de l'histoire de la Coupe du Monde ?", "choix": ["A) Ronaldo R9", "B) Miroslav Klose", "C) Pelé", "D) Fontaine"], "rep": "B", "lvl": "Difficile", "pts": 30},
    {"q": "Quel club est surnommé les 'Gunners' ?", "choix": ["A) Tottenham", "B) Liverpool", "C) Arsenal", "D) West Ham"], "rep": "C", "lvl": "Difficile", "pts": 30},
    {"q": "En quelle année a été créé le PSG ?", "choix": ["A) 1970", "B) 1974", "C) 1904", "D) 1998"], "rep": "A", "lvl": "Difficile", "pts": 30},
    {"q": "Quel joueur a gagné le plus de trophées collectifs ?", "choix": ["A) Dani Alves", "B) Messi", "C) Maxwell", "D) Giggs"], "rep": "B", "lvl": "Difficile", "pts": 30},
    
    # --- EXPERT (TRÈS DUR) ---
    {"q": "Quelle équipe a gagné l'Euro 1992 sans être qualifiée au départ ?", "choix": ["A) Danemark", "B) Grèce", "C) Suède", "D) Yougoslavie"], "rep": "A", "lvl": "Expert", "pts": 50},
    {"q": "Qui a marqué le but en or à l'Euro 2000 ?", "choix": ["A) Wiltord", "B) Trezeguet", "C) Zidane", "D) Henry"], "rep": "B", "lvl": "Expert", "pts": 50},
    {"q": "Combien de buts Just Fontaine a-t-il marqués en 1958 ?", "choix": ["A) 9", "B) 11", "C) 13", "D) 15"], "rep": "C", "lvl": "Expert", "pts": 50},
    {"q": "Quel est le seul gardien Ballon d'Or ?", "choix": ["A) Neuer", "B) Yachine", "C) Buffon", "D) Zoff"], "rep": "B", "lvl": "Expert", "pts": 50}
]

# --- 4. LOGIQUE DES JOKERS ---
jokers = {"50/50": True, "Appel": True}

def utiliser_joker_5050(question):
    """Enlève 2 mauvaises réponses."""
    mauvaises = [c for c in question["choix"] if not c.startswith(question["rep"])]
    a_enlever = random.sample(mauvaises, 2)
    restants = [c for c in question["choix"] if c not in a_enlever]
    return restants

def utiliser_joker_appel(question):
    """Simule un appel à un expert."""
    chance = 0.9 if question['lvl'] == "Facile" else 0.5 # L'expert est moins sûr en mode difficile
    
    print(f"\n📞 {Color.CYAN}Appel à Thierry (Expert foot)... Dring Dring...{Color.END}")
    time.sleep(2)
    if random.random() < chance:
        return f"Thierry : 'Salut ! Je suis presque sûr que c'est la réponse {question['rep']}.'"
    else:
        faux = [c for c in question["choix"] if not c.startswith(question["rep"])][0]
        return f"Thierry : 'Oula, pas facile... Je dirais peut-être {faux[0]}, mais sans conviction.'"

# --- 5. MOTEUR DU JEU ---
def lancer_quiz():
    clear_screen()
    print(f"{Color.YELLOW}{'='*50}")
    print(f"       ⚽  ULTIMATE FOOTBALL QUIZ PRO  ⚽")
    print(f"{'='*50}{Color.END}")
    
    nom_joueur = input("Entrez votre pseudo de champion : ").strip()
    
    print(f"\nBienvenue, {Color.BOLD}{nom_joueur}{Color.END} !")
    print("Modes de jeu :")
    print("1. Carrière (Progressif)")
    print("2. Mort Subite (Une erreur et c'est fini)")
    print("3. Voir les meilleurs scores")
    
    choix_mode = input("Votre choix : ")

    if choix_mode == "3":
        scores = charger_scores()
        print(f"\n{Color.PURPLE}🏆 TABLEAU D'HONNEUR 🏆{Color.END}")
        for idx, s in enumerate(scores):
            print(f"{idx+1}. {s['nom']} : {s['score']} pts ({s['date']})")
        return

    questions_melangees = questions_base.copy()
    random.shuffle(questions_melangees)
    
    score = 0
    vie = True
    
    # Boucle des questions
    for i, q in enumerate(questions_melangees):
        if not vie: break
        
        clear_screen()
        print(f"{Color.BLUE}Question {i+1} | Niveau: {q['lvl']} | Score: {score}{Color.END}")
        print(f"{Color.YELLOW}{'-'*50}{Color.END}")
        print(f"{Color.BOLD}{q['q']}{Color.END}")
        print(f"{Color.YELLOW}{'-'*50}{Color.END}")
        
        # Affichage des choix
        choix_a_afficher = q['choix']
        
        # Gestion de l'input joker
        reponse_donnee = False
        while not reponse_donnee:
            for c in choix_a_afficher:
                print(c)
            
            print(f"\n{Color.CYAN}Commandes : A/B/C/D ou J pour Joker{Color.END}")
            rep = input("Votre réponse : ").upper().strip()
            
            if rep == "J":
                if not jokers["50/50"] and not jokers["Appel"]:
                    print(f"{Color.RED}🚫 Plus de jokers disponibles !{Color.END}")
                    continue
                
                print("\n🃏 JOKERS DISPONIBLES :")
                if jokers["50/50"]: print("1. 50/50 (Enlève 2 choix)")
                if jokers["Appel"]: print("2. Appel à un ami")
                
                choix_joker = input("Lequel utiliser ? (1 ou 2) : ")
                
                if choix_joker == "1" and jokers["50/50"]:
                    choix_a_afficher = utiliser_joker_5050(q)
                    jokers["50/50"] = False
                    print(f"{Color.GREEN}✅ 50/50 activé !{Color.END}")
                elif choix_joker == "2" and jokers["Appel"]:
                    avis = utiliser_joker_appel(q)
                    print(f"{Color.GREEN}{avis}{Color.END}")
                    jokers["Appel"] = False
                else:
                    print("Choix invalide ou joker déjà utilisé.")
            
            elif rep in ["A", "B", "C", "D"]:
                reponse_donnee = True
                # Vérification
                if rep == q['rep']:
                    print(f"\n{Color.GREEN}✅ BUT !!! Bonne réponse ! (+{q['pts']} pts){Color.END}")
                    score += q['pts']
                    time.sleep(1.5)
                else:
                    print(f"\n{Color.RED}❌ CARTON ROUGE ! La bonne réponse était {q['rep']}.{Color.END}")
                    if choix_mode == "2": # Mort subite
                        vie = False
                        print(f"{Color.RED}💀 Éliminé en mort subite !{Color.END}")
                    time.sleep(2)
            else:
                print("Entrée invalide.")

    # Fin de partie
    clear_screen()
    typewriter(f"🏁 FIN DU MATCH POUR {nom_joueur.upper()} 🏁")
    print(f"Score Final : {Color.BOLD}{score} points{Color.END}")
    
    # Sauvegarde
    sauvegarder_score(nom_joueur, score)
    print(f"{Color.GREEN}💾 Score sauvegardé dans le classement !{Color.END}")
    
    # Commentaire de fin
    if score > 300:
        print(f"{Color.PURPLE}🐐 Commentaire : NIVEAU G.O.A.T (Greatest of All Time){Color.END}")
    elif score > 150:
        print(f"{Color.CYAN}⚽ Commentaire : Joueur de classe mondiale.{Color.END}")
    else:
        print(f"{Color.YELLOW}👶 Commentaire : Retourne au centre de formation...{Color.END}")

if __name__ == "__main__":
    # Boucle pour rejouer
    while True:
        lancer_quiz()
        replay = input("\nRejouer ? (O/N) : ").lower()
        if replay != 'o':
            print("Merci d'avoir joué !")
            break
        # On remet les jokers pour la nouvelle partie
        jokers = {"50/50": True, "Appel": True}