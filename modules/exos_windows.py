import duckdb
import pandas as pd
import streamlit as st


def get_window_tables_for_exo(con, exo_name):
    """Récupère les tables avec des noms simplifiés"""
    exo_num = exo_name.split(":")[0].lower().replace("exo", "").strip()

    if exo_num == "1":
        return {
            "table1": con.execute("SELECT * FROM window_funcs.exo1_data").df(),
            "sql_names": {
                "table1": "exo1_data",
            },
            "exo_num": exo_num,
            "display_names": {
                "table1": "furniture",  # Ce nom est utilisé dans les remplacements
            }
        }
    elif exo_num == "2":
        return None
#-----------------------------------------------------------
#  SQL
#---------------------------------------------------------------------

def display_window_exercise_sql(con, exo_name):
    """Affiche l'exercice WINDOW sélectionné"""
    tables = get_window_tables_for_exo(con, exo_name)

    if not tables:
        st.error("Exercice non trouvé")
        return

    st.subheader(f"{exo_name} - SQL")
    st.dataframe(tables["table1"])

    # Zone de solution
    st.subheader("Votre réponse SQL")
    user_input = st.text_area(
        "Écrivez votre requête SQL ici:",
        key=f"sql_{exo_name}"
    )

    if st.button(f"Tester {exo_name}"):
        try:
            # Remplacer le nom simplifié par le vrai nom de table
            real_query = user_input.replace("furniture", "window_funcs.exo1_data")
            user_result = con.execute(real_query).df()
            st.dataframe(user_result)
        except Exception as e:
            st.error(f"Erreur SQL: {str(e)}")

    if st.button(f"🔎 Afficher la solution"):
        st.code(get_sql_solution(exo_name), language="sql")
        st.markdown("**Résultat attendu**")
        st.dataframe(get_expected_sql_result(con, exo_name, tables))


def display_window_exercise_sql(con, exo_name):
    """Affiche l'exercice WINDOW sélectionné"""
    tables = get_window_tables_for_exo(con, exo_name)

    if not tables:
        st.error("Exercice non trouvé")
        return

    st.subheader(f"{exo_name} - SQL")
    st.dataframe(tables["table1"])

    # Zone de solution
    st.subheader("Votre réponse SQL")
    user_input = st.text_area(
        "Écrivez votre requête SQL ici:",
        key=f"sql_{exo_name}"
    )

    if st.button(f"Tester {exo_name}"):
        test_sql_solution(con, user_input, exo_name, tables)

    if st.button(f"🔎 Afficher la solution"):
        st.code(get_sql_solution(exo_name), language="sql")
        st.markdown("**Résultat attendu**")
        st.dataframe(get_expected_sql_result(con, exo_name, tables))


def test_sql_solution(con, user_query, exo_name, tables):
    """Valide la solution SQL de l'utilisateur"""
    try:
        # Remplacer les noms simplifiés par les vrais noms de tables
        exo_num = exo_name.split(":")[0].lower().replace("exo", "").strip()
        real_query = user_query

        if exo_num == "1":
            real_query = real_query.replace("furniture", "window_funcs.exo1_data")

        # Exécuter la requête
        user_result = con.execute(real_query).df()

        # Obtenir le résultat attendu
        expected = get_expected_sql_result(con, exo_name, tables)

        # Afficher les résultats
        st.write("Votre résultat:")
        st.dataframe(user_result)

        # Normaliser les DataFrames pour la comparaison
        def normalize_df(df):
            # Convertir toutes les colonnes en strings pour éviter les problèmes de types
            return df.astype(str).reset_index(drop=True)

        user_norm = normalize_df(user_result)
        expected_norm = normalize_df(expected)

        # Comparer les résultats
        if user_norm.equals(expected_norm):
            st.success("✅ Correct !")
        else:
            st.warning("⚠️ Résultat incorrect")
            st.write("Résultat attendu:")
            st.dataframe(expected)

            # Afficher les différences pour aider au débogage
            st.write("Différences:")
            diff = pd.concat([user_norm, expected_norm]).drop_duplicates(keep=False)
            st.dataframe(diff)

    except Exception as e:
        st.error(f"Erreur SQL : {str(e)}")


def display_solution_toggle(con, exo_name, category, tables):
    """Gère l'affichage/masquage de la solution"""
    session_key = f"show_{exo_name}_solution"

    if st.button("🔎 Afficher/Masquer la solution"):
        if session_key not in st.session_state:
            st.session_state[session_key] = False
        st.session_state[session_key] = not st.session_state[session_key]

    if st.session_state.get(session_key, False):
        show_solution_sql(con, exo_name, category, tables)


def show_solution_sql(con, exo_name, category, tables):
    """Affiche la solution complète"""
    st.subheader("Solution")

    st.code(get_sql_solution(exo_name), language="sql")

    st.markdown("**Résultat attendu**")
    st.dataframe(get_expected_sql_result(con, exo_name, tables))


def get_sql_solution(exo_name):
    """Retourne la solution SQL formatée avec des noms simples"""
    solutions = {
        "Exo1: OVER": """
            SELECT 
                category,
                item,
                weight,
                SUM(weight) OVER () AS poids_total
            FROM furniture
            ORDER BY category, item
            """,
        "Exo2: INNER JOIN": ""
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
        real_sql = real_sql.replace("furniture", "window_funcs.exo1_data")
        try:
            result = con.execute(real_sql).df()
            # Assurez-vous que le résultat a les bonnes colonnes
            if "poids_total" not in result.columns:
                st.error("La colonne 'poids_total' est manquante dans le résultat")
            return result
        except Exception as e:
            st.error(f"Erreur dans la solution attendue: {str(e)}")
            return pd.DataFrame()
    else:
        return pd.DataFrame()