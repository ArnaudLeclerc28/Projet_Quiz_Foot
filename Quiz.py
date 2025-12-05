import tkinter as tk
from tkinter import ttk
import random
import json
import os
import time
import winsound
import math

# ==========================================
# 🎨 CONFIGURATION "LIGHT & PRO"
# ==========================================
CFG = {
    "win_w": 1080,
    "win_h": 720,
    "bg": "#f8fafc",           # Blanc cassé très propre
    "panel": "#ffffff",        # Blanc pur
    "primary": "#2563eb",      # Bleu Roi
    "secondary": "#4338ca",    # Indigo profond
    "accent": "#ef4444",       # Rouge Vif
    "gold": "#d97706",         # Or (pour le niveau Légendaire)
    "success": "#16a34a",      # Vert
    "text": "#0f172a",         # Noir bleuté (lisible)
    "subtext": "#64748b",      # Gris
    "font_title": ("Impact", 45),
    "font_main": ("Segoe UI", 14),
    "font_bold": ("Segoe UI", 16, "bold"),
    "author": "By LECLERC Arnaud"
}

FILE_DB = "football_ultimate_db.json"

# ==========================================
# 💀 BASE DE DONNÉES (MODE ZINZIN - DIFFICILE / EXPERT / LÉGENDAIRE)
# ==========================================
QUESTIONS_MASTER = [
    # --- NIVEAU 3 : DIFFICILE ---
    {"q": "Qui détient le record de buts en une seule CDM (13 buts) ?", "choix": ["J. Fontaine", "G. Müller", "Ronaldo R9", "Klose"], "rep": "J. Fontaine", "lvl": 3},
    {"q": "Seul gardien Ballon d'Or de l'histoire ?", "choix": ["L. Yachine", "M. Neuer", "G. Buffon", "D. Zoff"], "rep": "L. Yachine", "lvl": 3},
    {"q": "Vainqueur surprise de l'Euro 2004 ?", "choix": ["Grèce", "Portugal", "Danemark", "Suède"], "rep": "Grèce", "lvl": 3},
    {"q": "Meilleur buteur de l'histoire de la C1 ?", "choix": ["C. Ronaldo", "Messi", "Lewandowski", "Benzema"], "rep": "C. Ronaldo", "lvl": 3},
    {"q": "Surnom du club d'Everton ?", "choix": ["The Toffees", "The Hammers", "The Villans", "The Saints"], "rep": "The Toffees", "lvl": 3},
    {"q": "Année de la première Coupe du Monde ?", "choix": ["1930", "1924", "1938", "1950"], "rep": "1930", "lvl": 3},
    {"q": "Quel joueur a gagné le plus de trophées collectifs ?", "choix": ["Messi", "Dani Alves", "Maxwell", "Iniesta"], "rep": "Messi", "lvl": 3},
    {"q": "Qui a marqué le 'But du Siècle' en 1986 ?", "choix": ["Maradona", "Pelé", "Cruyff", "Platini"], "rep": "Maradona", "lvl": 3},
    {"q": "Quel club a remporté la C1 2005 (Miracle d'Istanbul) ?", "choix": ["Liverpool", "Milan AC", "Juventus", "Bayern"], "rep": "Liverpool", "lvl": 3},
    {"q": "Nationalité de Luka Modric ?", "choix": ["Croate", "Serbe", "Slovène", "Bosnien"], "rep": "Croate", "lvl": 3},

    # --- NIVEAU 4 : EXPERT ---
    {"q": "Entraîneur des 'Invincibles' d'Arsenal ?", "choix": ["A. Wenger", "A. Ferguson", "J. Mourinho", "G. Graham"], "rep": "A. Wenger", "lvl": 4},
    {"q": "Vainqueur de la C1 avec 3 clubs différents ?", "choix": ["C. Seedorf", "S. Eto'o", "Z. Ibrahimovic", "C. Ancelotti"], "rep": "C. Seedorf", "lvl": 4},
    {"q": "Ville du stade 'San Siro' ?", "choix": ["Milan", "Turin", "Rome", "Gênes"], "rep": "Milan", "lvl": 4},
    {"q": "Pays organisateur du Mondial 1994 ?", "choix": ["USA", "Mexique", "Italie", "France"], "rep": "USA", "lvl": 4},
    {"q": "Buteur en or de la finale Euro 2000 ?", "choix": ["D. Trezeguet", "S. Wiltord", "T. Henry", "R. Pires"], "rep": "D. Trezeguet", "lvl": 4},
    {"q": "Seul joueur africain Ballon d'Or ?", "choix": ["G. Weah", "S. Eto'o", "D. Drogba", "M. Salah"], "rep": "G. Weah", "lvl": 4},
    {"q": "Quel club a été relégué en 2006 (Calciopoli) ?", "choix": ["Juventus", "Milan AC", "Lazio", "Fiorentina"], "rep": "Juventus", "lvl": 4},
    {"q": "Meilleur buteur de l'Euro 1984 (9 buts) ?", "choix": ["M. Platini", "M. Van Basten", "A. Shearer", "G. Müller"], "rep": "M. Platini", "lvl": 4},
    {"q": "Qui a raté son tir au but en finale CDM 1994 ?", "choix": ["R. Baggio", "F. Baresi", "D. Massaro", "P. Maldini"], "rep": "R. Baggio", "lvl": 4},
    {"q": "Premier vainqueur du Ballon d'Or (1956) ?", "choix": ["S. Matthews", "A. Di Stefano", "R. Kopa", "F. Puskas"], "rep": "S. Matthews", "lvl": 4},
    {"q": "Quel club a le plus de Copa Libertadores ?", "choix": ["Independiente", "Boca Juniors", "River Plate", "Peñarol"], "rep": "Independiente", "lvl": 4},

    # --- NIVEAU 5 : LÉGENDAIRE (MÉGA DIFFICILE) ---
    {"q": "Qui a marqué le tout premier but de l'histoire de la CDM ?", "choix": ["L. Laurent", "B. Patenaude", "G. Stábile", "J. Langenus"], "rep": "L. Laurent", "lvl": 5},
    {"q": "Le gardien-buteur J-L. Chilavert est de quelle nationalité ?", "choix": ["Paraguayen", "Colombien", "Chilien", "Uruguayen"], "rep": "Paraguayen", "lvl": 5},
    {"q": "Quel joueur détient le record de cartons rouges (+40) ?", "choix": ["G. Bedoya", "S. Ramos", "Pepe", "C. Cyril Rool"], "rep": "G. Bedoya", "lvl": 5},
    {"q": "Qui est le meilleur buteur de l'histoire de la sélection Iranienne ?", "choix": ["Ali Daei", "Mehdi Taremi", "Sardar Azmoun", "Karim Bagheri"], "rep": "Ali Daei", "lvl": 5},
    {"q": "Quel club anglais a remporté la C1 deux fois de suite (79-80) ?", "choix": ["Nottingham Forest", "Aston Villa", "Liverpool", "Leeds United"], "rep": "Nottingham Forest", "lvl": 5},
    {"q": "Qui a inventé le tir au but 'Panenka' (Euro 76) ?", "choix": ["Antonin Panenka", "Josef Masopust", "Pavel Nedved", "Z. Boniek"], "rep": "Antonin Panenka", "lvl": 5},
    {"q": "Seul joueur à avoir fait un quintuplé en 9 minutes ?", "choix": ["R. Lewandowski", "S. Agüero", "E. Haaland", "J. Defoe"], "rep": "R. Lewandowski", "lvl": 5},
    {"q": "Quel pays a perdu 3 finales de Coupe du Monde sans jamais gagner ?", "choix": ["Pays-Bas", "Hongrie", "Tchécoslovaquie", "Suède"], "rep": "Pays-Bas", "lvl": 5},
    {"q": "Le plus vieux buteur en Coupe du Monde (42 ans) ?", "choix": ["Roger Milla", "Pepe", "C. Blanco", "D. Zoff"], "rep": "Roger Milla", "lvl": 5},
    {"q": "Qui a entraîné le FC Porto lors de leur victoire C1 2004 ?", "choix": ["J. Mourinho", "A. Villas-Boas", "F. Santos", "N. Espírito Santo"], "rep": "J. Mourinho", "lvl": 5},
    {"q": "Quel est le seul club écossais vainqueur de la C1 (1967) ?", "choix": ["Celtic", "Rangers", "Aberdeen", "Hibernian"], "rep": "Celtic", "lvl": 5}
]

