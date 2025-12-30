class PanneauAffichage:
    def afficher_nb_places_disponibles(self, parking) -> str:
        """ Interroge le parking pour connaître le nombre de places restantes et affiche l'information sur l'écran d'entrée pour informer les conducteurs. """
        nb = parking.calculer_places_libres_total()
        msg = f"PLACES DISPONIBLES : {nb}"
        print(f"[PANNEAU] {msg}")
        return msg