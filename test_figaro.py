import feedparser

flux = feedparser.parse(
    "https://www.lefigaro.fr/rss/figaro_politique.xml",
    agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
)
print("Statut HTTP :", flux.get("status"))
print("Articles :", len(flux.entries))