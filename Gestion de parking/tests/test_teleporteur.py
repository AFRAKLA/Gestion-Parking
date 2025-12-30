import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.teleporteur import Teleporteur
from src.models.voiture import Voiture
from src.models.place import Place

class TestTeleporteur(unittest.TestCase):
    
    def test_teleportation(self):
        """ Vérifie que le mécanisme de téléportation s'exécute sans erreur lorsqu'on lui fournit une voiture et une destination valides. """
        t = Teleporteur()
        v = Voiture("TELE-1", 2.0, 4.0)
        
        # Création d'une place fictive nécessaire pour l'affichage de l'ID (ex: Z99) dans le téléporteur
        p = Place(99, "Z", 3.0, 6.0) 
        
        try:
            # On passe 'p' (la place) pour éviter que le print() interne ne plante sur un NoneType
            t.teleporter_voiture(v, p, None)
        except Exception as e:
            self.fail(f"Le téléporteur a planté de manière inattendue : {e}")

if __name__ == '__main__':
    unittest.main()