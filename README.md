# Bataille_Navale
Jeu Bataille navale (Python)

Etudiant: Edwin 

Script main.py

Ce fichier est le cœur de l’application, contenant la classe principale BatailleNavale qui gère l’interface utilisateur avec Tkinter et orchestre le jeu.

Classe BatailleNavale :
	Gère l’interface et les règles du jeu.
	- __init__(self, root): Initialise l’interface et le jeu.
	- init_accueil(self): Affiche l’écran d’accueil.
	- init_game(self): Lance une nouvelle partie.
	- placer_navire(self, event): Permet de placer un navire.
	- tirer(self, event): Gère les tirs du joueur.
	- tour_ordinateur(self): Gère le tour de l’ordinateur.
	- fin_partie(self, message): Affiche un message de fin de partie.

Script navire.py

Contient la classe Navire, représentant chaque bateau du jeu, avec ses positions et son état.

Classe Navire :
	- Gère la position et l’état d’un navire.
	- __init__(self, taille): Crée un navire de taille donnée.
	- placer(self, positions): Place le navire.
	- est_touche(self, position): Vérifie si le navire est touché.
	- est_coule(self): Vérifie si le navire est coulé.

Script plateau.py

Ce fichier contient la classe Plateau, représentant la grille de jeu où les navires sont placés et les tirs enregistrés.

Classe Plateau :
	- Gère la grille de jeu et les interactions.
	- __init__(self, taille): Crée un plateau de taille donnée.
	- peut_placer_navire(self, positions): Vérifie si un navire peut être placé.
	- recevoir_tir(self, position): Enregistre un tir.
	- tous_navires_coules(self): Vérifie si tous les navires sont coulés.

Script joueur.py

Contient la classe Joueur, représentant un joueur humain ou ordinateur.

Classe Joueur :
	- Gère les actions du joueur.
	- __init__(self, nom, est_ordinateur=False): Initialise un joueur, humain ou ordinateur.
	- placer_navires_aleatoirement(self, navires): Place les navires aléatoirement pour l’ordinateur.
	- choisir_tir(self, plateau): Choisit une position pour tirer (ordinateur).
