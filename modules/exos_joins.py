import duckdb
import pandas as pd
import streamlit as st


def get_join_tables_for_exo(con, exo_name):
    """Récupère les tables avec des noms simplifiés"""
    exo_num = exo_name.split(":")[0].lower().replace("exo", "").strip()

    if exo_num == "1":
        return {
            "table1": con.execute("SELECT * FROM joins.exo1_table1").df(),
            "table2": con.execute("SELECT * FROM joins.exo1_table2").df(),
            "sql_names": {
                "table1": "exo1_table1",
                "table2": "exo1_table2"
            },
            "exo_num": exo_num,
            "display_names": {
                "table1": "beverages",
                "table2": "food_items"
            }
        }
    elif exo_num == "2":
        return {
            "table1": con.execute("SELECT * FROM joins.exo2_table1").df(),  # Produits
            "table2": con.execute("SELECT * FROM joins.exo2_table2").df(),  # Catégories
            "sql_names": {
                "table1": "exo2_table1",
                "table2": "exo2_table2"
            },
            "exo_num": exo_num,
            "display_names": {
                "table1": "products",
                "table2": "categories"
            }
        }
#-----------------------------------------------------------
#  SQL
#---------------------------------------------------------------------

def display_join_exercise_sql(con, exo_name):
    """Affiche l'exercice avec des noms simplifiés"""
    tables = get_join_tables_for_exo(con, exo_name)

    if not tables:
        st.error("Exercice non trouvé")
        return

    st.subheader(f"{exo_name} - SQL")

    # Afficher les tables avec des noms simples
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**Table: {tables['display_names']['table1']}**")
        st.dataframe(tables["table1"])
    with col2:
        st.write(f"**Table: {tables['display_names']['table2']}**")
        st.dataframe(tables["table2"])

    display_solution_zone(con, exo_name, "joins", tables)


def display_solution_zone(con, exo_name, category, tables):
    """Affiche la zone de solution complète pour un exercice"""
    st.subheader("Votre réponse SQL")
    st.info("Note: Utilisez les noms de tables simplifiés (beverages, food_items) dans votre requête")
    user_input = st.text_area(
        "Écrivez votre requête SQL ici:",
        key=f"sql_{exo_name}"
    )

    if st.button(f"Tester {exo_name}", key=f"test_{exo_name}"):
        test_sql_solution(con, user_input, exo_name, tables)

    display_solution_toggle(con, exo_name, category)


def test_sql_solution(con, user_query, exo_name, tables):
    """Valide la solution SQL de l'utilisateur"""
    try:
        # Remplacer les noms simplifiés par les vrais noms de tables
        exo_num = exo_name.split(":")[0].lower().replace("exo", "").strip()
        real_query = user_query

        if exo_num == "1":
            real_query = real_query.replace("beverages", "joins.exo1_table1")
            real_query = real_query.replace("food_items", "joins.exo1_table2")
        elif exo_num == "2":
            real_query = real_query.replace("products", "joins.exo2_table1")
            real_query = real_query.replace("categories", "joins.exo2_table2")

        # Exécuter la requête
        user_result = con.execute(real_query).df()

        # Obtenir le résultat attendu
        expected = get_expected_sql_result(con, exo_name, tables)

        # Afficher les résultats
        st.dataframe(user_result)

        # Comparer les résultats
        if user_result.equals(expected):
            st.success("✅ Correct !")
        else:
            st.warning("⚠️ Résultat incorrect")
            st.write("Attendu :")
            st.dataframe(expected)

    except Exception as e:
        st.error(f"Erreur SQL : {str(e)}")


def display_solution_toggle(con, exo_name, category):
    """Gère l'affichage/masquage de la solution"""
    session_key = f"show_{exo_name}_solution"

    if st.button("🔎 Afficher/Masquer la solution"):
        if session_key not in st.session_state:
            st.session_state[session_key] = False
        st.session_state[session_key] = not st.session_state[session_key]

    if st.session_state.get(session_key, False):
        show_solution_sql(con, exo_name, category)


def show_solution_sql(con, exo_name, category):
    """Affiche la solution complète"""
    st.subheader("Solution")

    st.code(get_sql_solution(exo_name), language="sql")

    st.markdown("**Résultat attendu**")
    st.dataframe(get_expected_sql_result(con, exo_name))


def get_sql_solution(exo_name):
    """Retourne la solution SQL formatée avec des noms simples"""
    solutions = {
        "Exo1: CROSS JOIN": "SELECT * FROM beverages CROSS JOIN food_items",
        "Exo2: INNER JOIN": """SELECT p.nom AS product_name, p.prix_unitaire AS price,
                              c.categorie_name AS category, c.univers_name AS universe
                              FROM products p
                              INNER JOIN categories c ON p.produit_id = c.categorie_id"""
    }
    return solutions.get(exo_name)


