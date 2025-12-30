# DreamPark Manager – Gestion de Parking

Auteurs : Alaeddine & Karim  
Université : Université Toulouse 2 – Jean Jaurès  
Module : MI0C501T - Aspects statiques et dynamiques des langages – L3 MIASHS (2025)

---

## 1. Contexte du projet

Ce projet a été réalisé dans le cadre du module de Programmation Python en Licence 3 MIASHS.  
L’objectif était de concevoir une application simulant le fonctionnement d’un parking automatisé, en intégrant une logique métier complète, une interface graphique, la persistance des données et des tests unitaires.

Le projet DreamPark Manager vise à reproduire le fonctionnement réel d’un parking moderne, incluant les équipements matériels, les règles de gestion et le suivi de l’activité.

---

## 2. Fonctionnalités principales

### Côté interface (Gestion du parking)
- Tableau de bord affichant l’occupation du parking par niveau.
- Affichage des événements en temps réel (logs console).
- Actions manuelles (forcer une sortie, interaction service client).
- Génération de rapports d’activité et financiers (HTML et texte).

### Côté logique métier (Simulation)
- Attribution automatique des places selon les dimensions des véhicules.
- Contrôle du gabarit à l’entrée (refus si véhicule trop grand).
- Gestion des abonnements et du Pack Garantie (stockage externe).
- Tarification dynamique selon le statut du client et la durée.
- Archivage des transactions.

---

## 3. Architecture du projet

Le projet est structuré selon le patron *Modèle – Vue – Contrôleur (MVC)* afin de séparer les responsabilités et améliorer la lisibilité.

- *Modèle* : Contient la logique métier et les données (parking, places, véhicules, calculs).
- *Vue* : Interface graphique développée avec CustomTkinter (affichage et interactions).
- *Contrôleur* : Assure la coordination entre l’interface et la logique métier.

> Remarque technique : La classe BorneTicket est considérée comme un composant matériel simulé. Elle intègre donc sa propre logique d’interaction pour reproduire le comportement d’une borne réelle autonome.

---

## 4. Organisation des dossiers

Nous avons structuré le projet en modules distincts afin de respecter l’architecture MVC et de faciliter la maintenance.  
Voici le détail complet de chaque fichier présent dans l’application.

### 4.1. Le code source (src/)

Le dossier src/ constitue le cœur du programme. Il est divisé en plusieurs sous-catégories logiques.

#### A. Les modèles (src/models/)

Ce dossier contient toute la logique métier et la définition des objets du parking.

- acces.py : gère les barrières d’entrée et de sortie ainsi que les procédures d’accueil  
- borne_ticket.py : simule le comportement matériel de la borne (questions au client, impression du ticket)  
- camera.py : simule la lecture automatique des plaques d’immatriculation  
- client.py : définit les attributs d’un conducteur (nom, statut abonné, véhicule associé)  
- panneau_affichage.py : gère les messages informatifs affichés aux conducteurs (ex. : « COMPLET »)  
- parking.py : classe principale contenant la liste des places et des clients  
- place.py : définit une place de stationnement (numéro, niveau, dimensions, état libre/occupé)  
- placement.py : représente le ticket ou la transaction (heure de début, heure de fin)  
- teleporteur.py : mécanisme simulant le déplacement physique du véhicule vers sa place  
- voiture.py : définit les caractéristiques physiques du véhicule (immatriculation, hauteur, longueur)

#### B. Le contrôleur (src/controllers/)

- parking_controller.py : chef d’orchestre de l’application. Il reçoit les actions de l’interface graphique (clics) et ordonne aux modèles d’effectuer les traitements nécessaires.

#### C. La vue (src/views/)

- interface.py : contient l’ensemble du code de l’interface graphique CustomTkinter (fenêtres, boutons, tableau de bord).

#### D. Les utilitaires (src/utils/)

- generateur_html.py : module dédié à la création et à la mise en forme du rapport financier au format HTML.

#### E. À la racine du dossier source

- main.py : point d’entrée unique pour lancer l’application  
- logo_parking.ico : icône de l’application utilisée par l’interface graphique

---

### 4.2. Les tests unitaires (tests/)

Chaque module métier possède son propre fichier de test afin de garantir la fiabilité du code.  
Des mocks sont utilisés pour simuler l’interface graphique.

- test_acces.py : vérifie les scénarios d’entrée et de sortie  
- test_borne_ticket.py : teste la génération des tickets  
- test_camera.py : teste la détection des plaques  
- test_client.py : vérifie la création des profils clients  
- test_generateur_html.py : vérifie que le rapport se génère sans erreur  
- test_panneau_affichage.py : vérifie les messages d’alerte  
- test_parking.py : teste la recherche de places et le comptage  
- test_parking_controller.py : teste la coordination globale  
- test_place.py : vérifie le changement d’état des places (libre/occupé)  
- test_placement.py : teste le calcul des durées  
- test_teleporteur.py : vérifie l’assignation du véhicule à une place  
- test_voiture.py : vérifie les dimensions et l’historique du véhicule

---

### 4.3. Fichiers à la racine du projet

- README.md : documentation complète du projet  
- data_parking.pkl : fichier binaire généré automatiquement pour sauvegarder l’état du parking (persistance des données)

---

## 5. Lancer l’application

### Prérequis
- Python 3.x installé
- Bibliothèque customtkinter

### Installation
Ouvrez un terminal et installez la dépendance graphique :
```bash
pip install customtkinter

```
### Exécution
Lancez le programme depuis le terminal :
```bash
python src/main.py