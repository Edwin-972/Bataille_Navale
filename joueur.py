from plateau import Plateau
from random import randint, choice

class Joueur:
    def __init__(self, nom, est_ordinateur=False):
        self.nom = nom
        self.plateau = Plateau(10)  # Taille du plateau = 10x10
        self.est_ordinateur = est_ordinateur
        self.derniers_tirs_reussis = []  # Pour l'IA, cela stocke les tirs réussis

    def placer_navire(self, navire, positions):
        """Place un navire sur le plateau du joueur"""
        return self.plateau.placer_navire(navire, positions)

    def recevoir_tir(self, position):
        """Reçoit un tir à une position donnée"""
        return self.plateau.recevoir_tir(position)

    def choisir_tir(self, plateau_adversaire):
        """Choisit une position de tir (pour l'ordinateur)"""
        if self.est_ordinateur:
            if self.derniers_tirs_reussis:
                # Si un tir précédent a touché un navire, essayer de le couler
                x, y = self.derniers_tirs_reussis[-1]
                directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
                for dx, dy in directions:
                    new_x, new_y = x + dx, y + dy
                    if (0 <= new_x < plateau_adversaire.taille and 
                        0 <= new_y < plateau_adversaire.taille and
                        (new_x, new_y) not in plateau_adversaire.tirs):
                        return new_x, new_y

            # Si aucun tir stratégique n'a été trouvé, tirer dans une zone non explorée
            while True:
                x = randint(0, plateau_adversaire.taille - 1)
                y = randint(0, plateau_adversaire.taille - 1)
                if (x, y) not in plateau_adversaire.tirs:
                    return x, y
        return None

    def placer_navires_aleatoirement(self, tailles_navires):
        if self.est_ordinateur:
            for taille in tailles_navires:
                placed = False
                while not placed:
                    orientation = choice(["H", "V"])  # Choisir horizontal ou vertical
                    x = randint(0, self.plateau.taille - 1)
                    y = randint(0, self.plateau.taille - 1)

                    if orientation == "H":
                        positions = [(x, y + i) for i in range(taille)]
                    else:
                        positions = [(x + i, y) for i in range(taille)]

                    # Vérifier que le navire peut être placé et qu'il n'entre pas en collision avec d'autres navires
                    if not self.plateau.peut_placer_navire(positions):
                        continue
                    
                    # Vérifier que les navires sont suffisamment éloignés les uns des autres
                    if all(self.plateau.peut_placer_navire([pos]) for pos in positions):
                        from navire import Navire
                        navire = Navire(taille)
                        self.placer_navire(navire, positions)
                        placed = True