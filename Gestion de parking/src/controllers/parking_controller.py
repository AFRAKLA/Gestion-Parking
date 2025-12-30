import os
import sys
import random
import time
from datetime import datetime

from src.models.parking import Parking
from src.models.acces import Acces
from src.models.client import Client
from src.models.voiture import Voiture
from src.models.place import Place
from src.utils.generateur_html import GenerateurRapport

class ParkingController:
    def __init__(self, view):
        """ Initialisation du contrôleur : on lie la vue, on prépare l'accès et on charge les données si elles existent. """
        self.view = view
        self.acces = Acces(1)
        self.compteur_clients = 1
        
        loaded = Parking.charger_donnees()
        if loaded:
            self.parking = loaded
            if self.parking.clients:
                try:
                    last_name = self.parking.clients[-1].nom
                    self.compteur_clients = int(last_name.split("°")[-1]) + 1
                except:
                    self.compteur_clients = len(self.parking.clients) + 1
        else:
            self.parking = Parking()
            if not self.parking.mesPlaces:
                for niv in ["A", "B", "C"]:
                    for i in range(1, 5):
                        self.parking.mesPlaces.append(Place(i, niv, hauteur=3.0, longueur=6.0))

    def sauvegarder(self):
        """ Déclenche l'enregistrement des données du parking dans le fichier de sauvegarde. """
        self.parking.sauvegarder_donnees()

    def traiter_entree(self):
        """ Gère l'arrivée d'un client : création voiture, simulation aléatoire des dimensions et validation via la borne. """
        self.view.log("Procédure d'entrée initiée...")
        
        nom_client = f"Client N°{self.compteur_clients}"
        self.compteur_clients += 1
        client = Client(nom_client, "Toulouse")
        
        veut_provoquer_refus = (random.random() < 0.05)

        if veut_provoquer_refus:
            h = random.uniform(3.1, 4.0)
            l = random.uniform(6.1, 8.0)
            print(f"[DEBUG] Génération HORS GABARIT ({h:.2f}m x {l:.2f}m)")
        else:
            h = random.uniform(1.4, 2.5) 
            l = random.uniform(3.0, 5.0) 

        v = Voiture(f"FR-{random.randint(10,99)}-KZ", h, l)
        client.ma_voiture = v; v.proprietaire = client
        
        res = self.acces.lancer_procedure_entree(client, self.parking)
        
        if "Réussie" in res or "réussie" in res or "PACK" in res:
            self.view.log(f"ACCÈS AUTORISÉ : {client.nom}")
            self.parking.clients.append(client)
            if "PACK" in res: self.view.log(">>> PACK GARANTIE ACTIVÉ (Parking Externe)")
            
            self.parking.chiffre_affaires += 15.0
            self.sauvegarder()
            self.view.popup_custom("Succès Entrée", res, is_error=False)
        else:
            self.view.log(f"ACCÈS REFUSÉ : {res}")
            self.compteur_clients -= 1 
            self.view.popup_custom("Refus d'accès", res, is_error=True)

        self.view.rafraichir_interface()

    def traiter_sortie(self, client):
        """ Organise la sortie : libération de la place, archivage de la transaction et mise à jour de l'interface. """
        if client in self.parking.clients:
            self.parking.clients.remove(client)
        
        self.view.log(f"Traitement sortie pour {client.nom}...")

        res = self.acces.lancer_procedure_sortie(client, self.parking)
       
        
        if client.ma_voiture and not client.ma_voiture.est_aguerir_ailleurs:
             for place in self.parking.mesPlaces:
                 for ticket in client.ma_voiture.mes_placements:
                     if ticket in place.mes_placements:
                         place.est_libre = True

        self.view.log(f"SORTIE VALIDÉE : {res}")
        self.sauvegarder()
        self.view.popup_custom("Sortie Validée", res, is_error=False)
        self.view.rafraichir_interface()

    def traiter_maintenance(self, client):
        """ Simule l'envoi d'un véhicule en maintenance et sa réaffectation à une place après délai. """
        self.view.log(f"DEMANDE MAINTENANCE -> {client.nom}")
        voiture = client.ma_voiture
        place_concernee = None
        
        for p in self.parking.mesPlaces:
                if not p.est_libre and any(pl.est_en_cours for pl in p.mes_placements):
                    place_concernee = p; break 
        
        if place_concernee:
            place_concernee.est_libre = True
            self.view.rafraichir_interface()
            self.view.log(">>> Véhicule en atelier...")
            self.view.update()
            time.sleep(1.5)
            self.view.log(">>> Retour Véhicule...")
            
            new_place = self.parking.rechercher_place(voiture)
            if new_place:
                new_place.est_libre = False
                self.view.log(f"Véhicule garé sur {new_place.get_id()}")
            
            self.sauvegarder()
            self.view.rafraichir_interface()

    def modifier_livraison(self, client, new_addr, new_time):
        """ Permet de mettre à jour l'adresse et l'heure de livraison d'un client existant. """
        client.definir_service("Livraison Modifiée", new_addr, new_time)
        self.view.log(f">>> DOSSIER MIS À JOUR : {new_addr} à {new_time}")
        self.sauvegarder()
        self.view.popup_custom("Succès", f"Livraison reprogrammée.\n\n📍 {new_addr}\n⏰ {new_time}", is_error=False)

    def generer_html(self):
        """ Lance la génération du rapport HTML via l'utilitaire dédié. """
        if not self.parking.archives and not self.parking.clients:
             self.view.popup_custom("Info", "Pas assez de données.", is_error=True); return
        path = GenerateurRapport.generer_rapport(self.parking)
        self.view.log(f"Rapport HTML généré : {path}")
        self.view.popup_custom("Rapport HTML", f"Le rapport a été ouvert.\n{path}", is_error=False)

    def generer_txt(self):
        """ Lance la génération du rapport texte simple via l'utilitaire dédié. """
        if not self.parking.archives and not self.parking.clients:
             self.view.popup_custom("Info", "Pas assez de données.", is_error=True); return
        path = GenerateurRapport.generer_txt(self.parking)
        self.view.log(f"Rapport TXT généré : {path}")
        self.view.popup_custom("Rapport TXT Généré", f"Le fichier texte a été créé.\n\nChemin: {path}", is_error=False)
        try: os.startfile(path)
        except: pass