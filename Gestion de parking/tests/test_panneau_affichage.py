import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.panneau_affichage import PanneauAffichage
from src.models.parking import Parking

class TestPanneauAffichage(unittest.TestCase):
    def test_affichage(self):
        """ Vérifie simplement que la méthode d'affichage communique avec le parking sans lever d'exception critique. """
        panneau = PanneauAffichage()
        parking = Parking()
        
        try:
            panneau.afficher_nb_places_disponibles(parking)
        except Exception as e:
            self.fail(f"Erreur panneau: {e}")

if __name__ == '__main__':
    unittest.main()