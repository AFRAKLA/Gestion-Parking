class Place:
    def __init__(self, numero, niveau, hauteur, longueur):
        """ Définit une place de parking avec son emplacement et ses dimensions pour vérifier si un véhicule peut s'y garer. """
        self.numero = numero
        self.niveau = niveau
        self.hauteur = float(hauteur)
        self.longueur = float(longueur)
        self.est_libre = True
        self.mes_placements = []

    def get_id(self):
        """ Renvoie l'identifiant unique de la place (ex: A1) pour l'affichage et le suivi. """
        return f"{self.niveau}{self.numero}"
    
    def add_placement(self, placement):
        """ Occupe la place en y associant un ticket de stationnement et change son état à occupé. """
        self.est_libre = False
        self.mes_placements.append(placement)