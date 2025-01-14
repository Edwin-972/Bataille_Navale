class Navire:
    def __init__(self, taille):
        self.taille = taille
        self.positions = []
        self.positions_touchees = set()

    def placer(self, positions):
        """Place le navire aux positions données"""
        self.positions = positions

    def est_touche(self, position):
        """Vérifie si le navire est touché à la position donnée"""
        if position in self.positions:
            self.positions_touchees.add(position)
            return True
        return False

    def est_coule(self):
        """Vérifie si le navire est coulé"""
        return len(self.positions_touchees) == len(self.positions)

    def get_positions_non_touchees(self):
        """Retourne les positions non touchées du navire"""
        return [pos for pos in self.positions if pos not in self.positions_touchees]