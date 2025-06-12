#pylint: disable=missing-module-docstring

import ast
import duckdb
import streamlit as st
#------------------------------------------
import streamlit as st
import pandas as pd
##--------------
con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
#----------------------------
# Configuration de la page
st.set_page_config(layout="wide")

# Sidebar - Catégories d'exercices
st.sidebar.title("📂 Catégories")

# Section "JOIN"
with st.sidebar.expander("🔗 JOIN"):
    join_choice = st.radio(
        "Exercices JOIN",
        ["exo1: CROSS JOINS", "exo2: INNER JOINS"],
        # ["exo1: CROSS JOINS", "exo2: INNER JOINS", "exo3: CROSS JOINS & INNER JOINS",
        #  "exo4: CROSS JOINS", "exo5: FULL OUTER JOINS", "exo6: SELF JOINS"],
        index=None
    )
#
# Section "WINDOWS"
# with st.sidebar.expander("🪟 WINDOWS"):
#     windows_choice = st.radio(
#         "Exercices WINDOWS",
#         ["exo1: GROUP BY"],
#         # ["exo1: GROUP BY", "exo2: CASE WHEN", "exo3: GROUPING SET",
#         #  "exo4: FILTER", "exo5: ROLLS UP & CUBE"],
#         index=None
#     )
# 
# # Section "AGGREGATIONS"
# with st.sidebar.expander("📊 AGGREGATIONS"):
#     agg_choice = st.radio(
#         "Exercices AGGREGATIONS",
#         ["exo1: OVER", "exo2: ROWS BETWEEN", "exo3: PARTITION BY",
#          "exo4: LAG", "exo5: ROWS NUMBER vs RANK vs DENSE_RANK", "exo6: QUALITY"],
#         index=None
#     )

# Main Content
st.title("Data Skills Gym 🏋️‍♂️")

# Sélection du langage (onglets)
lang_tab1, lang_tab2, lang_tab3 = st.tabs(["SQL", "Pandas", "Spark"])

#------------------------

if join_choice == "exo1: CROSS JOINS":
    #SQL
    with lang_tab1:
        st.subheader("Énoncé")
        st.write("Réalisez un CROSS JOIN entre les tables beverages et food_items")
        st.subheader("La data")
        # Afficher les deux tables côte à côte
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Table 1: beverages")
            beverages_df = con.execute("SELECT * FROM beverages").df()
            st.dataframe(beverages_df)

        with col2:
            st.subheader("Table 2: food_items")
            food_items_df = con.execute("SELECT * FROM food_items").df()
            st.dataframe(food_items_df)

        st.subheader("Votre réponse")
        query = st.text_area(
            label="Écrivez votre requête SQL pour réaliser un CROSS JOIN entre ces tables:",
            key="user input"
        )
        if query:
            result = con.execute(query).df()
            st.dataframe(result)

        st.subheader(" Résultat")
        # Exemple de validation
        if 'result' in locals():
            expected_result = con.execute("""
                SELECT * FROM beverages CROSS JOIN food_items
            """).df()

            if result.equals(expected_result):
                st.success("✅ Correct !")
            else:
                st.warning("⚠️ Le résultat ne correspond pas à la solution attendue.")
        # solution SQL
        st.subheader(" Solution")
        # Solution avec toggle (affichage/masquage)
        if 'show_solution' not in st.session_state:
            st.session_state.show_solution = False

        if st.button("🔎 Afficher/Masquer la solution"):
            st.session_state.show_solution = not st.session_state.show_solution

        if st.session_state.show_solution:
            st.subheader("Requête attendue")
            st.code("""
        SELECT *
        FROM beverages
        CROSS JOIN food_items;
                """, language="sql")

            st.subheader("Résultat attendu")
            solution = con.execute("""
                    SELECT beverages.*, food_items.* 
                    FROM beverages 
                    CROSS JOIN food_items
                """).df()
            st.dataframe(solution)
    with lang_tab2:  # Onglet Pandas
        st.subheader("Énoncé")
        st.write(
        "Réalisez un produit cartésien (équivalent CROSS JOIN) entre les DataFrames beverages et food_items")

        # Afficher les DataFrames
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("DataFrame: beverages")
            beverages_df = con.execute("SELECT * FROM beverages").df()
            st.dataframe(beverages_df)

        with col2:
            st.subheader("DataFrame: food_items")
            food_items_df = con.execute("SELECT * FROM food_items").df()
            st.dataframe(food_items_df)

        st.subheader("Votre réponse en Pandas")
        pandas_code = st.text_area(
            label="Écrivez votre code pandas pour réaliser un CROSS JOIN entre ces tables:",
            key="user input pandas"
        )

        if st.button("Exécuter le code Pandas", key="run_pandas_exo1"):
            try:
                # Créer un environnement d'exécution sécurisé
                loc = {"pd": pd, "beverages_df": beverages_df, "food_items_df": food_items_df}
                exec(pandas_code, globals(), loc)
                if "result" in loc:
                    user_result = loc["result"]
                    st.subheader("Votre résultat")
                    st.dataframe(user_result)

                    # Validation
                    expected_result = pd.merge(beverages_df, food_items_df, how='cross')
                    if user_result.equals(expected_result):
                        st.success("✅ Correct !")
                    else:
                        st.warning("⚠️ Le résultat ne correspond pas à la solution attendue.")
                else:
                    st.error("Votre code doit créer une variable 'result' contenant le DataFrame résultat")
            except Exception as e:
                        st.error(f"Erreur: {e}")

         # Solution Pandas
        if 'show_pandas_solution_exo1' not in st.session_state:
            st.session_state.show_pandas_solution_exo1 = False

        if st.button("🔎 Afficher/Masquer la solution Pandas", key="solution_pandas_exo1"):
            st.session_state.show_pandas_solution_exo1 = not st.session_state.show_pandas_solution_exo1

        if st.session_state.show_pandas_solution_exo1:
            st.subheader("Solution Pandas")
            st.code("""
            # Méthode 1 (Pandas 1.2+)
            result = pd.merge(beverages_df, food_items_df, how='cross')

            # Méthode 2 (Pour versions antérieures)
            from itertools import product
            result = pd.DataFrame(
                product(beverages_df.values, food_items_df.values),
                columns=beverages_df.columns.tolist() + food_items_df.columns.tolist()
            )
                        """, language="python")

        st.subheader("Résultat attendu")
        solution = pd.merge(beverages_df, food_items_df, how='cross')
        st.dataframe(solution)

            #------
