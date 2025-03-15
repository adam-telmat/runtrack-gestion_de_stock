-- Création de la base de données
CREATE DATABASE IF NOT EXISTS store;
USE store;

-- Création de la table category
CREATE TABLE IF NOT EXISTS category (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Création de la table product
CREATE TABLE IF NOT EXISTS product (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    price INT NOT NULL,
    quantity INT NOT NULL,
    id_category INT,
    FOREIGN KEY (id_category) REFERENCES category(id)
);

-- Insertion de catégories
INSERT INTO category (name) VALUES
    ('Électronique'),
    ('Vêtements'),
    ('Alimentation'),
    ('Maison'),
    ('Livres');

-- Insertion de produits
INSERT INTO product (name, description, price, quantity, id_category) VALUES
    ('Smartphone', 'Téléphone intelligent avec écran tactile', 599, 50, 1),
    ('Ordinateur portable', 'Ordinateur portable léger et puissant', 899, 30, 1),
    ('T-shirt', 'T-shirt en coton de haute qualité', 25, 100, 2),
    ('Jeans', 'Jeans durable et confortable', 45, 75, 2),
    ('Chocolat', 'Tablette de chocolat noir 70%', 5, 200, 3),
    ('Café', 'Café en grains premium', 12, 150, 3),
    ('Lampe de bureau', 'Lampe LED ajustable', 35, 40, 4),
    ('Coussin', 'Coussin décoratif pour canapé', 20, 60, 4),
    ('Roman', 'Roman bestseller de fiction', 18, 80, 5),
    ('Livre de cuisine', 'Recettes faciles et rapides', 22, 45, 5);
