import tkinter as tk
from tkinter import messagebox
from navire import Navire
from plateau import Plateau
from joueur import Joueur

class BatailleNavale:
    def __init__(self, root):
        self.root = root
        self.root.title("Bataille Navale")
        self.TAILLE_GRILLE = 10
        self.TAILLE_CASE = 40
        self.NAVIRES_DISPONIBLES = [5, 4, 3, 3, 2, 2]
        self.navires_coules_joueur = 0
        self.navires_coules_ordinateur = 0
        self.init_accueil()

    def init_accueil(self):
        """Initialise l'écran d'accueil"""
        for widget in self.root.winfo_children():
            widget.destroy()

        frame_accueil = tk.Frame(self.root)
        frame_accueil.pack(pady=20)

        tk.Label(frame_accueil, text="Bataille Navale", font=("Arial", 24, "bold")).pack(pady=10)
        tk.Label(frame_accueil, text="Bienvenue dans le jeu de la Bataille Navale", 
                font=("Arial", 14)).pack(pady=10)

        tk.Button(frame_accueil, text="Nouvelle Partie", font=("Arial", 14),
                 command=self.init_game).pack(pady=20)

    def init_game(self):
        """Initialise une nouvelle partie"""
        self.joueur = Joueur("Joueur")
        self.ordinateur = Joueur("Ordinateur", est_ordinateur=True)
        self.phase = "placement"
        self.tour_joueur = True
        self.orientation = "H"
        self.current_navire = 0
        self.historique = []
        self.navires_coules_joueur = 0
        self.navires_coules_ordinateur = 0
        self.ordinateur.placer_navires_aleatoirement(self.NAVIRES_DISPONIBLES)
        self.init_ui()

    def init_ui(self):
        """Initialise l'interface utilisateur principale"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Création des frames principales
        frame_principal = tk.Frame(self.root)
        frame_principal.pack(padx=20, pady=10)

        # Frame pour les plateaux
        frame_plateaux = tk.Frame(frame_principal)
        frame_plateaux.pack()

        # Plateau joueur
        frame_joueur = tk.Frame(frame_plateaux)
        frame_joueur.pack(side=tk.LEFT, padx=20)
        tk.Label(frame_joueur, text="Votre plateau", font=("Arial", 14, "bold")).pack()
        self.canvas_joueur = self.creer_canvas_plateau(frame_joueur)
        self.canvas_joueur.bind("<Motion>", self.previsualiser_navire)
        self.canvas_joueur.bind("<Button-1>", self.placer_navire)

        # Plateau ordinateur
        frame_ordi = tk.Frame(frame_plateaux)
        frame_ordi.pack(side=tk.LEFT, padx=20)
        tk.Label(frame_ordi, text="Plateau adverse", font=("Arial", 14, "bold")).pack()
        self.canvas_ordi = self.creer_canvas_plateau(frame_ordi)
        self.canvas_ordi.bind("<Button-1>", self.tirer)

        # Frame informations
        frame_info = tk.Frame(frame_principal)
        frame_info.pack(pady=10)

        # Statut et tour
        self.label_status = tk.Label(frame_info, text="Placez vos navires", 
                                   font=("Arial", 12))
        self.label_status.pack()
        self.label_tour = tk.Label(frame_info, text="Tour : Joueur", 
                                 font=("Arial", 12))
        self.label_tour.pack()

        # Compteurs de navires coulés
        frame_compteurs = tk.Frame(frame_info)
        frame_compteurs.pack(pady=5)
        
        self.label_navires_joueur = tk.Label(frame_compteurs, 
            text=f"Navires coulés (Joueur) : {self.navires_coules_joueur}/{len(self.NAVIRES_DISPONIBLES)}", 
            font=("Arial", 10))
        self.label_navires_joueur.pack()
        
        self.label_navires_ordi = tk.Label(frame_compteurs, 
            text=f"Navires coulés (Ordinateur) : {self.navires_coules_ordinateur}/{len(self.NAVIRES_DISPONIBLES)}", 
            font=("Arial", 10))
        self.label_navires_ordi.pack()

        # Boutons de contrôle
        frame_controle = tk.Frame(frame_principal)
        frame_controle.pack(pady=10)

        self.btn_orientation = tk.Button(frame_controle, text="Changer Orientation",
                                       command=self.changer_orientation)
        self.btn_orientation.pack(side=tk.LEFT, padx=5)

        tk.Button(frame_controle, text="Nouvelle Partie",
                 command=self.init_accueil).pack(side=tk.LEFT, padx=5)

        # Historique
        frame_historique = tk.Frame(frame_principal)
        frame_historique.pack(pady=10, fill=tk.X)
        
        scrollbar = tk.Scrollbar(frame_historique)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.text_historique = tk.Text(frame_historique, height=5, width=50)
        self.text_historique.pack(side=tk.LEFT, fill=tk.X)
        
        scrollbar.config(command=self.text_historique.yview)
        self.text_historique.config(yscrollcommand=scrollbar.set)

    def creer_canvas_plateau(self, parent):
        """Crée un canvas pour un plateau de jeu"""
        canvas = tk.Canvas(parent, 
                         width=self.TAILLE_GRILLE * self.TAILLE_CASE + 20,
                         height=self.TAILLE_GRILLE * self.TAILLE_CASE + 20)
        canvas.pack()

        # Dessine la grille
        offset = 20
        for i in range(self.TAILLE_GRILLE + 1):
            # Lignes horizontales
            canvas.create_line(offset, offset + i * self.TAILLE_CASE,
                             offset + self.TAILLE_GRILLE * self.TAILLE_CASE,
                             offset + i * self.TAILLE_CASE)
            # Lignes verticales
            canvas.create_line(offset + i * self.TAILLE_CASE, offset,
                             offset + i * self.TAILLE_CASE,
                             offset + self.TAILLE_GRILLE * self.TAILLE_CASE)

        # Ajoute les labels
        for i in range(self.TAILLE_GRILLE):
            # Lettres
            canvas.create_text(offset + i * self.TAILLE_CASE + self.TAILLE_CASE/2,
                             offset/2, text=chr(65 + i))
            # Chiffres
            canvas.create_text(offset/2,
                             offset + i * self.TAILLE_CASE + self.TAILLE_CASE/2,
                             text=str(i + 1))

        return canvas

    def event_to_grid_coords(self, event):
        """Convertit les coordonnées d'un événement en coordonnées de grille"""
        offset = 20
        x = (event.y - offset) // self.TAILLE_CASE
        y = (event.x - offset) // self.TAILLE_CASE
        return x, y

    def changer_orientation(self):
        """Change l'orientation de placement des navires"""
        self.orientation = "V" if self.orientation == "H" else "H"
        self.btn_orientation.config(text=f"Orientation : {'Horizontale' if self.orientation == 'H' else 'Verticale'}")

    def previsualiser_navire(self, event):
        """Prévisualise le placement d'un navire"""
        if self.phase != "placement" or self.current_navire >= len(self.NAVIRES_DISPONIBLES):
            return

        x, y = self.event_to_grid_coords(event)
        if not (0 <= x < self.TAILLE_GRILLE and 0 <= y < self.TAILLE_GRILLE):
            return

        self.canvas_joueur.delete("preview")
        taille = self.NAVIRES_DISPONIBLES[self.current_navire]
        positions = self.calculer_positions(x, y, taille)
        
        if positions and self.joueur.plateau.peut_placer_navire(positions):
            self.dessiner_navire(self.canvas_joueur, positions, "lightgray", "preview")

    def calculer_positions(self, x, y, taille):
        """Calcule les positions pour un navire"""
        if self.orientation == "H":
            positions = [(x, y + i) for i in range(taille)]
        else:
            positions = [(x + i, y) for i in range(taille)]
        
        if all(0 <= px < self.TAILLE_GRILLE and 0 <= py < self.TAILLE_GRILLE 
               for px, py in positions):
            return positions
        return None

    def placer_navire(self, event):
        """Place un navire sur le plateau du joueur"""
        if self.phase != "placement" or self.current_navire >= len(self.NAVIRES_DISPONIBLES):
            return

        x, y = self.event_to_grid_coords(event)
        taille = self.NAVIRES_DISPONIBLES[self.current_navire]
        positions = self.calculer_positions(x, y, taille)

        if positions and self.joueur.plateau.peut_placer_navire(positions):
            navire = Navire(taille)
            self.joueur.placer_navire(navire, positions)
            self.dessiner_navire(self.canvas_joueur, positions, "gray")
            self.current_navire += 1

            if self.current_navire >= len(self.NAVIRES_DISPONIBLES):
                self.phase = "jeu"
                self.label_status.config(text="Tous les navires sont placés. À vous de jouer !")
                self.btn_orientation.config(state="disabled")

    def tirer(self, event):
        """Gère un tir du joueur"""
        if not self.tour_joueur or self.phase != "jeu":
            return

        x, y = self.event_to_grid_coords(event)
        if not (0 <= x < self.TAILLE_GRILLE and 0 <= y < self.TAILLE_GRILLE):
            return

        resultat = self.ordinateur.plateau.recevoir_tir((x, y))
        if resultat is None:
            return

        self.marquer_tir(self.canvas_ordi, x, y, resultat["touche"])
        message = f"Joueur tire en {chr(65 + y)}{x + 1} : "
        if resultat["touche"]:
            message += "Touché !"
            if resultat["coule"]:
                self.navires_coules_joueur += 1
                self.label_navires_ordi.config(
                    text=f"Navires coulés (Ordinateur) : {self.navires_coules_joueur}/{len(self.NAVIRES_DISPONIBLES)}"
                )
                message += " Navire coulé !"
        else:
            message += "Manqué !"
            
        self.ajouter_historique(message)

        if self.ordinateur.plateau.tous_navires_coules():
            self.fin_partie("Victoire ! Vous avez gagné !")
        else:
            self.tour_joueur = False
            self.label_tour.config(text="Tour : Ordinateur")
            self.root.after(1000, self.tour_ordinateur)

    def tour_ordinateur(self):
        """Gère le tour de l'ordinateur"""
        x, y = self.ordinateur.choisir_tir(self.joueur.plateau)
        resultat = self.joueur.plateau.recevoir_tir((x, y))
        
        self.marquer_tir(self.canvas_joueur, x, y, resultat["touche"])
        message = f"Ordinateur tire en {chr(65 + y)}{x + 1} : "
        if resultat["touche"]:
            message += "Touché !"
            if resultat["coule"]:
                self.navires_coules_ordinateur += 1
                self.label_navires_joueur.config(
                    text=f"Navires coulés (Joueur) : {self.navires_coules_ordinateur}/{len(self.NAVIRES_DISPONIBLES)}"
                )
                message += " Navire coulé !"
        else:
            message += "Manqué !"
            
        self.ajouter_historique(message)

        if self.joueur.plateau.tous_navires_coules():
            self.fin_partie("Défaite ! L'ordinateur a gagné !")
        else:
            self.tour_joueur = True
            self.label_tour.config(text="Tour : Joueur")

    def dessiner_navire(self, canvas, positions, couleur, tag=""):
        """Dessine un navire sur le canvas"""
        offset = 20
        for x, y in positions:
            canvas.create_rectangle(
                offset + y * self.TAILLE_CASE,
                offset + x * self.TAILLE_CASE,
                offset + (y + 1) * self.TAILLE_CASE,
                offset + (x + 1) * self.TAILLE_CASE,
                fill=couleur,
                tags=tag
            )

    def marquer_tir(self, canvas, x, y, touche):
        """Marque un tir sur le canvas"""
        offset = 20
        couleur = "red" if touche else "blue"
        canvas.create_oval(
            offset + y * self.TAILLE_CASE + 5,
            offset + x * self.TAILLE_CASE + 5,
            offset + (y + 1) * self.TAILLE_CASE - 5,
            offset + (x + 1) * self.TAILLE_CASE - 5,
            fill=couleur
        )

    def ajouter_historique(self, message):
        """Ajoute un message à l'historique"""
        self.historique.append(message)
        self.text_historique.insert("1.0", message + "\n")

    def fin_partie(self, message):
        """Gère la fin de la partie"""
        self.phase = "fin"
        messagebox.showinfo("Fin de partie", message)
        self.label_status.config(text=message)

if __name__ == "__main__":
    root = tk.Tk()
    jeu = BatailleNavale(root)
    root.mainloop()

