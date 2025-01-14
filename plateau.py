class Plateau:
    def __init__(self, taille):
        self.taille = taille
        self.grille = [[0 for _ in range(taille)] for _ in range(taille)]
        self.navires = []
        self.tirs = set()

    def peut_placer_navire(self, positions):
        """Vérifie si un navire peut être placé aux positions données"""
        return all(0 <= x < self.taille and 0 <= y < self.taille and 
                  self.grille[x][y] == 0 for x, y in positions)

    def placer_navire(self, navire, positions):
        """Place un navire sur le plateau"""
        if self.peut_placer_navire(positions):
            navire.placer(positions)
            for x, y in positions:
                self.grille[x][y] = 1
            self.navires.append(navire)
            return True
        return False

    def recevoir_tir(self, position):
        """Gère la réception d'un tir à une position donnée"""
        x, y = position
        if position in self.tirs:
            return None
        
        self.tirs.add(position)
        touche = False
        navire_touche = None
        
        for navire in self.navires:
            if navire.est_touche(position):
                touche = True
                navire_touche = navire
                break
                
        return {
            "touche": touche,
            "coule": navire_touche.est_coule() if navire_touche else False
        }

    def tous_navires_coules(self):
        """Vérifie si tous les navires sont coulés"""
        return all(navire.est_coule() for navire in self.navires)

    def get_etat_case(self, position):
        """Retourne l'état d'une case"""
        x, y = position
        if position in self.tirs:
            return 2 if self.grille[x][y] == 1 else 3
        return self.grille[x][y]