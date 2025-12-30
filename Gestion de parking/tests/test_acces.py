import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.acces import Acces
from src.models.client import Client
from src.models.voiture import Voiture
from src.models.parking import Parking
from src.models.place import Place

class TestAcces(unittest.TestCase):
    
    def setUp(self):
        """ Préparation de l'environnement de test : création d'un parking avec une place large (6x6) et d'un client standard. """
        self.acces = Acces(1)
        self.parking = Parking()
        
        # On crée une place carrée de 6m x 6m pour éviter tout problème d'orientation (Hauteur/Longueur)
        self.parking.mesPlaces = [Place(1, "A", 6.0, 6.0)]
        
        self.parking.calculer_places_libres_total()
        
        self.client = Client("TestClient", "Toulouse")
        # Voiture standard (H=2.0, L=4.0) qui rentre largement dans 6x6
        self.client.ma_voiture = Voiture("TEST-CAR", 2.0, 4.0)

    @patch('src.models.borne_ticket.BorneTicket.demander_statut_initial')
    @patch('src.models.borne_ticket.BorneTicket.demander_pack_garantie')
    @patch('src.models.borne_ticket.BorneTicket.proposer_type_paiement')
    @patch('src.models.borne_ticket.BorneTicket.delivrer_ticket')
    def test_entree_reussie(self, mock_ticket, mock_paiement, mock_pack, mock_statut):
        """ Teste le scénario nominal : le client entre normalement, prend un ticket standard et se gare. """
        mock_statut.return_value = "Non (Visiteur)"
        mock_pack.return_value = "Non (Standard)"
        
        res = self.acces.lancer_procedure_entree(self.client, self.parking)
        
        self.assertIn("Réussie", res)
        self.assertTrue(self.client.ma_voiture.est_dans_parking)
        self.assertFalse(self.parking.mesPlaces[0].est_libre)

    @patch('src.models.borne_ticket.BorneTicket.demander_statut_initial')
    @patch('src.models.borne_ticket.BorneTicket.demander_pack_garantie')
    @patch('src.models.borne_ticket.BorneTicket.proposer_type_paiement')
    @patch('src.models.borne_ticket.BorneTicket.delivrer_ticket')
    def test_refus_taille(self, mock_ticket, mock_paiement, mock_pack, mock_statut):
        """ Vérifie que le système refuse l'entrée si le véhicule dépasse les dimensions de la place (8m de long vs 6m). """
        self.client.ma_voiture = Voiture("MONSTER", 4.0, 8.0)
        
        mock_statut.return_value = "Non (Visiteur)"
        mock_pack.return_value = "Non (Standard)"
        
        res = self.acces.lancer_procedure_entree(self.client, self.parking)
        
        self.assertIn("REFUS", res)
        self.assertFalse(self.client.ma_voiture.est_dans_parking)
        self.assertTrue(self.parking.mesPlaces[0].est_libre)

    @patch('src.models.borne_ticket.BorneTicket.demander_statut_initial')
    @patch('src.models.borne_ticket.BorneTicket.demander_pack_garantie')
    @patch('src.models.borne_ticket.BorneTicket.proposer_services')
    @patch('src.models.borne_ticket.BorneTicket.proposer_type_paiement')
    @patch('src.models.borne_ticket.BorneTicket.delivrer_ticket')
    def test_entree_pack_garantie(self, mock_tick, mock_pay, mock_srv, mock_pack, mock_statut):
        """ Vérifie que le Pack Garantie force l'entrée (stockage externe) même si le parking est complet physiquement. """
        # On sature artificiellement le parking
        self.parking.mesPlaces[0].est_libre = False 
        self.parking.calculer_places_libres_total() 
        
        mock_statut.return_value = "Non (Visiteur)"
        mock_pack.return_value = "Oui (Pack)" 
        mock_srv.return_value = "Aucun"
        
        res = self.acces.lancer_procedure_entree(self.client, self.parking)
        
        self.assertIn("PACK", res)
        self.assertTrue(self.client.ma_voiture.est_dans_parking)
        self.assertTrue(self.client.ma_voiture.est_aguerir_ailleurs)

if __name__ == "__main__":
    unittest.main()