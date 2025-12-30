import unittest
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.voiture import Voiture
from src.models.placement import Placement

class TestVoiture(unittest.TestCase):
    
    def setUp(self):
        """ Initialise une voiture avec des dimensions standard pour servir de base aux tests. """
        self.voiture = Voiture("AB-123-CD", 2.0, 4.0)

    def test_dimensions(self):
        """ Vérifie que les caractéristiques physiques et l'immatriculation sont correctement enregistrées à la création. """
        self.assertEqual(self.voiture.immatriculation, "AB-123-CD")
        self.assertEqual(self.voiture.hauteur, 2.0)

    def test_ajout_placement(self):
        """ Teste l'historisation : vérifie que l'ajout d'un ticket (placement) est bien conservé dans la liste du véhicule. """
        p = Placement(datetime.now())
        self.voiture.add_placement(p)
        self.assertIn(p, self.voiture.mes_placements)

if __name__ == '__main__':
    unittest.main()