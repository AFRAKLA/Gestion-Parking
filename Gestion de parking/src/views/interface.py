import sys
import os
import time
import customtkinter as ctk

# Fix imports
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(os.path.dirname(current_dir))
if project_root not in sys.path: sys.path.append(project_root)

# IMPORT DU CONTROLEUR
from src.controllers.parking_controller import ParkingController

# --- CONFIGURATION DU DESIGN ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

class ParkingGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("DREAM PARK • COMMANDER CENTER [v3.0 MVC]")
        self.geometry("1100x750")
        self.minsize(1000, 700)
        
        # Centrage
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = int((screen_width - 1100) / 2)
        y = int((screen_height - 750) / 2)
        self.geometry(f"1100x750+{x}+{y}")

        # --- INITIALISATION MVC ---
        # La vue crée le contrôleur et lui passe 'self' (elle-même)
        self.controller = ParkingController(self)
        
        # Pour faciliter l'affichage, on garde un lien vers les données via le contrôleur
        self.parking = self.controller.parking 

        # Layout Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.setup_sidebar()

        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.setup_dashboard()

        self.rafraichir_interface()

    # --- MÉTHODES D'AFFICHAGE (UI) ---

    def popup_custom(self, title, message, is_error=False):
        top = ctk.CTkToplevel(self)
        top.title(title)
        w, h = 400, 200
        sw, sh = top.winfo_screenwidth(), top.winfo_screenheight()
        top.geometry(f"{w}x{h}+{int((sw-w)/2)}+{int((sh-h)/2)}")
        top.transient(self); top.grab_set()
        
        color = "#C0392B" if is_error else "#27AE60"
        ctk.CTkLabel(top, text=title.upper(), font=("Arial", 14, "bold"), text_color=color).pack(pady=(20, 10))
        ctk.CTkLabel(top, text=message, wraplength=350, font=("Arial", 12)).pack(pady=10, padx=20)
        ctk.CTkButton(top, text="OK", fg_color=color, width=100, command=top.destroy).pack(pady=20)
        self.wait_window(top)

    def demander_saisie(self, title, prompt):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        w, h = 400, 200
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"{w}x{h}+{int((sw-w)/2)}+{int((sh-h)/2)}")
        dialog.transient(self); dialog.grab_set()
        
        ctk.CTkLabel(dialog, text=prompt, font=("Arial", 12, "bold")).pack(pady=20)
        entry = ctk.CTkEntry(dialog, width=250)
        entry.pack(pady=10)
        entry.focus()
        
        self.user_input = None
        def valider():
            self.user_input = entry.get()
            dialog.destroy()
            
        ctk.CTkButton(dialog, text="Valider", fg_color="#3498DB", command=valider).pack(pady=20)
        self.wait_window(dialog)
        return self.user_input

    def demander_heure(self, title):
        dialog = ctk.CTkToplevel(self)
        dialog.title(title)
        w, h = 300, 250
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"{w}x{h}+{int((sw-w)/2)}+{int((sh-h)/2)}")
        dialog.transient(self); dialog.grab_set()

        ctk.CTkLabel(dialog, text="RÉGLAGE HEURE LIVRAISON", font=("Arial", 12, "bold")).pack(pady=15)
        self.h_val = 12
        self.m_val = 30
        f_time = ctk.CTkFrame(dialog, fg_color="transparent"); f_time.pack(pady=10)
        lbl_h = ctk.CTkLabel(f_time, text="12", font=("Arial", 40, "bold"), width=60)
        lbl_m = ctk.CTkLabel(f_time, text="30", font=("Arial", 40, "bold"), width=60)
        lbl_sep = ctk.CTkLabel(f_time, text=":", font=("Arial", 40, "bold"))

        def update_display():
            lbl_h.configure(text=f"{self.h_val:02d}")
            lbl_m.configure(text=f"{self.m_val:02d}")
        def inc_h(): self.h_val = (self.h_val + 1) % 24; update_display()
        def dec_h(): self.h_val = (self.h_val - 1) % 24; update_display()
        def inc_m(): self.m_val = (self.m_val + 5) % 60; update_display()
        def dec_m(): self.m_val = (self.m_val - 5) % 60; update_display()

        ctk.CTkButton(f_time, text="▲", width=40, command=inc_h, fg_color="#34495E").grid(row=0, column=0, padx=5)
        lbl_h.grid(row=1, column=0)
        ctk.CTkButton(f_time, text="▼", width=40, command=dec_h, fg_color="#34495E").grid(row=2, column=0, padx=5)
        lbl_sep.grid(row=1, column=1, padx=5)
        ctk.CTkButton(f_time, text="▲", width=40, command=inc_m, fg_color="#34495E").grid(row=0, column=2, padx=5)
        lbl_m.grid(row=1, column=2)
        ctk.CTkButton(f_time, text="▼", width=40, command=dec_m, fg_color="#34495E").grid(row=2, column=2, padx=5)

        self.final_time = None
        def valider():
            self.final_time = f"{self.h_val:02d}:{self.m_val:02d}"
            dialog.destroy()
        ctk.CTkButton(dialog, text="Valider Horaire", fg_color="#27AE60", command=valider).pack(pady=20)
        self.wait_window(dialog)
        return self.final_time

    def setup_sidebar(self):
        self.lbl_logo = ctk.CTkLabel(self.sidebar, text="DREAM PARK\nMANAGER", font=ctk.CTkFont(size=20, weight="bold"))
        self.lbl_logo.pack(pady=(40, 30))

        # --- ACTIONS DELEGUEES AU CONTROLEUR ---
        self.btn_entree = ctk.CTkButton(self.sidebar, text="▶  ENTRÉE VÉHICULE", height=40, fg_color="#27AE60", hover_color="#2ECC71", command=self.controller.traiter_entree)
        self.btn_entree.pack(padx=20, pady=10, fill="x")

        self.btn_sortie = ctk.CTkButton(self.sidebar, text="◀  SORTIE / PAIEMENT", height=40, fg_color="#C0392B", hover_color="#E74C3C", command=self.action_sortie_ui)
        self.btn_sortie.pack(padx=20, pady=10, fill="x")

        self.btn_flex = ctk.CTkButton(self.sidebar, text="📞  SERVICE CLIENT", height=40, fg_color="#D35400", hover_color="#E67E22", command=self.action_flexibilite_ui)
        self.btn_flex.pack(padx=20, pady=10, fill="x")

        ctk.CTkFrame(self.sidebar, height=2, fg_color="gray30").pack(fill="x", padx=20, pady=30)

        self.btn_rapport = ctk.CTkButton(self.sidebar, text="📄  RAPPORT HTML", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.controller.generer_html)
        self.btn_rapport.pack(padx=20, pady=10, fill="x")
        
        self.btn_rapport_txt = ctk.CTkButton(self.sidebar, text="📝  RAPPORT TXT", fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), command=self.controller.generer_txt)
        self.btn_rapport_txt.pack(padx=20, pady=5, fill="x")

        self.frame_footer = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.frame_footer.pack(side="bottom", pady=20, padx=10)
        ctk.CTkLabel(self.frame_footer, text="Application créer par\nAlaeddine et Karim\nMIASHS - PROJET PYTHON 2025", 
                     font=("Arial", 10), text_color="gray50").pack()

    def setup_dashboard(self):
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(1, weight=1)

        self.frame_stats = ctk.CTkFrame(self.main_area, height=100, corner_radius=10)
        self.frame_stats.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        self.setup_stats_bar()

        self.map_view = ctk.CTkTabview(self.main_area)
        self.map_view.grid(row=1, column=0, sticky="nsew")
        self.map_view.add("Niveau A"); self.map_view.add("Niveau B"); self.map_view.add("Niveau C")
        
        self.spot_widgets = {} 
        self.creer_grille_places("Niveau A", "A")
        self.creer_grille_places("Niveau B", "B")
        self.creer_grille_places("Niveau C", "C")

        self.console_frame = ctk.CTkFrame(self.main_area, height=150)
        self.console_frame.grid(row=2, column=0, sticky="ew", pady=(20, 0))
        
        ctk.CTkLabel(self.console_frame, text="SYSTEM LOGS", font=("Courier", 12, "bold")).pack(anchor="w", padx=10, pady=5)
        self.log_box = ctk.CTkTextbox(self.console_frame, height=100, font=("Courier", 12), text_color="#00FF00", fg_color="black")
        self.log_box.pack(fill="both", padx=5, pady=5)
        self.log("Système initialisé - Mode MVC Actif")

    def setup_stats_bar(self):
        self.frame_stats.grid_columnconfigure((0,1,2), weight=1)
        self.stat_libres = self._create_stat_card(self.frame_stats, 0, "PLACES LIBRES", "--", "#2980b9")
        self.stat_occup = self._create_stat_card(self.frame_stats, 1, "VÉHICULES PRÉSENTS", "--", "#27ae60")
        self.stat_revenue = self._create_stat_card(self.frame_stats, 2, "REVENU ESTIMÉ", "--", "#f39c12")

    def _create_stat_card(self, parent, col, title, value, color):
        frame = ctk.CTkFrame(parent, fg_color=color)
        frame.grid(row=0, column=col, padx=10, pady=10, sticky="nsew")
        lbl_val = ctk.CTkLabel(frame, text=value, font=("Arial", 32, "bold"), text_color="white")
        lbl_val.pack(expand=True, pady=(10,0))
        lbl_title = ctk.CTkLabel(frame, text=title, font=("Arial", 10), text_color="white")
        lbl_title.pack(expand=True, pady=(0,10))
        return lbl_val

    def creer_grille_places(self, tab_name, niveau_prefix):
        tab = self.map_view.tab(tab_name)
        tab.grid_columnconfigure((0,1), weight=1) 
        row, col = 0, 0
        places_niveau = [p for p in self.parking.mesPlaces if p.get_id().startswith(niveau_prefix)]
        
        for place in places_niveau:
            btn = ctk.CTkButton(
                tab, text=f"{place.get_id()}\nLIBRE", 
                width=180, height=100, corner_radius=15,
                font=("Arial", 16, "bold"), fg_color="#34495E", hover=False
            )
            btn.grid(row=row, column=col, padx=15, pady=15)
            self.spot_widgets[place.get_id()] = btn
            col += 1
            if col > 1: col = 0; row += 1

    def log(self, message):
        timestamp = time.strftime("[%H:%M:%S]")
        self.log_box.insert("end", f"{timestamp} > {message}\n")
        self.log_box.see("end")

    def rafraichir_interface(self):
        self.parking.calculer_places_libres_total()
        self.stat_libres.configure(text=str(self.parking.nbPlacesLibres))
        self.stat_occup.configure(text=str(len(self.parking.clients)))
        self.stat_revenue.configure(text=f"{self.parking.chiffre_affaires:.2f} €")

        for place in self.parking.mesPlaces:
            widget = self.spot_widgets.get(place.get_id())
            if widget:
                if place.est_libre:
                    widget.configure(fg_color="#34495E", text=f"{place.get_id()}\nLIBRE")
                else:
                    widget.configure(fg_color="#C0392B", text=f"{place.get_id()}\nOCCUPÉ")
        self.update_idletasks()

    # --- UI SPECIFIQUES (SELECTION) QUI APPELLENT ENSUITE LE CONTROLEUR ---

    def action_sortie_ui(self):
        if not self.parking.clients:
            self.popup_custom("Erreur", "Le parking est vide !", is_error=True)
            return

        self.log("Demande de sortie...")
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Sélection Véhicule")
        dialog.geometry("500x550")
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"500x550+{int((sw-500)/2)}+{int((sh-550)/2)}")
        dialog.transient(self); dialog.grab_set()
        
        ctk.CTkLabel(dialog, text="SCANNER TICKET (Sélection)", font=("Arial", 16, "bold")).pack(pady=20)
        scroll_frame = ctk.CTkScrollableFrame(dialog, width=450, height=400)
        scroll_frame.pack(pady=10)

        def confirmer_sortie(cli_obj):
            dialog.destroy()
            self.controller.traiter_sortie(cli_obj)

        for cli in self.parking.clients:
            v = cli.ma_voiture
            immat = v.immatriculation if v else "?"
            nom_place = "INCONNU"
            color_btn = "#34495E"
            if v and v.est_aguerir_ailleurs:
                nom_place = "EXTERNE"; color_btn = "#8E44AD"
            else:
                if v:
                    placement_actif = None
                    for p in v.mes_placements:
                        if p.est_en_cours: placement_actif = p; break
                    if placement_actif:
                        for place in self.parking.mesPlaces:
                            if placement_actif in place.mes_placements:
                                nom_place = f"PLACE {place.get_id()}"; break
            
            btn_text = f"[{nom_place}]   {cli.nom}   |   {immat}"
            ctk.CTkButton(scroll_frame, text=btn_text, font=("Courier", 13, "bold"), fg_color=color_btn, height=40, anchor="w", command=lambda c=cli: confirmer_sortie(c)).pack(pady=5, padx=5, fill="x")

    def action_flexibilite_ui(self):
        if not self.parking.clients:
            self.log("Erreur: Pas de client dans le parking.")
            self.popup_custom("Info", "Aucun client à contacter.", True)
            return
        
        dialog = ctk.CTkToplevel(self)
        dialog.title("Centre d'Appels - Sélection Client")
        dialog.geometry("500x500")
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"500x500+{int((sw-500)/2)}+{int((sh-500)/2)}")
        dialog.transient(self); dialog.grab_set()

        ctk.CTkLabel(dialog, text="QUI VOULEZ-VOUS CONTACTER ?", font=("Arial", 16, "bold")).pack(pady=15)
        scroll = ctk.CTkScrollableFrame(dialog, width=450, height=350)
        scroll.pack(pady=10)

        def choisir_client(c):
            dialog.destroy()
            self._ui_gerer_service_client(c)

        for cli in self.parking.clients:
            srv = cli.service_demande if cli.service_demande else "Aucun"
            color = "#34495E"
            if "Livraison" in srv: color = "#D35400"
            elif "Maintenance" in srv: color = "#8E44AD"

            txt = f"{cli.nom}  |  Service: {srv}"
            ctk.CTkButton(scroll, text=txt, fg_color=color, height=40, anchor="w", command=lambda x=cli: choisir_client(x)).pack(pady=5, padx=5, fill="x")

    def _ui_gerer_service_client(self, client):
        self.log(f"Connexion établie avec {client.nom}...")
        
        dialog = ctk.CTkToplevel(self)
        dialog.title(f"Dossier : {client.nom}")
        dialog.geometry("400x350")
        sw, sh = dialog.winfo_screenwidth(), dialog.winfo_screenheight()
        dialog.geometry(f"400x350+{int((sw-400)/2)}+{int((sh-350)/2)}")
        dialog.transient(self); dialog.grab_set()
        
        ctk.CTkLabel(dialog, text=f"CLIENT : {client.nom}", font=("Arial", 14, "bold")).pack(pady=15)
        ctk.CTkLabel(dialog, text=f"Service actuel : {client.service_demande}", text_color="#BDC3C7").pack(pady=5)
        
        def maintenance():
            dialog.destroy()
            self.controller.traiter_maintenance(client)

        def modifier_livraison():
            dialog.destroy()
            new_addr = self.demander_saisie("Modification Dossier", "Nouvelle Adresse de Livraison :")
            if new_addr:
                new_time = self.demander_heure("Horaire")
                if new_time:
                    self.controller.modifier_livraison(client, new_addr, new_time)

        ctk.CTkButton(dialog, text="Lancer Maintenance Immédiate", fg_color="#E67E22", command=maintenance).pack(pady=10)
        ctk.CTkButton(dialog, text="Modifier Livraison / Horaire", fg_color="#3498DB", command=modifier_livraison).pack(pady=10)

if __name__ == "__main__":
    app = ParkingGUI()
    app.mainloop()