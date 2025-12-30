import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.camera import Camera

class TestCamera(unittest.TestCase):
    
    def test_scan(self):
        """ Teste la robustesse de la caméra : vérifie que la méthode ne lève pas d'exception même si aucun véhicule n'est détecté (None). """
        cam = Camera()
        
        try:
            cam.scanner_plaque(None) 
        except Exception as e:
            self.fail(f"Camera.scanner_plaque a levé une erreur inattendue : {e}")

if __name__ == '__main__':
    unittest.main()