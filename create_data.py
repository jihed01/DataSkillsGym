import io
import duckdb
import pandas as pd
import random
from datetime import datetime, timedelta

def initialize_database():
    # Connexion à la base de données
    con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)

    # Création des schémas par catégorie
    con.execute("CREATE SCHEMA IF NOT EXISTS joins")
    con.execute("CREATE SCHEMA IF NOT EXISTS aggregations")
    con.execute("CREATE SCHEMA IF NOT EXISTS window_funcs")

    # Catégorie JOINS
    _create_join_tables(con)

    # # Catégorie AGGREGATIONS
    # _create_aggregation_tables(con)
    #
    # Catégorie WINDOW FUNCTIONS
    _create_window_function_tables(con)

    con.close()


def _create_join_tables(con):
    """Crée les tables pour les exercices JOINS"""
    # Exo 1 - CROSS JOIN
    beverages = pd.DataFrame({
        'beverage': ['orange juice', 'Expresso', 'Tea'],
        'price': [2.5, 2, 3]
    })
    con.execute("CREATE TABLE IF NOT EXISTS joins.exo1_table1 AS SELECT * FROM beverages")

    food_items = pd.DataFrame({
        'food_item': ['cookie juice', 'chocolatine', 'muffin'],
        'food_price': [2.5, 2, 3]
    })
    con.execute("CREATE TABLE IF NOT EXISTS joins.exo1_table2 AS SELECT * FROM food_items")

    # Exo 2 - INNER JOIN
    # Génération des données
    univers = ["Électronique", "Mode", "Maison"]
    categories_par_univers = {
        "Électronique": ["Téléphones", "Ordinateurs"],
        "Mode": ["Vêtements", "Accessoires"],
        "Maison": ["Meubles", "Décoration"]
    }
    noms_produits = {
        "Téléphones": ["iPhone 13", "Samsung Galaxy S21", "Google Pixel 6", "OnePlus 9", "Xiaomi Mi 11"],
        "Ordinateurs": ["MacBook Pro", "Dell XPS 15", "HP Spectre x360", "Lenovo ThinkPad", "Asus ROG Zephyrus"],
        "Vêtements": ["Chemise en lin", "Robe d'été", "Jeans slim", "Veste en cuir", "Pull en laine"],
        "Accessoires": ["Montre élégante", "Sac à dos moderne", "Lunettes de soleil", "Ceinture en cuir",
                        "Écharpe en soie"],
        "Meubles": ["Canapé modulaire", "Table à manger en bois", "Lit king-size", "Chaise ergonomique",
                    "Bureau en verre"],
        "Décoration": ["Vase en céramique", "Tableau abstrait", "Bougie parfumée", "Coussins décoratifs",
                       "Horloge murale"]
    }

    # Création des DataFrames
    donnees = []
    produit_id_counter = 1
    categorie_id = 0

    for univers_id, univers_name in enumerate(univers):
        for categorie in categories_par_univers[univers_name]:
            categorie_id += 1
            for _ in range(5):  # 5 produits par catégorie pour simplifier
                produit = {
                    "produit_id": produit_id_counter,
                    "univers_id": univers_id,
                    "univers_name": univers_name,
                    "categorie_name": categorie,
                    "categorie_id": categorie_id,
                    "nom": random.choice(noms_produits[categorie]),
                    "prix_unitaire": round(random.uniform(10, 1000), 2)
                }
                donnees.append(produit)
                produit_id_counter += 1

    df = pd.DataFrame(donnees)
    products = df[["produit_id", "prix_unitaire", "nom"]]
    categories = df[["categorie_id", "categorie_name", "univers_name"]].drop_duplicates()

    # Création des tables dans DuckDB
    con.execute("CREATE TABLE IF NOT EXISTS joins.exo2_table1 AS SELECT * FROM products")
    con.execute("CREATE TABLE IF NOT EXISTS joins.exo2_table2 AS SELECT * FROM categories")

    # Ajout de quelques exemples de ventes pour un exercice ultérieur
    ventes = []
    date_debut = datetime(2023, 7, 1)
    date_fin = datetime(2023, 7, 31)

    for _ in range(100):  # 100 ventes pour simplifier
        date_vente = date_debut + timedelta(days=random.randint(0, 30))
        product = products.sample(1).iloc[0]
        quantite_vendue = random.randint(1, 5)
        ventes.append({
            "date": date_vente,
            "produit_id": product["produit_id"],
            "quantite_vendue": quantite_vendue,
            "prix_unitaire": product["prix_unitaire"],
            "montant_total": product["prix_unitaire"] * quantite_vendue
        })

    ventes_df = pd.DataFrame(ventes)
    con.execute("CREATE TABLE IF NOT EXISTS joins.exo2_ventes AS SELECT * FROM ventes_df")

    # Exo 3 à 5
    # [...] Même structure pour les autres exercices


# def _create_aggregation_tables(con):
#     """Crée les tables pour les exercices AGGREGATIONS"""
#     # Exo 1
#
#
#     con.execute("CREATE TABLE IF NOT EXISTS aggregations.exo1_main AS SELECT * FROM ...")
#
#     # Exo 2 à 5
#     # [...] Même structure pour les autres exercices
#
#
def _create_window_function_tables(con):
    """Crée les tables pour les exercices WINDOW FUNCTIONS"""
    # Exo 1 : La clause OVER
    # Define the furniture data
    furniture_data = [
        ("Chairs", "Chair 1", 5.2),
        ("Chairs", "Chair 2", 4.5),
        ("Chairs", "Chair 3", 6.8),
        ("Sofas", "Sofa 1", 25.5),
        ("Sofas", "Sofa 2", 20.3),
        ("Sofas", "Sofa 3", 30.0),
        ("Tables", "Table 1", 15.0),
        ("Tables", "Table 2", 12.5),
        ("Tables", "Table 3", 18.2),
    ]

    # Create a pandas DataFrame from the predefined data
    furniture = pd.DataFrame(furniture_data, columns=["category", "item", "weight"])

    con.execute("CREATE TABLE IF NOT EXISTS window_funcs.exo1_data AS SELECT * FROM furniture")

    # Exo 2 à 5
    # [...] Même structure pour les autres exercices


if __name__ == "__main__":
    initialize_database()
