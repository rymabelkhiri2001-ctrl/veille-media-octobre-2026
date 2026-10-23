# Veille média octobre 2026

Tableau de bord interactif de veille média en affaires publiques :
il collecte l'actualité française, la classe par thème et repère les sujets qui montent.

## Thèmes suivis
Budget 2027, retraites, immigration, numérique/IA, ordre public / manifestations.

## Sources
Le Monde (politique, économie), Le Figaro, Franceinfo, Public Sénat (flux RSS).

## Fichiers
- `collecte.py` : collecte les articles, les classe par mots-clés, les stocke dans `articles.csv`
- `app.py` : tableau de bord Streamlit (filtres, graphiques, entités, signaux)
- `collecte_auto.bat` : lance la collecte (utilisé par la tâche planifiée quotidienne)

## Lancer le projet
    pip install pandas feedparser requests streamlit plotly
    python collecte.py
    streamlit run app.py