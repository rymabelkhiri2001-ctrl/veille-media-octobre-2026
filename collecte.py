

import os
import feedparser
import pandas as pd

AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"

FLUX = {
    "Le Monde - Politique": "https://www.lemonde.fr/politique/rss_full.xml",
    "Le Monde - Economie": "https://www.lemonde.fr/economie/rss_full.xml",
    "Le Figaro - Politique": "https://www.lefigaro.fr/rss/figaro_politique.xml",
    "Franceinfo - Politique": "https://www.franceinfo.fr/politique.rss",
    "Public Sénat": "https://www.publicsenat.fr/feed",
}

THEMES = {
    "Budget 2027": ["budget", "49.3", "déficit", "dette", "loi de finances", "plf", "impôt", "fiscal", "taxe", "finances publiques", "économies", "bercy", "cour des comptes"],
    "Retraites": ["retraite", "pension", "âge légal", "conclave", "cotisation", "plfss", "sécurité sociale", "assurance vieillesse"],
    "Immigration": ["immigration", "immigré", "migrant", "migratoire", "titre de séjour", "oqtf", "régularisation", "étranger", "asile", "expulsion", "naturalisation"],
    "Numérique/IA": ["intelligence artificielle", " ia ", "l'ia", "l’ia", "numérique", "algorithme", "données", "cyber", "réseaux sociaux", "plateforme", "cnil", "arcom", "fibre", "réseau mobile"],
    "Ordre public / manifestations": ["manifestation", "manifestant", "maintien de l'ordre", "17 octobre", "police", "émeute", "garde à vue", "préfet"],
}


def trouver_theme(texte):
    texte = " " + texte.lower() + " "
    for theme, mots in THEMES.items():
        if any(mot in texte for mot in mots):
            return theme
    return "Hors thèmes"


lignes = []
for source, url in FLUX.items():
    flux = feedparser.parse(url, agent=AGENT)
    print(source, ":", len(flux.entries), "articles")
    for a in flux.entries:
        texte = a.get("title", "") + " " + a.get("summary", "")
        lignes.append({
            "source": source,
            "date": a.get("published", ""),
            "titre": a.get("title", ""),
            "resume": a.get("summary", ""),
            "lien": a.get("link", ""),
            "theme": trouver_theme(texte),
        })

df = pd.DataFrame(lignes)
df["date"] = pd.to_datetime(df["date"], errors="coerce", utc=True, format="mixed")

if os.path.exists("articles.csv"):
    ancien = pd.read_csv("articles.csv")
    ancien["date"] = pd.to_datetime(ancien["date"], errors="coerce", utc=True, format="mixed")
    df = pd.concat([ancien, df])

df = df.drop_duplicates(subset="lien").sort_values("date", ascending=False)
df.to_csv("articles.csv", index=False, encoding="utf-8-sig")

print()
print("Total articles stockés :", len(df))
print(df["theme"].value_counts())