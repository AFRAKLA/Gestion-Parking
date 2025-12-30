from datetime import datetime
from src.models.borne_ticket import BorneTicket
from src.models.panneau_affichage import PanneauAffichage
from src.models.teleporteur import Teleporteur
from src.models.camera import Camera

class Acces:
    def __init__(self, id_acces: int):
        """ Initialise une voie d'accès équipée de tous les appareils nécessaires (borne, caméra, etc.) """
        self.id_acces = id_acces
        self.ma_camera = Camera()
        self.ma_borne = BorneTicket()
        self.mon_panneau = PanneauAffichage()
        self.tele_in = Teleporteur()
        self.tele_out = Teleporteur()

    def lancer_procedure_entree(self, client, parking) -> str:
        """ Orchestre le scénario complet d'entrée : dialogue avec la borne, vérification des places et placement du véhicule. """
        from src.models.placement import Placement
        
        voiture = client.ma_voiture
        if not voiture: 
            return "Erreur : Pas de véhicule détecté."

        if not client.est_abonne:
            if self.ma_borne.demander_statut_initial() == "Oui (Abonné)":
                client.est_abonne = True

        if self.ma_borne.demander_pack_garantie() == "Oui (Pack)":
            client.activer_pack_garantie()

        if client.est_abonne or client.pack_garantie:
            self.ma_borne.proposer_services(client)

        self.ma_borne.proposer_type_paiement(client)
        self.ma_borne.delivrer_ticket(client)

        place_trouvee = parking.rechercher_place(voiture)

        if place_trouvee is None:
            if client.pack_garantie:
                voiture.est_dans_parking = True
                voiture.est_aguerir_ailleurs = True 
                nv_placement = Placement(datetime.now())
                voiture.add_placement(nv_placement)
                client.enregistrer_visite()
                return "Parking COMPLET/INADAPTÉ.\n✅ PACK GARANTIE : Prise en charge externe validée."
            else:
                self.mon_panneau.afficher_nb_places_disponibles(parking)
                if parking.nbPlacesLibres > 0:
                    return f"REFUS : Votre véhicule ({voiture.hauteur:.2f}m x {voiture.longueur:.2f}m)\nest trop grand pour nos places disponibles."
                return "Parking COMPLET. Veuillez patienter."
        
        nv_placement = Placement(datetime.now())
        place_trouvee.add_placement(nv_placement)
        voiture.add_placement(nv_placement)
        voiture.est_dans_parking = True
        
        self.tele_in.teleporter_voiture(voiture, place_trouvee, nv_placement)
        client.enregistrer_visite()

        return f"Entrée Réussie.\nPlace attribuée : {place_trouvee.get_id()}"

    def lancer_procedure_sortie(self, client, parking) -> str:
        """ Gère le scénario de sortie : utilise l'objet 'parking' réel pour archiver la transaction correctement. """
        voiture = client.ma_voiture
        if not voiture: return "Erreur : Pas de voiture."

        placement_actif = None
        for p in voiture.mes_placements:
            if p.est_en_cours:
                placement_actif = p
                break
        
        if voiture.est_aguerir_ailleurs:
            if not placement_actif: 
                from src.models.placement import Placement
                placement_actif = Placement(datetime.now())

            parking.archiver_sortie(voiture, "EXTERNE", placement_actif.date_debut)
            
            placement_actif.partir_place()
            voiture.est_dans_parking = False
            voiture.est_aguerir_ailleurs = False
            return "Récupération Véhicule Externe (Pack Garantie)."
        
        if placement_actif:
            # On archive dans le VRAI parking
            parking.archiver_sortie(voiture, "INTERNE", placement_actif.date_debut)
            
            placement_actif.partir_place()
            voiture.est_dans_parking = False
            
            return "Sortie Validée. Merci de votre visite."
        
        return "Erreur : Ticket introuvable ou déjà sorti."