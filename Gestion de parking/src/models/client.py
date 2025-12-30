class Client:
    def __init__(self, nom, ville):
        """ Initialise un nouveau client avec ses informations personnelles de base et un statut par défaut (non abonné). """
        self.nom = nom
        self.ville = ville
        self.est_abonne = False
        self.pack_garantie = False
        self.ma_voiture = None
        
        # Gestion des services optionnels
        self.service_demande = "Aucun"
        self.adresse_livraison = None
        self.heure_livraison = None
        
        # Statistiques de fidélité
        self.nb_frequentations = 1

    def activer_pack_garantie(self):
        """ Active l'option 'Pack Garantie' qui assure une place de stationnement et confère automatiquement le statut d'abonné. """
        self.pack_garantie = True
        self.est_abonne = True 

    def definir_service(self, type_service, adresse=None, heure=None):
        """ Enregistre une demande de service spécifique (ex: Livraison, Maintenance) avec ses paramètres logistiques (adresse, horaire). """
        self.service_demande = type_service
        self.adresse_livraison = adresse
        self.heure_livraison = heure

    def enregistrer_visite(self):
        """ Incrémente le compteur de visites du client pour le suivi statistique et la fidélité. """
        self.nb_frequentations += 1