elif join_choice == "exo2: INNER JOINS":
    with lang_tab1:
        st.header("Exercice 2: INNER JOIN")
        st.write("""
        **Énoncé** :  
        Trouver les combinaisons où le prix des boissons correspond au prix des articles alimentaires.
        """)
        # Affichage des tables (mêmes tables que l'exo1)
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Table: beverages")
            st.dataframe(con.execute("SELECT * FROM beverages").df())
        with col2:
            st.subheader("Table: food_items")
            st.dataframe(con.execute("SELECT * FROM food_items").df())

        st.subheader("Votre réponse")
        query = st.text_area(
            label="Écrivez votre requête SQL pour réaliser un CROSS JOIN entre ces tables:",
            key="user input exo2"
        )
        if query:
            result = con.execute(query).df()
            st.dataframe(result)
        # Exemple de validation
        if 'result' in locals():
            expected_result = con.execute("""
            SELECT b.beverage, b.price, f.food_item, f.food_price
            FROM beverages b
            INNER JOIN food_items f ON b.price = f.food_price
            """).df()

            if result.equals(expected_result):
                st.success("✅ Correct !")
            else:
                st.warning("⚠️ Le résultat ne correspond pas à la solution attendue.")


        # solution
        st.subheader(" Solution")
        # Solution avec toggle (affichage/masquage)
        if 'show_solution' not in st.session_state:
            st.session_state.show_solution = False

        if st.button("🔎 Afficher/Masquer la solution"):
            st.session_state.show_solution = not st.session_state.show_solution

        if st.session_state.show_solution:
            st.subheader("Requête attendue")
            st.code("""
            SELECT b.beverage, b.price, f.food_item, f.food_price
            FROM beverages b
            INNER JOIN food_items f ON b.price = f.food_price;
                """, language="sql")

            st.subheader("Résultat attendu")
            solution = con.execute("""
            SELECT b.beverage, b.price, f.food_item, f.food_price
            FROM beverages b
            INNER JOIN food_items f ON b.price = f.food_price
                """).df()
            st.dataframe(solution)
#.......................................
    with lang_tab2:  # Onglet Pandas
        st.subheader("Énoncé")
        st.write("Fusionnez les DataFrames sur les prix correspondants (équivalent INNER JOIN)")

        # Afficher les DataFrames
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("DataFrame: beverages")
            beverages_df = con.execute("SELECT * FROM beverages").df()
            st.dataframe(beverages_df)

        with col2:
            st.subheader("DataFrame: food_items")
            food_items_df = con.execute("SELECT * FROM food_items").df()
            st.dataframe(food_items_df)

        st.subheader("Votre réponse en Pandas")
        pandas_code = st.text_area(
            label="Écrivez votre code Pandas pour fusionner sur les prix:",
            key="pandas_input_exo2"
        )

        if st.button("Exécuter le code Pandas", key="run_pandas_exo2"):
            try:
                loc = {"pd": pd, "beverages_df": beverages_df, "food_items_df": food_items_df}
                exec(pandas_code, globals(), loc)
                if "result" in loc:
                    user_result = loc["result"]
                    st.subheader("Votre résultat")
                    st.dataframe(user_result)

                    # Validation
                    expected_result = pd.merge(
                        beverages_df,
                        food_items_df,
                        left_on='price',
                        right_on='food_price'
                    )
                    if user_result.equals(expected_result):
                        st.success("✅ Correct !")
                    else:
                        st.warning("⚠️ Le résultat ne correspond pas à la solution attendue.")
                else:
                    st.error("Votre code doit créer une variable 'result' contenant le DataFrame résultat")
            except Exception as e:
                st.error(f"Erreur: {e}")

        # Solution Pandas
        if 'show_pandas_solution_exo2' not in st.session_state:
            st.session_state.show_pandas_solution_exo2 = False

        if st.button("🔎 Afficher/Masquer la solution Pandas", key="solution_pandas_exo2"):
            st.session_state.show_pandas_solution_exo2 = not st.session_state.show_pandas_solution_exo2

        if st.session_state.show_pandas_solution_exo2:
            st.subheader("Solution Pandas")
            st.code("""
    # Méthode standard
    result = pd.merge(
        beverages_df,
        food_items_df,
        left_on='price',
        right_on='food_price'
    )

    # Alternative avec join
    result = beverages_df.set_index('price').join(
        food_items_df.set_index('food_price'),
        how='inner',
        lsuffix='_beverage',
        rsuffix='_food'
    ).reset_index()
                """, language="python")

            st.subheader("Résultat attendu")
            solution = pd.merge(
                beverages_df,
                food_items_df,
                left_on='price',
                right_on='food_price'
            )
            st.dataframe(solution)
#..........................
else:
    st.info("Sélectionnez un exercice dans la sidebar pour commencer")
#---------------


