class Camera:
    def __init__(self):
        """ Initialise la caméra et la met en état de fonctionnement (ACTIVE). """
        self.statut = "ACTIVE"

    def capturer_hauteur(self, voiture) -> float:
        """ Simule la mesure physique de la hauteur du véhicule via des capteurs. """
        return voiture.hauteur

    def capturer_longueur(self, voiture) -> float:
        """ Simule la mesure de la longueur du véhicule. """
        return voiture.longueur

    def capturer_immatriculation(self, voiture) -> str:
        """ Simule la reconnaissance optique de caractères (OCR) pour lire la plaque d'immatriculation. """
        return voiture.immatriculation
    
    def scanner_plaque(self, voiture):
        """ Effectue un scan simple et retourne un message formaté pour l'affichage ou les tests unitaires. """
        if voiture:
            immat = self.capturer_immatriculation(voiture)
            return f"Scan OK : {immat}"
        return "Erreur : Aucun véhicule détecté"

    def scan_complet(self, voiture):
        """ Réalise une analyse complète du véhicule et renvoie un dictionnaire contenant les dimensions et l'immatriculation pour le contrôle d'accès. """
        if not voiture:
            return None
        
        return {
            "immatriculation": self.capturer_immatriculation(voiture),
            "hauteur": self.capturer_hauteur(voiture),
            "longueur": self.capturer_longueur(voiture)
        }