import unittest
from unittest.mock import patch, mock_open
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.utils.generateur_html import GenerateurRapport
from src.models.parking import Parking

class TestGenerateurHtml(unittest.TestCase):
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('webbrowser.open')
    def test_generation_html(self, mock_browser, mock_file):
        """ Vérifie que le générateur crée bien un fichier et tente d'ouvrir le navigateur sans effectuer les actions réelles (Mock). """
        p = Parking()
        GenerateurRapport.generer_rapport(p)
        
        mock_file.assert_called()
        mock_browser.assert_called()

if __name__ == '__main__':
    unittest.main()