# ==========================================
# ✨ EFFETS VISUELS (PARTICULES)
# ==========================================
class Particle:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.vel_x = random.uniform(-5, 5)
        self.vel_y = random.uniform(-12, -4)
        self.gravity = 0.6
        self.color = random.choice([CFG['primary'], CFG['accent'], CFG['success'], CFG['gold'], "#8b5cf6"])
        self.size = random.randint(5, 10)
        self.id = canvas.create_oval(x, y, x+self.size, y+self.size, fill=self.color, outline="")

    def update(self):
        self.vel_y += self.gravity
        self.x += self.vel_x
        self.y += self.vel_y
        self.canvas.move(self.id, self.vel_x, self.vel_y)
        return self.y < CFG['win_h']

class ParticleSystem:
    def __init__(self, canvas):
        self.canvas = canvas
        self.particles = []
        self.is_active = False

    def explode(self):
        self.is_active = True
        for _ in range(150): # Plus de particules !
            self.particles.append(Particle(self.canvas, CFG['win_w']//2, CFG['win_h']//2))
        self.animate()

    def animate(self):
        if not self.particles:
            self.is_active = False
            return
        for p in self.particles[:]:
            if not p.update():
                self.canvas.delete(p.id)
                self.particles.remove(p)
        if self.is_active:
            self.canvas.after(20, self.animate)

# ==========================================
# 🎮 MOTEUR DU JEU
# ==========================================
class QuizMasterApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Football Ultimate Quiz - {CFG['author']}")
        self.root.geometry(f"{CFG['win_w']}x{CFG['win_h']}")
        self.root.configure(bg=CFG['bg'])
        self.root.resizable(False, False)

        self.score = 0
        self.combo = 1
        self.high_score = self.load_score()
        self.user_name = "Challenger"
        self.timer_on = False
        self.time_left = 15

        # Canvas pour dessiner (Barre de temps, fond, particules)
        self.canvas = tk.Canvas(root, width=CFG['win_w'], height=CFG['win_h'], bg=CFG['bg'], highlightthickness=0)
        self.canvas.place(x=0, y=0)
        self.particles = ParticleSystem(self.canvas)

        self.create_title_screen()

    def load_score(self):
        if os.path.exists(FILE_DB):
            try: 
                with open(FILE_DB, 'r') as f: 
                    return json.load(f).get("record", 0)
            except: return 0
        return 0

    def save_score(self):
        if self.score > self.high_score:
            self.high_score = self.score
            with open(FILE_DB, 'w') as f: json.dump({"record": self.high_score}, f)

    def play_sound(self, type):
        # Système de son simple pour Windows
        try:
            if type == "win": winsound.Beep(1000, 100)
            elif type == "win_big": winsound.Beep(1000, 50); winsound.Beep(1500, 50); winsound.Beep(2000, 100)
            elif type == "lose": winsound.Beep(300, 300)
            elif type == "start": winsound.Beep(600, 200)
        except: pass

    def clear_ui(self):
        # Supprime les widgets (boutons, entry...)
        for widget in self.root.winfo_children():
            if not isinstance(widget, tk.Canvas): widget.destroy()
        # Supprime tout ce qui a été dessiné avec le tag "ui_layer" (textes de fin, barres...)
        self.canvas.delete("ui_layer")

    # --- ECRAN TITRE ---
    def create_title_screen(self):
        self.clear_ui()
        self.canvas.delete("all") # Reset total pour l'accueil

        # Déco de fond
        self.canvas.create_oval(-100, -100, 400, 400, fill="#e0e7ff", outline="")
        self.canvas.create_oval(800, 500, 1300, 1000, fill="#fee2e2", outline="")

        frame = tk.Frame(self.root, bg=CFG['bg'])
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text="ULTIMATE", font=("Impact", 60), fg=CFG['primary'], bg=CFG['bg']).pack()
        tk.Label(frame, text="FOOTBALL QUIZ", font=("Impact", 60), fg=CFG['text'], bg=CFG['bg']).pack()
        
        tk.Label(frame, text="⚽ ÉDITION LÉGENDAIRE", font=("Segoe UI", 14, "bold"), fg=CFG['gold'], bg=CFG['bg'], pady=5).pack()
        
        tk.Label(frame, text=f"🏆 RECORD ACTUEL : {self.high_score}", font=("Consolas", 14), fg=CFG['subtext'], bg=CFG['bg']).pack(pady=20)

        # Champ Nom
        tk.Label(frame, text="Pseudo du joueur :", font=("Segoe UI", 12), fg=CFG['text'], bg=CFG['bg']).pack()
        self.entry_name = tk.Entry(frame, font=("Segoe UI", 16), justify="center", bg="white", relief="solid", bd=1)
        self.entry_name.insert(0, self.user_name)
        self.entry_name.pack(ipady=5, pady=5)

        # Bouton Start
        btn = tk.Button(frame, text="LANCER LE MATCH", font=("Segoe UI", 16, "bold"), bg=CFG['primary'], fg="white", 
                        relief="flat", cursor="hand2", activebackground=CFG['secondary'], activeforeground="white",
                        command=self.start_game)
        btn.pack(pady=30, ipadx=30, ipady=10)

        # Signature
        tk.Label(self.root, text=CFG['author'], font=("Consolas", 10), fg=CFG['subtext'], bg=CFG['bg']).place(relx=0.98, rely=0.98, anchor="se")

    # --- JEU ---
    def start_game(self):
        # 🛡️ FIX DU BUG "REJOUER" : On utilise try/except
        try:
            self.user_name = self.entry_name.get()
        except:
            pass # Si le champ n'existe plus, on garde le nom en mémoire

        self.score = 0
        self.combo = 1
        self.play_sound("start")
        
        # Préparation du deck : On mélange tout et on prend 15 questions
        self.questions_deck = QUESTIONS_MASTER.copy()
        random.shuffle(self.questions_deck)
        self.questions_deck = self.questions_deck[:15] 
        self.q_index = 0
        
        self.load_question_ui()

    def load_question_ui(self):
        self.clear_ui()
        
        # Barre Header blanche (Tag: ui_layer pour pouvoir l'effacer)
        self.canvas.create_rectangle(0, 0, CFG['win_w'], 110, fill="white", outline="#e2e8f0", tags="ui_layer")
        
        # Affichage Score & Combo
        self.lbl_score = tk.Label(self.root, text=f"SCORE: {self.score}", font=("Impact", 20), bg="white", fg=CFG['primary'])
        self.lbl_score.place(x=30, y=30)
        
        combo_color = CFG['gold'] if self.combo >= 3 else CFG['accent']
        self.lbl_combo = tk.Label(self.root, text=f"COMBO x{self.combo}", font=("Impact", 20), bg="white", fg=combo_color)
        self.lbl_combo.place(x=250, y=30)

        # Barre de temps (Fond gris)
        self.canvas.create_rectangle(0, 105, CFG['win_w'], 110, fill="#e2e8f0", outline="", tags="ui_layer")
        # Barre de temps (Remplissage dynamique)
        self.time_left = 15
        self.bar_id = self.canvas.create_rectangle(0, 105, CFG['win_w'], 110, fill=CFG['primary'], outline="", tags="ui_layer")
        
        # Données de la question
        q_data = self.questions_deck[self.q_index]
        
        # Badge de difficulté
        diff_colors = {3: CFG['primary'], 4: "#9333ea", 5: CFG['gold']}
        diff_names = {3: "DIFFICILE", 4: "EXPERT", 5: "LÉGENDAIRE"}
        lvl = q_data['lvl']
        
        tk.Label(self.root, text=f"QUESTION {self.q_index + 1}/15 • {diff_names[lvl]}", font=("Segoe UI", 12, "bold"), fg=diff_colors[lvl], bg=CFG['bg']).pack(pady=(150, 10))
        
        # Carte Question
        q_frame = tk.Frame(self.root, bg="white", padx=40, pady=30, relief="solid", bd=1)
        q_frame.config(highlightbackground="#cbd5e1", highlightthickness=1)
        q_frame.pack(padx=20, pady=5)
        
        tk.Label(q_frame, text=q_data['q'], font=("Segoe UI", 22, "bold"), fg=CFG['text'], bg="white", wraplength=900).pack()

        # Zone Boutons
        frame_btn = tk.Frame(self.root, bg=CFG['bg'])
        frame_btn.pack(expand=True, fill="both", padx=150, pady=20)

        choices = q_data['choix'].copy()
        random.shuffle(choices)
        self.current_btns = []

        for i, choix in enumerate(choices):
            btn = tk.Button(frame_btn, text=choix, font=("Segoe UI", 16), bg="white", fg=CFG['text'],
                            relief="solid", bd=1, cursor="hand2", width=20, height=2,
                            activebackground=CFG['primary'], activeforeground="white",
                            command=lambda c=choix, b_idx=i: self.check_answer(c, b_idx))
            
            btn.grid(row=i//2, column=i%2, padx=15, pady=15, sticky="nsew")
            frame_btn.grid_columnconfigure(i%2, weight=1)
            self.current_btns.append(btn)
            
        # Signature
        tk.Label(self.root, text=CFG['author'], font=("Consolas", 10), fg=CFG['subtext'], bg=CFG['bg']).place(relx=0.5, rely=0.98, anchor="s")

        self.timer_on = True
        self.animate_timer()

    def animate_timer(self):
        if self.timer_on and self.time_left > 0:
            self.time_left -= 0.05
            width = (self.time_left / 15) * CFG['win_w']
            
            color = CFG['primary']
            if self.time_left < 5: color = CFG['accent']
            
            self.canvas.coords(self.bar_id, 0, 105, width, 110)
            self.canvas.itemconfig(self.bar_id, fill=color)
            
            self.root.after(50, self.animate_timer)
        elif self.time_left <= 0 and self.timer_on:
            self.check_answer(None, -1)

    def check_answer(self, rep_user, btn_idx):
        self.timer_on = False
        q_data = self.questions_deck[self.q_index]
        is_correct = (rep_user == q_data['rep'])

        # Bloquer boutons
        for btn in self.current_btns: btn.config(state="disabled")

        if is_correct:
            if btn_idx != -1: self.current_btns[btn_idx].config(bg=CFG['success'], fg="white", bd=0)
            
            # Points selon difficulté
            base_pts = {3: 200, 4: 400, 5: 600}
            pts = base_pts[q_data['lvl']]
            bonus = int(self.time_left * 10)
            total = int((pts + bonus) * self.combo)
            
            self.score += total
            
            # Son différent si c'est une question légendaire
            if q_data['lvl'] == 5: self.play_sound("win_big")
            else: self.play_sound("win")

            self.combo += 0.5
        else:
            if btn_idx != -1: self.current_btns[btn_idx].config(bg=CFG['accent'], fg="white", bd=0)
            # Montrer la bonne réponse
            for btn in self.current_btns:
                if btn['text'] == q_data['rep']: btn.config(bg=CFG['success'], fg="white", bd=0)
            
            self.play_sound("lose")
            self.combo = 1

        self.root.after(1500, self.next_step)

    def next_step(self):
        self.q_index += 1
        if self.q_index < len(self.questions_deck):
            self.load_question_ui()
        else:
            self.game_over()

    def game_over(self):
        self.clear_ui()
        self.save_score()
        
        # 🛡️ FIX BUG AFFICHAGE : On ajoute tags="ui_layer" pour pouvoir effacer au prochain tour
        self.canvas.create_text(CFG['win_w']//2, 180, text="FIN DU MATCH", font=("Impact", 60), fill=CFG['text'], tags="ui_layer")
        
        color_score = CFG['primary'] if self.score < self.high_score else CFG['gold']
        self.canvas.create_text(CFG['win_w']//2, 300, text=f"{self.score} PTS", font=("Impact", 80), fill=color_score, tags="ui_layer")
        
        msg = "Bien joué !"
        if self.score > 8000: msg = "T'ES UN GÉNIE DU FOOT !"
        elif self.score < 2000: msg = "C'est la DHR là..."
        
        self.canvas.create_text(CFG['win_w']//2, 400, text=f"{self.user_name}, {msg}", font=("Segoe UI", 20), fill=CFG['subtext'], tags="ui_layer")

        if self.score >= self.high_score and self.score > 0:
            self.canvas.create_text(CFG['win_w']//2, 230, text="✨ NOUVEAU RECORD ✨", font=("Segoe UI", 24, "bold"), fill=CFG['gold'], tags="ui_layer")
            self.particles.explode() # BOOM

        # Boutons
        frame = tk.Frame(self.root, bg=CFG['bg'])
        frame.place(relx=0.5, rely=0.75, anchor="center")
        
        tk.Button(frame, text="REJOUER", bg=CFG['primary'], fg="white", font=CFG['font_bold'], width=15, relief="flat", command=self.start_game).pack(side="left", padx=20)
        tk.Button(frame, text="QUITTER", bg=CFG['accent'], fg="white", font=CFG['font_bold'], width=15, relief="flat", command=self.root.quit).pack(side="left", padx=20)
        
        tk.Label(self.root, text=CFG['author'], font=("Consolas", 10), fg=CFG['subtext'], bg=CFG['bg']).place(relx=0.5, rely=0.98, anchor="s")

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizMasterApp(root)
    root.mainloop()