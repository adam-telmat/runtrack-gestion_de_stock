# Application de Gestion de Stock

Cette application permet de gérer le stock d'un magasin avec une interface graphique. Elle utilise Python avec Tkinter pour l'interface et MySQL pour la base de données.

## Prérequis

- Python 3.x
- MySQL Server
- Bibliothèques Python requises :
  - tkinter (généralement inclus avec Python)
  - mysql-connector-python

## Installation des dépendances

```bash
pip install mysql-connector-python
```

## Configuration de la base de données

1. Assurez-vous que MySQL Server est installé et en cours d'exécution sur votre machine.
2. Exécutez le script SQL `job01.sql` pour créer la base de données et les tables nécessaires :

```bash
mysql -u root -p < job01.sql
```

3. Modifiez les informations de connexion dans les fichiers `job01.py` et `setup.py` pour utiliser votre mot de passe MySQL :

```python
self.connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="votre_mot_de_passe",  # Modifiez cette ligne avec votre mot de passe
    database="store"
)
```

## Exécution de l'application

Pour lancer l'application, exécutez :

```bash
python job01.py
```

## Fonctionnalités

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

## Utilisation

### Onglet "Gestion des produits"

1. **Ajouter un produit** : Remplissez les champs du formulaire et cliquez sur "Ajouter"
2. **Modifier un produit** : Sélectionnez un produit dans la liste, modifiez les champs et cliquez sur "Mettre à jour"
3. **Supprimer un produit** : Sélectionnez un produit dans la liste et cliquez sur "Supprimer"
4. **Effacer le formulaire** : Cliquez sur "Effacer" pour réinitialiser tous les champs
5. **Filtrer par catégorie** : Sélectionnez une catégorie dans le menu déroulant et cliquez sur "Appliquer"
6. **Réinitialiser le filtre** : Cliquez sur "Réinitialiser" pour afficher tous les produits
7. **Exporter en CSV** : Cliquez sur "Exporter en CSV" pour enregistrer les données affichées dans un fichier CSV

### Onglet "Statistiques"

Cet onglet affiche deux graphiques :
1. **Nombre de produits par catégorie** : Montre le nombre de produits dans chaque catégorie
2. **Valeur du stock par catégorie** : Montre la valeur totale (prix × quantité) des produits dans chaque catégorie

Pour rafraîchir les graphiques après des modifications, cliquez sur "Rafraîchir les graphiques".

## Résolution des problèmes de connexion

Si vous rencontrez des erreurs lors de la connexion à la base de données, voici quelques solutions :

### 1. Utiliser le script d'installation

Un script d'installation a été créé pour faciliter la configuration. Exécutez :

```bash
python setup.py
```

Ce script va :
- Vérifier la version de Python
- Installer les dépendances nécessaires
- Tester la connexion à MySQL
- Configurer la base de données

### 2. Vérifier que MySQL est démarré

Sur Windows :
1. Ouvrez le Gestionnaire des services (services.msc)
2. Recherchez "MySQL" dans la liste
3. Vérifiez que le service est démarré, sinon démarrez-le

Sur Linux :
```bash
sudo systemctl status mysql
# Si arrêté, démarrez-le avec :
sudo systemctl start mysql
```

### 3. Vérifier les informations de connexion

Si vous utilisez un mot de passe pour votre utilisateur MySQL, modifiez-le dans les fichiers :
- `job01.py`
- `setup.py`

### 4. Installer manuellement les dépendances

```bash
pip install mysql-connector-python
```

### 5. Créer manuellement la base de données

Si l'application ne peut pas créer automatiquement la base de données, vous pouvez l'exécuter manuellement :

```bash
mysql -u root -p < job01.sql
```

## Dépannage

| Erreur | Solution |
|--------|----------|
| "Unknown database 'store'" | La base de données n'existe pas. Exécutez `setup.py` ou le script SQL manuellement. |
| "Access denied for user..." | Vérifiez les informations de connexion (utilisateur/mot de passe). |
| "Can't connect to MySQL server..." | Vérifiez que le serveur MySQL est démarré. |
| "No module named 'mysql'" | Installez mysql-connector-python avec pip. |

## Dépendances supplémentaires

Pour les nouvelles fonctionnalités, vous aurez besoin d'installer matplotlib :

```bash
pip install matplotlib
``` 