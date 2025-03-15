# Gestion de Stock - Projet Python/MySQL

Ce projet contient une application de gestion de stock pour un magasin, développée en Python avec une base de données MySQL.

## Structure du projet

- **jour03/** : Dossier contenant l'application de gestion de stock
  - `job01.py` : Programme principal avec interface graphique Tkinter
  - `job01.sql` : Script SQL pour créer la base de données et les tables

## Application de Gestion de Stock

Cette application permet de gérer le stock d'un magasin avec une interface graphique. Elle utilise Python avec Tkinter pour l'interface et MySQL pour la base de données.

### Fonctionnalités

L'application permet de :

1. **Gestion des produits**
   - Afficher la liste complète des produits en stock
   - Ajouter un nouveau produit
   - Modifier un produit existant (nom, description, prix, quantité, catégorie)
   - Supprimer un produit
   - Filtrer les produits par catégorie
   - Exporter les produits en format CSV

2. **Visualisation des données**
   - Afficher des graphiques sur le nombre de produits par catégorie
   - Afficher des graphiques sur la valeur du stock par catégorie

### Prérequis

- Python 3.x
- MySQL Server
- Bibliothèques Python requises :
  - tkinter (généralement inclus avec Python)
  - mysql-connector-python
  - matplotlib

### Installation

```bash
# Installation des dépendances
pip install mysql-connector-python matplotlib

# Configuration de la base de données
mysql -u root -p < jour03/job01.sql
```

### Exécution

```bash
# Lancer l'application
python jour03/job01.py
```

### Configuration de la base de données

Avant de lancer l'application, assurez-vous de modifier les informations de connexion à la base de données dans le fichier `jour03/job01.py` :

```python
self.connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="votre_mot_de_passe",  # Modifiez cette ligne avec votre mot de passe
    database="store"
)
```

## Captures d'écran

![Gestion des produits](screenshots/products.png)
![Statistiques](screenshots/stats.png)

## Auteur

[Votre nom]