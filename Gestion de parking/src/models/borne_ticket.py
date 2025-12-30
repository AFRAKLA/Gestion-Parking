import tkinter as tk
from tkinter import messagebox

COLOR_BG_POPUP = "#F4F7F6"
COLOR_BTN_PRIMARY = "#3498DB"
COLOR_BTN_SECONDARY = "#95a5a6"
COLOR_TEXT = "#2C3E50"

class BorneTicket:
    
    def _choix(self, title, message, options):
        """ Méthode alias utilisée par les tests unitaires pour intercepter les interactions graphiques (Mocking). """
        opt1 = options[0]
        opt2 = options[1] if len(options) > 1 else None
        opt3 = options[2] if len(options) > 2 else None
        return self._demander_choix_boutons(title, message, opt1, opt2, opt3)

    def _demander_choix_boutons(self, title, message, option1, option2, option3=None):
        """ Affiche une fenêtre popup personnalisée avec 2 ou 3 boutons de choix et retourne la sélection de l'utilisateur. """
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.configure(bg=COLOR_BG_POPUP)
        
        width = 550 if option3 else 450
        dialog.geometry(f"{width}x240")
        dialog.resizable(False, False)
        
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (240 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        dialog.transient() 
        dialog.grab_set()  
        
        self.choix_user = None
        def set_choix(valeur):
            self.choix_user = valeur
            dialog.destroy()

        tk.Label(dialog, text=message, font=("Helvetica Neue", 13), bg=COLOR_BG_POPUP, wraplength=width-40, fg=COLOR_TEXT).pack(pady=(30, 20))
        
        frame_btn = tk.Frame(dialog, bg=COLOR_BG_POPUP)
        frame_btn.pack(pady=10)
        btn_style = {"font": ("Helvetica Neue", 10, "bold"), "width": 18, "height": 2, "relief": "flat", "borderwidth": 0, "cursor": "hand2"}

        tk.Button(frame_btn, text=option1, command=lambda: set_choix(option1), bg=COLOR_BTN_PRIMARY, fg="white", **btn_style).pack(side="left", padx=10)

        col2 = COLOR_BTN_SECONDARY if option2 and ("Non" in option2 or "Visiteur" in option2 or "Standard" in option2) else COLOR_BTN_PRIMARY
        if option2:
            tk.Button(frame_btn, text=option2, command=lambda: set_choix(option2), bg=col2, fg="white", **btn_style).pack(side="left", padx=10)

        if option3:
             tk.Button(frame_btn, text=option3, command=lambda: set_choix(option3), bg="#8E44AD", fg="white", **btn_style).pack(side="left", padx=10)

        dialog.wait_window()
        return self.choix_user if self.choix_user else (option2 if option2 else option1)

    def _demander_texte(self, title, prompt):
        """ Ouvre une fenêtre popup avec un champ de saisie texte (Entry) et retourne la chaîne saisie. """
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.configure(bg=COLOR_BG_POPUP)
        dialog.geometry("400x200")
        dialog.resizable(False, False)
        
        x = (dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (dialog.winfo_screenheight() // 2) - (200 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        dialog.transient()
        dialog.grab_set()
        
        self.saisie_user = None
        
        tk.Label(dialog, text=prompt, font=("Helvetica Neue", 12), bg=COLOR_BG_POPUP, fg=COLOR_TEXT).pack(pady=(30, 10))
        entry = tk.Entry(dialog, font=("Helvetica Neue", 12), width=30)
        entry.pack(pady=10)
        entry.focus_set()
        
        def valider(event=None):
            self.saisie_user = entry.get()
            dialog.destroy()
            
        entry.bind('<Return>', valider)
        tk.Button(dialog, text="Valider", command=valider, bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", font=("Helvetica", 10, "bold"), width=15).pack(pady=10)
        
        dialog.wait_window()
        return self.saisie_user

    def _demander_heure(self, title, prompt):
        """ Ouvre une fenêtre popup permettant de sélectionner une heure (HH:MM) via des Spinbox. """
        dialog = tk.Toplevel()
        dialog.title(title)
        dialog.configure(bg=COLOR_BG_POPUP)
        dialog.geometry("350x220")
        dialog.resizable(False, False)
        
        x = (dialog.winfo_screenwidth() // 2) - (350 // 2)
        y = (dialog.winfo_screenheight() // 2) - (220 // 2)
        dialog.geometry(f'+{x}+{y}')
        
        dialog.transient()
        dialog.grab_set()
        
        self.heure_choisie = None
        
        tk.Label(dialog, text=prompt, font=("Helvetica Neue", 12), bg=COLOR_BG_POPUP, fg=COLOR_TEXT).pack(pady=(20, 15))
        frame_time = tk.Frame(dialog, bg=COLOR_BG_POPUP); frame_time.pack()
        
        sb_h = tk.Spinbox(frame_time, from_=0, to=23, width=3, font=("Arial", 20, "bold"), format="%02.0f", justify="center", wrap=True)
        sb_h.pack(side="left", padx=5)
        tk.Label(frame_time, text=":", font=("Arial", 20, "bold"), bg=COLOR_BG_POPUP).pack(side="left")
        sb_m = tk.Spinbox(frame_time, from_=0, to=59, width=3, font=("Arial", 20, "bold"), format="%02.0f", justify="center", wrap=True)
        sb_m.pack(side="left", padx=5)

        def valider():
            self.heure_choisie = f"{int(sb_h.get()):02d}:{int(sb_m.get()):02d}"
            dialog.destroy()

        tk.Button(dialog, text="Valider Heure", command=valider, bg=COLOR_BTN_PRIMARY, fg="white", relief="flat", font=("Helvetica", 10, "bold"), width=15).pack(pady=30)
        dialog.wait_window()
        return self.heure_choisie

    def delivrer_ticket(self, client) -> str:
        """ Simule l'impression physique d'un ticket en générant un code aléatoire. """
        import random
        return f"TICKET-{random.randint(1000, 9999)}"

    def demander_statut_initial(self) -> str:
        """ Étape 1 : Demande au client s'il possède déjà un abonnement. """
        return self._choix(
            "Étape 1/4 : Identification", 
            "Êtes-vous déjà client Abonné ?", 
            ["Oui (Abonné)", "Non (Visiteur)"]
        )

    def demander_pack_garantie(self) -> str:
        """ Étape 2 : Propose l'activation de l'option 'Pack Garantie' pour sécuriser une place. """
        return self._choix(
            "Étape 2/4 : Garantie Stationnement", 
            "Souhaitez-vous activer le 'Pack Garantie' ?\n(Place assurée même si complet + Services inclus)", 
            ["Oui (Pack Garantie)", "Non (Standard)"]
        )

    def proposer_services(self, client) -> str:
        """ Étape 3 : Propose des services additionnels (Livraison, Maintenance) aux clients éligibles. """
        choix = self._choix("Étape 3/4 : Services Premium", "Désirez-vous un service optionnel (Livraison, Entretien) ?", ["Oui", "Non"])
        
        if choix == "Oui":
            type_service = self._choix("Type de Service", "Quel service souhaitez-vous ?", ["Livraison", "Maintenance"])
            
            if type_service == "Livraison":
                adr = self._demander_texte("Livraison", "Veuillez saisir l'adresse de livraison :")
                if adr:
                    heure = self._demander_heure("Livraison", "Choisissez l'heure de livraison :")
                    if heure:
                        client.definir_service("Livraison", adr, heure)
            
            elif type_service == "Maintenance":
                client.definir_service("Maintenance")
            return "OK"
        return "Aucun"

    def proposer_type_paiement(self, client) -> str:
        """ Étape 4 : Invite le client à choisir son moyen de paiement, en signalant les tarifs réduits. """
        msg = "Veuillez choisir votre mode de paiement :"
        if client.est_abonne or client.pack_garantie:
            msg += "\n\n✨ INFO : Tarif réduit appliqué !"
        
        choix = self._choix("Étape 4/4 : Paiement", msg, ["Carte Bancaire", "Espèces"])
        return choix if choix else "Carte Bancaire"

    def recuperer_infos_carte(self, client) -> str:
        """ Simule la lecture électronique de la carte bancaire du client. """
        return f"Carte_Puce_{client.nom}"