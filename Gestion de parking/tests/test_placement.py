import unittest
import sys
import os
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.placement import Placement

class TestPlacement(unittest.TestCase):
    
    def test_cycle_vie(self):
        """ Vérifie le cycle de vie complet d'un stationnement : création (actif) -> départ (clôturé avec date de fin). """
        now = datetime.now()
        pl = Placement(now)
        
        # Vérification état initial
        self.assertTrue(pl.est_en_cours)
        self.assertEqual(pl.date_debut, now)
        
        # Action de départ
        pl.partir_place()
        
        # Vérification état final
        self.assertFalse(pl.est_en_cours)
        self.assertIsNotNone(pl.date_fin)

if __name__ == '__main__':
    unittest.main()