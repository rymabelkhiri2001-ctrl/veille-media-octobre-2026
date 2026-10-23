import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Veille média octobre 2026", layout="wide")
st.title("Veille média octobre 2026")

df = pd.read_csv("articles.csv")
df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True, format="mixed")

tous_themes = sorted(df["theme"].unique())
toutes_sources = sorted(df["source"].unique())

themes = st.sidebar.multiselect("Thèmes", tous_themes, default=tous_themes)
sources = st.sidebar.multiselect("Sources", toutes_sources, default=toutes_sources)

filtre = df[df["theme"].isin(themes) & df["source"].isin(sources)]
recherche = st.sidebar.text_input("Recherche (mot-clé)")
if recherche:
    masque = (
        filtre["titre"].fillna("").str.contains(recherche, case=False, regex=False)
        | filtre["resume"].fillna("").str.contains(recherche, case=False, regex=False)
    )
    filtre = filtre[masque]

st.metric("Articles affichés", len(filtre))

col1, col2 = st.columns(2)

par_theme = filtre["theme"].value_counts().reset_index()
col1.plotly_chart(px.bar(par_theme, x="theme", y="count", title="Articles par thème"), width="stretch")

par_source = filtre["source"].value_counts().reset_index()
col2.plotly_chart(px.bar(par_source, x="source", y="count", title="Articles par source"), width="stretch")

datees = filtre.dropna(subset=["date"]).copy()
datees["jour"] = datees["date"].dt.date
par_jour = datees.groupby(["jour", "theme"]).size().reset_index(name="articles")
st.plotly_chart(px.line(par_jour, x="jour", y="articles", color="theme", markers=True, title="Évolution par thème"), width="stretch")

st.dataframe(filtre[["date", "source", "theme", "titre", "lien"]], width="stretch")
import re

ENTITES = {
    "Macron": ["macron"],
    "Nuñez": ["nuñez", "nunez"],
    "Geffray": ["geffray"],
    "Lisnard": ["lisnard"],
    "Delogu": ["delogu"],
    "Faure": ["olivier faure"],
    "Binet": ["binet"],
    "Bardella": ["bardella"],
    "Le Pen": ["le pen"],
    "Mélenchon": ["mélenchon"],
    "RN": ["rassemblement national", "rn"],
    "LFI": ["insoumis", "lfi"],
    "Parti socialiste": ["parti socialiste"],
   
}

texte = (filtre["titre"].fillna("") + " " + filtre["resume"].fillna("")).str.lower()
comptes = {}
for nom, alias in ENTITES.items():
    motif = r"\b(?:" + "|".join(re.escape(a) for a in alias) + r")\b"
    comptes[nom] = int(texte.str.contains(motif, regex=True).sum())

entites = pd.DataFrame({"entité": list(comptes), "articles": list(comptes.values())})
entites = entites[entites["articles"] > 0].sort_values("articles")
st.plotly_chart(px.bar(entites, x="articles", y="entité", orientation="h", title="Entités les plus citées"), width="stretch")
dernier = datees["date"].max()
limite = dernier - pd.Timedelta(days=2)
recent = datees[datees["date"] >= limite]
avant = datees[datees["date"] < limite]
nb_jours_avant = max((limite - datees["date"].min()).days, 1)

tendance = pd.DataFrame({
    "moyenne/jour (2 derniers jours)": recent["theme"].value_counts() / 2,
    "moyenne/jour (avant)": avant["theme"].value_counts() / nb_jours_avant,
}).fillna(0).round(1)
tendance["évolution"] = (tendance.iloc[:, 0] - tendance.iloc[:, 1]).round(1)

st.subheader("Signaux : thèmes qui montent")
tendance = tendance.drop(index="Hors thèmes", errors="ignore")
st.dataframe(tendance.sort_values("évolution", ascending=False), width="stretch")