def get_expected_sql_result(con, exo_name, tables=None):
    """Exécute la solution avec les vrais noms de tables"""
    solution_sql = get_sql_solution(exo_name)
    if not solution_sql:
        return pd.DataFrame()

    # Remplacer les noms simplifiés
    exo_num = exo_name.split(":")[0].lower().replace("exo", "").strip()
    real_sql = solution_sql

    if exo_num == "1":
        real_sql = real_sql.replace("beverages", "joins.exo1_table1")
        real_sql = real_sql.replace("food_items", "joins.exo1_table2")
    elif exo_num == "2":
        real_sql = real_sql.replace("beverages", "joins.exo2_table1")
        real_sql = real_sql.replace("food_items", "joins.exo2_table2")

    try:
        return con.execute(real_sql).df()
    except Exception as e:
        st.error(f"Erreur dans la solution attendue: {str(e)}")
        return pd.DataFrame()



# ---------------------------------------------------------------------
#  Pandas
# ---------------------------------------------------------------------
def display_join_exercise_pandas(con, exo_name):
    """Affiche un exercice JOIN dans l'onglet Pandas"""
    tables = get_join_tables_for_exo(con, exo_name)

    st.subheader(f"{exo_name} - Pandas")

    col1, col2 = st.columns(2)
    with col1:
        st.write("**Table (disponible sous le nom 'table1'): beverages**")
        st.dataframe(tables["table1"])
    with col2:
        st.write("**Table (disponible sous le nom 'table2'): food_items**")
        st.dataframe(tables["table2"])

    display_pandas_solution_zone(exo_name, tables)


def display_pandas_solution_zone(exo_name, tables):
    """Gère l'affichage des solutions Pandas"""
    st.subheader("Votre réponse en Pandas")
    st.info("""Note: 
    - Les tables sont disponibles sous les noms 'table1' (beverages) et 'table2' (food_items)
    - Votre code doit créer une variable 'result' contenant le DataFrame résultant""")

    user_code = st.text_area(
        "Écrivez votre code Pandas ici:",
        key=f"pandas_{exo_name}",
        height=200,
        value="result = pd.merge(table1, table2, how='cross')"  # Exemple par défaut
    )

    if st.button(f"Tester {exo_name}", key=f"test_pandas_{exo_name}"):
        test_pandas_solution(user_code, exo_name, tables)

    if st.button(f"🔎 Afficher solution {exo_name}"):
        st.code(get_pandas_solution(exo_name), language="python")
        st.markdown("**Résultat attendu**")
        st.dataframe(get_expected_pandas_result(exo_name, tables))


def test_pandas_solution(user_code, exo_name, tables):
    """Valide la solution Pandas de l'utilisateur"""
    try:
        # Préparer l'environnement avec les bons noms de variables
        loc = {
            "pd": pd,
            "table1": tables["table1"],  # beverages
            "table2": tables["table2"],  # food_items
            "__builtins__": __builtins__
        }

        # Exécuter le code utilisateur
        exec(user_code, globals(), loc)

        if "result" not in loc:
            st.error("Erreur: Votre code doit créer une variable nommée 'result'")
            return

        user_result = loc["result"]
        expected = get_expected_pandas_result(exo_name, tables)

        st.write("Votre résultat:")
        st.dataframe(user_result)

        if user_result.equals(expected):
            st.success("✅ Correct !")
        else:
            st.warning("⚠️ Résultat incorrect")
            st.write("Résultat attendu:")
            st.dataframe(expected)

    except Exception as e:
        st.error(f"Erreur dans votre code : {str(e)}")
        st.info("Astuce: Utilisez les variables table1 et table2, pas beverages et food_items")


def get_pandas_solution(exo_name):
    """Retourne la solution Pandas"""
    solutions = {
        "Exo1: CROSS JOIN": """# Solution pour CROSS JOIN
result = pd.merge(table1, table2, how='cross')""",
        "Exo2: INNER JOIN": """# Solution pour INNER JOIN
result = pd.merge(
    table1, 
    table2, 
    left_on='produit_id',
    right_on='categorie_id'
)[['nom', 'prix_unitaire', 'categorie_name', 'univers_name']]
result.columns = ['product_name', 'price', 'category', 'universe']"""
    }
    return solutions.get(exo_name, "# Solution non disponible")


def get_expected_pandas_result(exo_name, tables):
    """Retourne le résultat attendu pour Pandas"""
    try:
        if exo_name == "Exo1: CROSS JOIN":
            return pd.merge(
                tables["table1"],
                tables["table2"],
                how='cross'
            )
        elif exo_name == "Exo2: INNER JOIN":
            return pd.merge(
                tables["table1"],
                tables["table2"],
                left_on='price',
                right_on='food_price'
            )
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Erreur dans la solution attendue Pandas: {str(e)}")
        return pd.DataFrame()

def show_solution_pandas(con, exo_name, category):
    """Affiche la solution complète"""
    st.subheader("Solution")

    st.code(get_pandas_solution(exo_name), language="python")

    st.markdown("**Résultat attendu**")
    st.dataframe(get_expected_sql_result(con, exo_name))

