import sys
import os

"""
Projet Python - Gestion de Parking
Université Toulouse 2 - Jean-Jaurès
Auteurs : Alaeddine & Karim
"""

current_dir = os.path.dirname(os.path.abspath(__file__))

root_dir = os.path.dirname(current_dir)

sys.path.append(root_dir)

from src.views.interface import ParkingGUI

def main():
    """ Point d'entrée de l'application : lance l'interface graphique qui initialise l'ensemble du système de parking. """
    app = ParkingGUI()
    app.mainloop()

if __name__ == "__main__":
    main()