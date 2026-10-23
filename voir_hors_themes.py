import pandas as pd

df = pd.read_csv("articles.csv")
for titre in df[df["theme"] == "Hors thèmes"]["titre"].head(30):
    print("-", titre)