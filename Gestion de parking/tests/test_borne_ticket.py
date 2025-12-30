import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.borne_ticket import BorneTicket

class TestBorneTicket(unittest.TestCase):
    
    @patch('tkinter.Toplevel') 
    def test_menu_choix(self, mock_toplevel):
        """ Vérifie la logique de sélection des menus en simulant le clic utilisateur via un Mock, sans ouvrir l'interface graphique réelle. """
        borne = BorneTicket()
        
        with patch.object(BorneTicket, '_choix', return_value="Oui"):
            rep = borne.demander_statut_initial()
            self.assertEqual(rep, "Oui")

if __name__ == '__main__':
    unittest.main()