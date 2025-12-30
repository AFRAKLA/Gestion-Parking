from datetime import datetime

class Placement:
    def __init__(self, date_debut: datetime):
        """ Initialise un ticket de stationnement (placement) avec l'heure d'arrivée du véhicule. """
        self.date_debut = date_debut
        self.date_fin = None
        self.est_en_cours = True

    def partir_place(self):
        """ Clôture la session de stationnement en enregistrant l'heure de départ et en désactivant le ticket. """
        self.date_fin = datetime.now()
        self.est_en_cours = False