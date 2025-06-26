import streamlit as st
import duckdb
from modules.exos_joins import (
    display_join_exercise_sql,
    display_join_exercise_pandas
)
from modules.exos_windows import display_window_exercise_sql

# Configuration
con = duckdb.connect("data/exercises_sql_tables.duckdb")
st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialisation session state
if 'current_category' not in st.session_state:
    st.session_state.current_category = None
    st.session_state.current_exercise = None

# Sidebar - Navigation
st.sidebar.title("📚 Data Skills Gym")


# Fonction pour créer des radios avec gestion d'état
def create_category_radio(category, options, key):
    with st.sidebar.expander(category["icon"] + " " + category["name"]):
        # Créer une clé unique pour chaque radio
        radio_key = f"radio_{key}"

        # Si une autre catégorie est sélectionnée, réinitialiser cette radio
        if st.session_state.current_category and st.session_state.current_category != key:
            st.session_state[radio_key] = None

        selected = st.radio(
            f"Exercices {category['name']}",
            options,
            index=None,
            key=radio_key,
            on_change=lambda: handle_radio_change(key, st.session_state[radio_key])
        )


def handle_radio_change(category_key, exercise_name):
    """Gère le changement de sélection d'un exercice"""
    # Réinitialiser toutes les autres sélections
    for key in st.session_state:
        if key.startswith("radio_") and key != f"radio_{category_key}":
            st.session_state[key] = None

    # Mettre à jour la sélection courante
    if exercise_name:
        st.session_state.current_category = category_key
        st.session_state.current_exercise = exercise_name
    else:
        st.session_state.current_category = None
        st.session_state.current_exercise = None


# Définition des catégories
categories = {
    "JOIN": {
        "name": "JOIN",
        "icon": "🔗",
        "exercises": ["Exo1: CROSS JOIN", "Exo2: INNER JOIN"]
    },
    "WINDOWS": {
        "name": "WINDOWS",
        "icon": "🪟",
        "exercises": ["Exo1: OVER"]
    },
    "AGGREGATIONS": {
        "name": "AGGREGATIONS",
        "icon": "📊",
        "exercises": ["Exo1: OVER", "Exo2: ROWS BETWEEN"]
    }
}

# Création des radios dans la sidebar
for key, category in categories.items():
    create_category_radio(category, category["exercises"], key.lower())

# Main Content
st.title("Data Skills Gym 🏋️‍♂️")
sql_tab, pandas_tab, spark_tab = st.tabs(["SQL", "Pandas", "Spark"])

# Affichage conditionnel
if st.session_state.current_exercise:
    # Catégorie JOINS
    if st.session_state.current_category == "join":
        with sql_tab:
            display_join_exercise_sql(con, st.session_state.current_exercise)
        with pandas_tab:
            display_join_exercise_pandas(con, st.session_state.current_exercise)

    # Catégorie WINDOWS
    elif st.session_state.current_category == "windows":
        with sql_tab:
            display_window_exercise_sql(con, st.session_state.current_exercise)
        with pandas_tab:
            st.info("Version Pandas à venir")

    # Catégorie AGGREGATIONS
    elif st.session_state.current_category == "aggregations":
        st.info("Catégorie AGGREGATIONS à venir")

else:
    st.info("Sélectionnez un exercice pour commencer")