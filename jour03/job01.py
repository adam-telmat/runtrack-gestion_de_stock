import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import mysql.connector
from mysql.connector import Error
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class StoreManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestion de Stock")
        self.root.geometry("1200x700")
        self.root.resizable(True, True)
        
        # Variables pour les champs de saisie
        self.product_id = tk.StringVar()
        self.product_name = tk.StringVar()
        self.product_description = tk.StringVar()
        self.product_price = tk.StringVar()
        self.product_quantity = tk.StringVar()
        self.product_category = tk.StringVar()
        
        # Variable pour le filtre de catégorie
        self.filter_category = tk.StringVar()
        
        # Connexion à la base de données
        self.connection = None
        self.connect_to_database()
        
        # Création de l'interface
        self.create_widgets()
        
        # Chargement initial des produits
        self.load_products()
        self.load_categories()
        
        # Mise à jour du graphique
        self.update_chart()
    
    def connect_to_database(self):
        try:
            # Première tentative de connexion à la base de données "store"
            self.connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="pixel8pro",  # Mot de passe mis à jour
                database="store"
            )
            print("Connexion à la base de données réussie")
        except Error as e:
            # Si la base de données n'existe pas, essayons de la créer
            if "Unknown database" in str(e):
                try:
                    # Connexion sans spécifier de base de données
                    temp_connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="pixel8pro"  # Mot de passe mis à jour
                    )
                    
                    # Création de la base de données et des tables
                    cursor = temp_connection.cursor()
                    
                    # Exécution du script SQL
                    with open('jour03/job01.sql', 'r') as sql_file:
                        sql_script = sql_file.read()
                        # Exécuter chaque commande séparément
                        for command in sql_script.split(';'):
                            if command.strip():
                                cursor.execute(command)
                    
                    temp_connection.commit()
                    cursor.close()
                    temp_connection.close()
                    
                    # Nouvelle tentative de connexion à la base de données créée
                    self.connection = mysql.connector.connect(
                        host="localhost",
                        user="root",
                        password="pixel8pro",  # Mot de passe mis à jour
                        database="store"
                    )
                    messagebox.showinfo("Succès", "Base de données créée et initialisée avec succès")
                    print("Base de données créée et connexion réussie")
                except Error as create_error:
                    error_message = f"Erreur lors de la création de la base de données: {create_error}\n\n"
                    error_message += "Vérifiez que:\n"
                    error_message += "1. Le serveur MySQL est démarré\n"
                    error_message += "2. Les informations de connexion sont correctes\n"
                    error_message += "3. Vous avez les droits nécessaires pour créer une base de données"
                    messagebox.showerror("Erreur de connexion", error_message)
                    print(f"Erreur lors de la création de la base de données: {create_error}")
            else:
                error_message = f"Erreur lors de la connexion à la base de données: {e}\n\n"
                error_message += "Vérifiez que:\n"
                error_message += "1. Le serveur MySQL est démarré\n"
                error_message += "2. Les informations de connexion sont correctes\n"
                error_message += "3. La base de données 'store' existe"
                messagebox.showerror("Erreur de connexion", error_message)
                print(f"Erreur de connexion: {e}")
    
    def create_widgets(self):
        # Création d'un notebook (onglets)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Onglet de gestion des produits
        products_tab = ttk.Frame(notebook)
        notebook.add(products_tab, text="Gestion des produits")
        
        # Onglet des statistiques
        stats_tab = ttk.Frame(notebook)
        notebook.add(stats_tab, text="Statistiques")
        
        # Configuration de l'onglet des produits
        self.setup_products_tab(products_tab)
        
        # Configuration de l'onglet des statistiques
        self.setup_stats_tab(stats_tab)
    
    def setup_products_tab(self, parent):
        # Frame principale
        main_frame = ttk.Frame(parent, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Frame pour les contrôles (formulaire)
        control_frame = ttk.LabelFrame(main_frame, text="Détails du produit", padding="10")
        control_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Champs du formulaire
        ttk.Label(control_frame, text="ID:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(control_frame, textvariable=self.product_id, state="readonly").grid(row=0, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Nom:").grid(row=0, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(control_frame, textvariable=self.product_name, width=30).grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Prix:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(control_frame, textvariable=self.product_price).grid(row=1, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Quantité:").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        ttk.Entry(control_frame, textvariable=self.product_quantity).grid(row=1, column=3, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Catégorie:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.category_combobox = ttk.Combobox(control_frame, textvariable=self.product_category)
        self.category_combobox.grid(row=2, column=1, padx=5, pady=5)
        
        ttk.Label(control_frame, text="Description:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.description_text = tk.Text(control_frame, height=3, width=50)
        self.description_text.grid(row=3, column=1, columnspan=3, padx=5, pady=5, sticky=tk.W+tk.E)
        
        # Frame pour les boutons
        button_frame = ttk.Frame(control_frame)
        button_frame.grid(row=4, column=0, columnspan=4, pady=10)
        
        ttk.Button(button_frame, text="Ajouter", command=self.add_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Mettre à jour", command=self.update_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Supprimer", command=self.delete_product).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Effacer", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        
        # Frame pour le filtre et l'exportation
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Label(filter_frame, text="Filtrer par catégorie:").pack(side=tk.LEFT, padx=5)
        self.filter_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_category, width=20)
        self.filter_combobox.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Appliquer", command=self.apply_filter).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Réinitialiser", command=self.reset_filter).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Exporter en CSV", command=self.export_to_csv).pack(side=tk.RIGHT, padx=5)
        
        # Frame pour le tableau des produits
        table_frame = ttk.LabelFrame(main_frame, text="Liste des produits", padding="10")
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Tableau des produits
        columns = ("id", "name", "description", "price", "quantity", "category")
        self.product_tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        # Définition des en-têtes
        self.product_tree.heading("id", text="ID")
        self.product_tree.heading("name", text="Nom")
        self.product_tree.heading("description", text="Description")
        self.product_tree.heading("price", text="Prix")
        self.product_tree.heading("quantity", text="Quantité")
        self.product_tree.heading("category", text="Catégorie")
        
        # Définition des largeurs de colonnes
        self.product_tree.column("id", width=50)
        self.product_tree.column("name", width=150)
        self.product_tree.column("description", width=300)
        self.product_tree.column("price", width=100)
        self.product_tree.column("quantity", width=100)
        self.product_tree.column("category", width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.product_tree.yview)
        self.product_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.product_tree.pack(fill=tk.BOTH, expand=True)
        
        # Événement de sélection
        self.product_tree.bind("<<TreeviewSelect>>", self.item_selected)
    
    def setup_stats_tab(self, parent):
        # Frame pour les graphiques
        chart_frame = ttk.Frame(parent, padding="10")
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Création de deux sous-frames pour les graphiques
        left_chart_frame = ttk.LabelFrame(chart_frame, text="Produits par catégorie", padding="10")
        left_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        right_chart_frame = ttk.LabelFrame(chart_frame, text="Valeur du stock par catégorie", padding="10")
        right_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Création des figures pour les graphiques
        self.fig1 = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax1 = self.fig1.add_subplot(111)
        
        self.fig2 = plt.Figure(figsize=(5, 4), dpi=100)
        self.ax2 = self.fig2.add_subplot(111)
        
        # Création des canvas pour afficher les graphiques
        self.canvas1 = FigureCanvasTkAgg(self.fig1, left_chart_frame)
        self.canvas1.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.canvas2 = FigureCanvasTkAgg(self.fig2, right_chart_frame)
        self.canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Bouton pour rafraîchir les graphiques
        ttk.Button(chart_frame, text="Rafraîchir les graphiques", command=self.update_chart).pack(pady=10)
    
    def update_chart(self):
        try:
            cursor = self.connection.cursor()
            
            # Requête pour obtenir le nombre de produits par catégorie
            query1 = """
            SELECT c.name, COUNT(p.id) 
            FROM category c
            LEFT JOIN product p ON c.id = p.id_category
            GROUP BY c.name
            """
            cursor.execute(query1)
            category_counts = cursor.fetchall()
            
            # Requête pour obtenir la valeur du stock par catégorie (prix * quantité)
            query2 = """
            SELECT c.name, SUM(p.price * p.quantity) 
            FROM category c
            LEFT JOIN product p ON c.id = p.id_category
            GROUP BY c.name
            """
            cursor.execute(query2)
            category_values = cursor.fetchall()
            
            cursor.close()
            
            # Préparation des données pour les graphiques
            categories1 = [item[0] for item in category_counts]
            counts = [item[1] for item in category_counts]
            
            categories2 = [item[0] for item in category_values]
            values = [item[1] if item[1] is not None else 0 for item in category_values]
            
            # Effacer les graphiques précédents
            self.ax1.clear()
            self.ax2.clear()
            
            # Création du graphique à barres pour le nombre de produits
            bars1 = self.ax1.bar(categories1, counts, color='skyblue')
            self.ax1.set_xlabel('Catégorie')
            self.ax1.set_ylabel('Nombre de produits')
            self.ax1.set_title('Nombre de produits par catégorie')
            
            # Ajout des valeurs au-dessus des barres
            for bar in bars1:
                height = bar.get_height()
                self.ax1.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}', ha='center', va='bottom')
            
            # Rotation des étiquettes pour une meilleure lisibilité
            self.ax1.set_xticklabels(categories1, rotation=45, ha='right')
            
            # Création du graphique à barres pour la valeur du stock
            bars2 = self.ax2.bar(categories2, values, color='lightgreen')
            self.ax2.set_xlabel('Catégorie')
            self.ax2.set_ylabel('Valeur du stock (€)')
            self.ax2.set_title('Valeur du stock par catégorie')
            
            # Ajout des valeurs au-dessus des barres
            for bar in bars2:
                height = bar.get_height()
                self.ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(height)}€', ha='center', va='bottom')
            
            # Rotation des étiquettes pour une meilleure lisibilité
            self.ax2.set_xticklabels(categories2, rotation=45, ha='right')
            
            # Ajustement des graphiques
            self.fig1.tight_layout()
            self.fig2.tight_layout()
            
            # Mise à jour des canvas
            self.canvas1.draw()
            self.canvas2.draw()
            
        except Error as e:
            messagebox.showerror("Erreur de base de données", f"Erreur lors de la mise à jour des graphiques: {e}")
    
    def load_products(self, category_filter=None):
        # Effacer les données existantes
        for item in self.product_tree.get_children():
            self.product_tree.delete(item)
        
        try:
            cursor = self.connection.cursor()
            
            if category_filter:
                query = """
                SELECT p.id, p.name, p.description, p.price, p.quantity, c.name 
                FROM product p 
                LEFT JOIN category c ON p.id_category = c.id
                WHERE c.name = %s
                """
                cursor.execute(query, (category_filter,))
            else:
                query = """
                SELECT p.id, p.name, p.description, p.price, p.quantity, c.name 
                FROM product p 
                LEFT JOIN category c ON p.id_category = c.id
                """
                cursor.execute(query)
                
            products = cursor.fetchall()
            
            for product in products:
                self.product_tree.insert("", tk.END, values=product)
            
            cursor.close()
        except Error as e:
            messagebox.showerror("Erreur de base de données", f"Erreur lors du chargement des produits: {e}")
    
    def load_categories(self):
        try:
            cursor = self.connection.cursor()
            query = "SELECT id, name FROM category"
            cursor.execute(query)
            categories = cursor.fetchall()
            
            # Dictionnaire pour stocker les catégories (id: name)
            self.categories_dict = {category[0]: category[1] for category in categories}
            
            # Mise à jour des combobox
            category_names = list(self.categories_dict.values())
            self.category_combobox['values'] = category_names
            
            # Mise à jour du combobox de filtre avec une option "Toutes" en plus
            filter_values = ["Toutes"] + category_names
            self.filter_combobox['values'] = filter_values
            self.filter_category.set("Toutes")
            
            cursor.close()
        except Error as e:
            messagebox.showerror("Erreur de base de données", f"Erreur lors du chargement des catégories: {e}")
    
    def apply_filter(self):
        category = self.filter_category.get()
        if category == "Toutes":
            self.load_products()
        else:
            self.load_products(category)
    
    def reset_filter(self):
        self.filter_category.set("Toutes")
        self.load_products()
    
    def export_to_csv(self):
        try:
            # Demander à l'utilisateur où enregistrer le fichier
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                title="Enregistrer le fichier CSV"
            )
            
            if not file_path:  # Si l'utilisateur annule
                return
            
            cursor = self.connection.cursor()
            
            # Récupérer les données en fonction du filtre actuel
            category_filter = self.filter_category.get()
            if category_filter == "Toutes":
                query = """
                SELECT p.id, p.name, p.description, p.price, p.quantity, c.name 
                FROM product p 
                LEFT JOIN category c ON p.id_category = c.id
                """
                cursor.execute(query)
            else:
                query = """
                SELECT p.id, p.name, p.description, p.price, p.quantity, c.name 
                FROM product p 
                LEFT JOIN category c ON p.id_category = c.id
                WHERE c.name = %s
                """
                cursor.execute(query, (category_filter,))
            
            products = cursor.fetchall()
            cursor.close()
            
            # Écrire dans le fichier CSV
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                # Écrire l'en-tête
                csv_writer.writerow(['ID', 'Nom', 'Description', 'Prix', 'Quantité', 'Catégorie'])
                
                # Écrire les données
                for product in products:
                    csv_writer.writerow(product)
            
            messagebox.showinfo("Succès", f"Les données ont été exportées avec succès vers {file_path}")
            
        except Error as e:
            messagebox.showerror("Erreur de base de données", f"Erreur lors de l'exportation des données: {e}")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exportation des données: {e}")
    
    def get_category_id(self, category_name):
        for id, name in self.categories_dict.items():
            if name == category_name:
                return id
        return None
    
    def item_selected(self, event):
        selected_item = self.product_tree.selection()[0]
        values = self.product_tree.item(selected_item, 'values')
        
        # Mise à jour des variables
        self.product_id.set(values[0])
        self.product_name.set(values[1])
        self.description_text.delete(1.0, tk.END)
        self.description_text.insert(tk.END, values[2])
        self.product_price.set(values[3])
        self.product_quantity.set(values[4])
        self.product_category.set(values[5])
    
    def clear_form(self):
        self.product_id.set("")
        self.product_name.set("")
        self.description_text.delete(1.0, tk.END)
        self.product_price.set("")
        self.product_quantity.set("")
        self.product_category.set("")
    
    def add_product(self):
        name = self.product_name.get()
        description = self.description_text.get(1.0, tk.END).strip()
        price = self.product_price.get()
        quantity = self.product_quantity.get()
        category_name = self.product_category.get()
        
        # Validation
        if not name or not price or not quantity or not category_name:
            messagebox.showerror("Erreur de validation", "Tous les champs sont obligatoires")
            return
        
        try:
            price = int(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Erreur de validation", "Le prix et la quantité doivent être des nombres entiers")
            return
        
        category_id = self.get_category_id(category_name)
        if not category_id:
            messagebox.showerror("Erreur de validation", "Catégorie invalide")
            return
        
        try:
            cursor = self.connection.cursor()
            query = """
            INSERT INTO product (name, description, price, quantity, id_category)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (name, description, price, quantity, category_id))
            self.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Succès", "Produit ajouté avec succès")
            self.clear_form()
            self.load_products()
            self.update_chart()
        except Error as e:
            messagebox.showerror("Erreur de base de données", f"Erreur lors de l'ajout du produit: {e}")
    
    def update_product(self):
        product_id = self.product_id.get()
        if not product_id:
            messagebox.showerror("Erreur de validation", "Veuillez sélectionner un produit à mettre à jour")
            return
        
        name = self.product_name.get()
        description = self.description_text.get(1.0, tk.END).strip()
        price = self.product_price.get()
        quantity = self.product_quantity.get()
        category_name = self.product_category.get()
        
        # Validation
        if not name or not price or not quantity or not category_name:
            messagebox.showerror("Erreur de validation", "Tous les champs sont obligatoires")
            return
        
        try:
            price = int(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Erreur de validation", "Le prix et la quantité doivent être des nombres entiers")
            return
        
        category_id = self.get_category_id(category_name)
        if not category_id:
            messagebox.showerror("Erreur de validation", "Catégorie invalide")
            return
        
        try:
            cursor = self.connection.cursor()
            query = """
            UPDATE product
            SET name = %s, description = %s, price = %s, quantity = %s, id_category = %s
            WHERE id = %s
            """
            cursor.execute(query, (name, description, price, quantity, category_id, product_id))
            self.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Succès", "Produit mis à jour avec succès")
            self.clear_form()
            self.load_products()
            self.update_chart()
        except Error as e:
            messagebox.showerror("Erreur de base de données", f"Erreur lors de la mise à jour du produit: {e}")
    
    def delete_product(self):
        product_id = self.product_id.get()
        if not product_id:
            messagebox.showerror("Erreur de validation", "Veuillez sélectionner un produit à supprimer")
            return
        
        confirm = messagebox.askyesno("Confirmation", "Êtes-vous sûr de vouloir supprimer ce produit?")
        if not confirm:
            return
        
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM product WHERE id = %s"
            cursor.execute(query, (product_id,))
            self.connection.commit()
            cursor.close()
            
            messagebox.showinfo("Succès", "Produit supprimé avec succès")
            self.clear_form()
            self.load_products()
            self.update_chart()
        except Error as e:
            messagebox.showerror("Erreur de base de données", f"Erreur lors de la suppression du produit: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = StoreManagementApp(root)
    root.mainloop()
