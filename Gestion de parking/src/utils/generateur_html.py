import os
import webbrowser
from datetime import datetime

class GenerateurRapport:
    
    @staticmethod
    def generer_txt(parking):
        """ Génère un rapport textuel simple (.txt) récapitulant les indicateurs clés et l'historique du parking. """
        filename = "Rapport_DreamPark.txt"
        full_path = os.path.join(os.getcwd(), filename)
        
        nb_total = len(parking.mesPlaces)
        nb_occupes = len(parking.clients)
        taux = (nb_occupes / nb_total * 100) if nb_total > 0 else 0
        ca_total = parking.chiffre_affaires

        with open(full_path, "w", encoding="utf-8") as f:
            f.write("==================================================\n")
            f.write("       DREAM PARK MANAGER - RAPPORT SYSTÈME       \n")
            f.write("==================================================\n")
            f.write(f"Date de génération : {datetime.now().strftime('%d/%m/%Y à %H:%M')}\n")
            f.write("--------------------------------------------------\n\n")
            
            f.write("[1] INDICATEURS CLÉS (KPI)\n")
            f.write(f"    - Chiffre d'Affaires : {ca_total:.2f} €\n")
            f.write(f"    - Taux d'Occupation  : {int(taux)} %\n")
            f.write(f"    - Véhicules Présents : {nb_occupes}\n")
            f.write(f"    - Total Sorties      : {len(parking.archives)}\n\n")
            
            f.write("[2] VÉHICULES ACTUELLEMENT STATIONNÉS\n")
            if not parking.clients:
                f.write("    (Aucun véhicule sur site)\n")
            else:
                f.write(f"    {'CLIENT':<15} | {'IMMAT':<12} | {'STATUT':<15} | {'SERVICE'}\n")
                f.write("    " + "-"*60 + "\n")
                for cli in parking.clients:
                    v = cli.ma_voiture
                    immat = v.immatriculation if v else "N/A"
                    statut = "STANDARD"
                    if cli.pack_garantie: statut = "PACK GARANTIE"
                    elif cli.est_abonne: statut = "ABONNÉ"
                    
                    if v and v.est_aguerir_ailleurs: statut += " (EXT)"
                    
                    f.write(f"    {cli.nom:<15} | {immat:<12} | {statut:<15} | {cli.service_demande}\n")
            f.write("\n")

            f.write("[3] HISTORIQUE DES TRANSACTIONS (ARCHIVES)\n")
            if not parking.archives:
                f.write("    (Aucune transaction enregistrée)\n")
            else:
                f.write(f"    {'CLIENT':<15} | {'SORTIE':<16} | {'PRIX':<8} | {'DURÉE'}\n")
                f.write("    " + "-"*60 + "\n")
                for arch in parking.archives:
                    prix = arch.get('prix', 0.0)
                    duree = arch.get('duree', '-')
                    f.write(f"    {arch['client']:<15} | {arch['sortie']:<16} | {prix:5.2f} € | {duree}\n")
            
            f.write("\n==================================================\n")
            f.write("FIN DU RAPPORT\n")
            
        return full_path

    @staticmethod
    def generer_rapport(parking):
        """ Produit un tableau de bord HTML complet avec graphiques CSS et l'ouvre automatiquement dans le navigateur. """
        nb_total = len(parking.mesPlaces)
        nb_occupes = len(parking.clients)
        taux = (nb_occupes / nb_total * 100) if nb_total > 0 else 0
        ca_total = parking.chiffre_affaires

        style_css = """
            :root { 
                --bg: #1a1a1a; 
                --card-bg: #2C3E50; 
                --text-main: #ECF0F1; 
                --text-muted: #BDC3C7; 
                --accent: #3498DB; 
                --success: #27AE60;
                --danger: #C0392B;
                --warning: #F39C12;
            }
            
            body { font-family: 'Segoe UI', Roboto, Helvetica, sans-serif; background-color: var(--bg); color: var(--text-main); margin: 0; padding: 40px; }
            
            .header { display: flex; justify-content: space-between; align-items: flex-end; border-bottom: 2px solid var(--accent); padding-bottom: 20px; margin-bottom: 40px; }
            .logo { font-size: 32px; font-weight: 800; color: white; letter-spacing: 1px; }
            .logo span { color: var(--accent); }
            .date { color: var(--text-muted); font-size: 14px; }

            .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 40px; }
            .card { background: var(--card-bg); padding: 25px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.3); border-top: 4px solid var(--accent); }
            .card h3 { margin: 0; font-size: 12px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px; }
            .card p { margin: 15px 0 0; font-size: 32px; font-weight: bold; color: white; }
            .money { color: var(--success) !important; }

            .progress-container { background: var(--card-bg); padding: 20px; border-radius: 10px; margin-bottom: 40px; }
            .bar-bg { background: #1a252f; height: 24px; border-radius: 12px; overflow: hidden; margin-top: 10px; }
            .bar-fill { background: linear-gradient(90deg, #3498DB, #2980b9); height: 100%; transition: width 1s ease-in-out; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: bold; text-shadow: 0 1px 2px rgba(0,0,0,0.5); }

            h2 { color: white; margin-top: 50px; border-left: 5px solid var(--warning); padding-left: 15px; font-size: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; background: var(--card-bg); border-radius: 10px; overflow: hidden; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }
            th { background: #34495E; color: var(--text-muted); padding: 18px; text-align: left; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; }
            td { padding: 18px; border-bottom: 1px solid #3d566e; color: white; font-size: 14px; }
            tr:last-child td { border-bottom: none; }
            tr:hover { background: rgba(255,255,255,0.03); }
            
            .badge { padding: 6px 12px; border-radius: 4px; font-size: 11px; font-weight: bold; color: white; text-transform: uppercase; }
            .b-abo { background: var(--warning); }
            .b-pack { background: #8e44ad; }
            .b-std { background: #34495E; color: #BDC3C7; }
            .b-ext { background: var(--danger); }
            
            .footer { margin-top: 60px; text-align: center; color: var(--text-muted); font-size: 12px; border-top: 1px solid #333; padding-top: 20px; }
            .footer strong { color: var(--accent); }
        """

        html_content = f"""
        <!DOCTYPE html>
        <html lang="fr">
        <head>
            <meta charset="UTF-8">
            <title>Rapport - DreamPark Control Center</title>
            <style>
                {style_css}
                .bar-fill {{ width: {taux}%; }} 
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">DREAM<span>PARK</span> DASHBOARD</div>
                <div class="date">Généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')}</div>
            </div>

            <div class="grid">
                <div class="card">
                    <h3>Chiffre d'Affaires</h3>
                    <p class="money">{ca_total:.2f} €</p>
                </div>
                <div class="card">
                    <h3>Taux d'Occupation</h3>
                    <p>{int(taux)} %</p>
                </div>
                <div class="card">
                    <h3>Véhicules Présents</h3>
                    <p>{nb_occupes}</p>
                </div>
                <div class="card">
                    <h3>Total Sorties</h3>
                    <p>{len(parking.archives)}</p>
                </div>
            </div>

            <div class="progress-container">
                <div style="display:flex; justify-content:space-between; color:var(--text-muted); margin-bottom:5px; font-size:13px;">
                    <span>Occupation du Parking</span>
                    <span>{nb_occupes} / {nb_total} places</span>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill">{int(taux)}%</div>
                </div>
            </div>

            <h2>VÉHICULES SUR SITE</h2>
            <table>
                <thead>
                    <tr>
                        <th>Client</th>
                        <th>Immatriculation</th>
                        <th>Emplacement</th>
                        <th>Statut / Offre</th>
                        <th>Service Actif</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        if not parking.clients:
            html_content += "<tr><td colspan='5' style='text-align:center; padding:30px; color:#7f8c8d;'>Aucun véhicule présent.</td></tr>"
        
        for cli in parking.clients:
            v = cli.ma_voiture
            immat = v.immatriculation if v else "N/A"
            badge = '<span class="badge b-std">STANDARD</span>'
            if cli.pack_garantie: badge = '<span class="badge b-pack">PACK GARANTIE</span>'
            elif cli.est_abonne: badge = '<span class="badge b-abo">ABONNÉ</span>'
            
            place_txt = "Zone Interne"
            if v and v.est_aguerir_ailleurs: place_txt = '<span class="badge b-ext">EXTERNE</span>'

            html_content += f"""
                <tr>
                    <td style="font-weight:bold;">{cli.nom}</td>
                    <td style="font-family:monospace; font-size:1.1em;">{immat}</td>
                    <td>{place_txt}</td>
                    <td>{badge}</td>
                    <td>{cli.service_demande}</td>
                </tr>
            """

        html_content += """
                </tbody>
            </table>

            <h2>HISTORIQUE DES TRANSACTIONS</h2>
            <table>
                <thead>
                    <tr>
                        <th>Client</th>
                        <th>Sortie le</th>
                        <th>Durée</th>
                        <th>Type Client</th>
                        <th>Montant Final</th>
                    </tr>
                </thead>
                <tbody>
        """
        
        if not parking.archives:
            html_content += "<tr><td colspan='5' style='text-align:center; padding:30px; color:#7f8c8d;'>Aucune archive disponible.</td></tr>"

        for arch in parking.archives:
            duree = arch.get('duree', '-')
            prix = arch.get('prix', 0.0)
            s = arch.get('statut', '')
            b_cls = "b-std"
            if "Pack" in s: b_cls = "b-pack"
            elif "Abonné" in s: b_cls = "b-abo"

            html_content += f"""
                <tr>
                    <td>{arch['client']}</td>
                    <td>{arch['sortie']}</td>
                    <td>{duree}</td>
                    <td><span class="badge {b_cls}">{s}</span></td>
                    <td class="money" style="font-weight:bold; font-family:monospace; font-size:1.1em;">{prix:.2f} €</td>
                </tr>
            """

        html_content += """
                </tbody>
            </table>
            
            <div class="footer">
                Application créer par <strong>Alaeddine et Karim</strong> - MIASHS - PROJET PYTHON 2025
            </div>
        </body>
        </html>
        """

        filename = "Rapport_DreamPark.html"
        full_path = os.path.join(os.getcwd(), filename)
        
        with open(full_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        webbrowser.open('file://' + full_path)
        return full_path