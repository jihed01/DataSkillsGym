# Data Skills Gym 🏋️‍♂️

Application interactive pour maîtriser les concepts SQL avancés à travers des exercices pratiques.

## Fonctionnalités clés

- 🧩 **Exercices progressifs** sur les JOINs, fonctions window et agrégations
- 💡 **Solutions détaillées** avec explications
- ✅ **Validation en temps réel** des requêtes SQL
- 🐍 **Versions SQL et Pandas** pour chaque exercice
- 📊 **Visualisation interactive** des résultats

## Comment l'utiliser

### Localement
1. Cloner le dépôt :
```bash
git clone https://github.com/jihed01/DataSkillsGym.git
cd DataSkillsGym
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installer les dépendances :
```bash
python create_data.py
```
4. Initialiser la base de données :
```bash
python create_data.py
```
5. Lancer l'application :
````bash
streamlit run app.py
````

## Structure du projet

DataSkillsGym/
├── data/                     # Base de données DuckDB
├── modules/                  # Modules des exercices
│   ├── exos_joins.py         # Exercices JOIN
│   ├── exos_windows.py       # Exercices Window Functions
│   └── __init__.py
├── .gitignore
├── app.py                    # Application principale
├── create_data.py            # Script d'initialisation
├── README.md                 # Ce fichier
└── requirements.txt          # Dépendances

## 📚 Exercices disponibles

### 🔗 JOINs
- **Exo1: CROSS JOIN**  
  Pratiquez les jointures cartésiennes entre deux tables
- **Exo2: INNER JOIN**  
  Maîtrisez les jointures internes avec des conditions complexes

### 🪟 Window Functions
- **Exo1: OVER()**  
  Introduction aux fonctions de fenêtrage avec la clause OVER
- **Exo2: PARTITION BY** *(à venir)*  
  Apprenez à partitionner vos données pour des calculs avancés

### 📊 Agrégations
- **Exo1: GROUP BY basics**  
  Fondamentaux des regroupements et agrégations simples
- **Exo2: Fonctions d'agrégation** *(à venir)*  
  Découvrez les fonctions d'agrégation avancées (ROLLUP, CUBE)