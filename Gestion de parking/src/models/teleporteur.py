class Teleporteur:
    def teleporter_voiture(self, voiture, place, placement):
        """ Simule le déplacement instantané d'un véhicule vers sa place attribuée pour fluidifier le trafic. """
        print(f"Téléportation de {voiture.immatriculation} vers {place.get_id()}")

    def teleporter_voiture_super_abonne(self, voiture):
        """ Méthode réservée pour une future extension de téléportation VIP (non implémentée pour cette version). """
        pass