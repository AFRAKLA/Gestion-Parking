import unittest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.controllers.parking_controller import ParkingController

class TestParkingController(unittest.TestCase):
    
    def setUp(self):
        """ Initialise un environnement de test isolé avec une vue simulée (Mock) pour contrôler les réactions de l'interface. """
        self.mock_view = MagicMock()
        self.controller = ParkingController(self.mock_view)

    @patch('src.models.acces.Acces.lancer_procedure_entree')
    def test_traiter_entree_succes(self, mock_acces):
        """ Vérifie que le contrôleur gère correctement une entrée validée en mettant à jour la vue (popup succès + rafraîchissement). """
        mock_acces.return_value = "Entrée Réussie"
        
        self.controller.traiter_entree()
        
        self.mock_view.popup_custom.assert_called_with("Succès Entrée", "Entrée Réussie", is_error=False)
        self.mock_view.rafraichir_interface.assert_called()

    def test_modifier_livraison(self):
        """ S'assure que la modification des paramètres de livraison est bien transmise à l'objet client concerné. """
        client = MagicMock()
        self.controller.modifier_livraison(client, "Paris", "12:00")
        
        client.definir_service.assert_called_with("Livraison Modifiée", "Paris", "12:00")

if __name__ == '__main__':
    unittest.main()