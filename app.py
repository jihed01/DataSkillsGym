import streamlit as st
import duckdb
from modules.exos_joins import (
    display_join_exercise_sql,
    display_join_exercise_pandas
)

# Configuration
con = duckdb.connect("data/exercises_sql_tables.duckdb")
st.set_page_config(layout="wide")

# Sidebar - Navigation
st.sidebar.title("📚 Data Skills Gym")

# Section "JOIN"
with st.sidebar.expander("🔗 JOIN"):
    join_choice = st.radio(
        "Exercices JOIN",
        ["Exo1: CROSS JOIN", "Exo2: INNER JOIN"],
        # ["exo1: CROSS JOIN", "exo2: INNER JOINS", "exo3: CROSS JOINS & INNER JOINS",
        #  "exo4: CROSS JOINS", "exo5: FULL OUTER JOINS", "exo6: SELF JOINS"],
        index=None
    )
#Section "WINDOWS"
with st.sidebar.expander("🪟 WINDOWS"):
    windows_choice = st.radio(
        "Exercices WINDOWS",
        ["exo1: GROUP BY"],
        # ["exo1: GROUP BY", "exo2: CASE WHEN", "exo3: GROUPING SET",
        #  "exo4: FILTER", "exo5: ROLLS UP & CUBE"],
        index=None
    )

# Section "AGGREGATIONS"
with st.sidebar.expander("📊 AGGREGATIONS"):
    agg_choice = st.radio(
        "Exercices AGGREGATIONS",
        ["exo1: OVER", "exo2: ROWS BETWEEN", "exo3: PARTITION BY",
         "exo4: LAG", "exo5: ROWS NUMBER vs RANK vs DENSE_RANK", "exo6: QUALITY"],
        index=None
    )

# Main Content
st.title("Data Skills Gym 🏋️‍♂️")
sql_tab, pandas_tab, spark_tab = st.tabs(["SQL", "Pandas", "Spark"])

# Catégorie JOINS
if join_choice == "Exo1: CROSS JOIN":
    with sql_tab:
        display_join_exercise_sql(con, join_choice)
    with pandas_tab:
        display_join_exercise_pandas(con, join_choice)
elif join_choice == "Exo2: INNER JOIN":
    with sql_tab:
        display_join_exercise_sql(con, join_choice)
    with pandas_tab:
        display_join_exercise_pandas(con, join_choice)
else:
    st.info("Sélectionnez une catégorie pour commencer")