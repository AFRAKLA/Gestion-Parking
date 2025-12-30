import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.place import Place

class TestPlace(unittest.TestCase):
    
    def test_id_generation(self):
        """ Vérifie que l'identifiant est bien formé (Niveau + Numéro) et que la place est libre par défaut. """
        p = Place(5, "B", 2.5, 5.0)
        self.assertEqual(p.get_id(), "B5")
        self.assertTrue(p.est_libre)

    def test_occupation(self):
        """ Teste le changement d'état de la place (libre -> occupée) lors d'une affectation. """
        p = Place(1, "A", 2.5, 5.0)
        p.est_libre = False
        self.assertFalse(p.est_libre)

if __name__ == '__main__':
    unittest.main()