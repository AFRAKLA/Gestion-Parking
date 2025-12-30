import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.client import Client

class TestClient(unittest.TestCase):
    
    def setUp(self):
        """ Initialise un client de test propre avant chaque exécution pour garantir l'indépendance des tests. """
        self.client = Client("Karim", "Toulouse")

    def test_initialisation(self):
        """ Vérifie que les attributs de base (nom, ville) sont correctement affectés à la création. """
        self.assertEqual(self.client.nom, "Karim")
        self.assertEqual(self.client.ville, "Toulouse")
        self.assertFalse(self.client.est_abonne)

    def test_activation_pack(self):
        """ S'assure que l'activation du Pack Garantie modifie bien les statuts d'abonnement et de garantie. """
        self.client.activer_pack_garantie()
        self.assertTrue(self.client.pack_garantie)
        self.assertTrue(self.client.est_abonne)

    def test_definir_service(self):
        """ Contrôle que les informations logistiques (adresse, heure) sont bien enregistrées lors d'une demande de service. """
        self.client.definir_service("Livraison", "Capitole", "10:00")
        self.assertEqual(self.client.service_demande, "Livraison")
        self.assertEqual(self.client.adresse_livraison, "Capitole")

if __name__ == '__main__':
    unittest.main()