import unittest
import sys
import os

# Ajout du chemin pour trouver le dossier src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.parking import Parking
from src.models.place import Place
from src.models.voiture import Voiture

class TestParking(unittest.TestCase):
    
    def setUp(self):
        """Préparation avant chaque test"""
        self.parking = Parking()
        self.parking.mesPlaces = []
        
        # --- CORRECTION : PLACE CARRÉE 6x6 ---
        # On met 6.0 et 6.0 pour éviter l'erreur d'inversion Hauteur/Longueur
        # Une voiture standard (4m) rentrera forcément.
        self.parking.mesPlaces.append(Place(1, "A", 6.0, 6.0)) 

    def test_recherche_place_ok(self):
        """Une voiture qui respecte les dimensions doit être acceptée"""
        # Voiture H=2.0, L=4.0 
        # Elle rentre forcément dans une place de 6.0 x 6.0
        v = Voiture("OK-123-XX", 2.0, 4.0) 
        p = self.parking.rechercher_place(v)
        
        self.assertIsNotNone(p, "Le parking devrait trouver une place libre.")
        self.assertEqual(p.get_id(), "A1")

    def test_recherche_place_trop_grande(self):
        """Une voiture trop grande doit être refusée"""
        # Voiture H=8.0 (Plus grand que 6.0)
        # Elle sera refusée peu importe si c'est la hauteur ou la longueur
        v = Voiture("BIG-TRUCK", 8.0, 8.0)
        p = self.parking.rechercher_place(v)
        
        self.assertIsNone(p, "Le parking ne devrait pas proposer de place pour ce camion.")

    def test_calcul_places_libres(self):
        """Vérifie que le compteur de places libres fonctionne"""
        # Au début : 1 place libre
        self.parking.calculer_places_libres_total()
        self.assertEqual(self.parking.nbPlacesLibres, 1)
        
        # On simule une occupation
        self.parking.mesPlaces[0].est_libre = False
        
        # Maintenant : 0 place libre
        self.parking.calculer_places_libres_total()
        self.assertEqual(self.parking.nbPlacesLibres, 0)

if __name__ == '__main__':
    unittest.main()