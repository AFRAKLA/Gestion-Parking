import pickle
import os

class Parking:
    def __init__(self):
        """ Initialise les structures de données principales (places, clients, archives) et définit le fichier de sauvegarde. """
        self.mesPlaces = []
        self.clients = []
        self.archives = []
        self.chiffre_affaires = 0.0
        
        self.fichier_data = "data_parking.pkl"

    def rechercher_place(self, voiture):
        """ Parcourt la liste des places pour trouver un emplacement libre compatible avec les dimensions du véhicule. """
        for place in self.mesPlaces:
            if place.est_libre:
                if (voiture.hauteur <= place.hauteur) and (voiture.longueur <= place.longueur):
                    return place
        return None

    def calculer_places_libres_total(self):
        """ Compte le nombre de places actuellement libres dans le parking et met à jour l'attribut correspondant. """
        compteur = 0
        for p in self.mesPlaces:
            if p.est_libre:
                compteur += 1
        self.nbPlacesLibres = compteur
        return compteur

    def archiver_sortie(self, voiture, nom_place, date_entree):
        """ Calcule le montant dû en fonction de la durée, met à jour le chiffre d'affaires et enregistre la transaction dans l'historique. """
        from datetime import datetime
        date_sortie = datetime.now()
        duree = date_sortie - date_entree
        
        minutes = duree.total_seconds() / 60
        prix = minutes * 0.5
        
        statut = "Standard"
        if voiture.proprietaire.pack_garantie: statut = "Pack Garantie"
        elif voiture.proprietaire.est_abonne: statut = "Abonné"

        self.chiffre_affaires += prix

        archive = {
            "client": voiture.proprietaire.nom,
            "place": nom_place,
            "entree": date_entree.strftime("%H:%M"),
            "sortie": date_sortie.strftime("%H:%M"),
            "duree": f"{int(minutes)} min",
            "prix": prix,
            "statut": statut
        }
        self.archives.append(archive)

    def sauvegarder_donnees(self):
        """ Utilise le module pickle pour enregistrer l'état complet du parking dans un fichier binaire. """
        try:
            chemin_absolu = os.path.abspath(self.fichier_data)
            
            with open(self.fichier_data, "wb") as fichier:
                pickle.dump(self, fichier)
            
        except Exception as e:
            print(f"Erreur lors de la sauvegarde : {e}")

    @staticmethod
    def charger_donnees():
        """ Tente de récupérer les données du parking depuis le fichier de sauvegarde s'il existe. """
        fichier_data = "data_parking.pkl"
        
        if os.path.exists(fichier_data):
            try:
                with open(fichier_data, "rb") as fichier:
                    donnees = pickle.load(fichier)
                    return donnees
            except Exception as e:
                print(f"Erreur lors du chargement (Fichier corrompu ?) : {e}")
                return None
        else:
            return None