class Voiture:
    def __init__(self, immatriculation: str, hauteur: float, longueur: float):
        """ Initialise un véhicule avec ses dimensions physiques et son immatriculation pour le contrôle d'accès. """
        self.immatriculation = immatriculation
        self.hauteur = hauteur
        self.longueur = longueur
        self.est_dans_parking = False
        self.est_aguerir_ailleurs = False
        
        self.mes_placements = []
        self.proprietaire = None

    def add_placement(self, placement):
        """ Historise un nouveau stationnement (ticket) associé à ce véhicule. """
        self.mes_placements.append(placement)