import os
import pandas as pd

neueNamen = {"citySearch": "gesuchte_stadt", "date": "zeitpunkt", "title": "titel", "price": "preis", "zimmer": "anz_zimmer", "street": "strasse", "city": "stadt", "district": "stadtteil", "category": "kategorie", "floors": "anz_stockwerke", "condition": "zustand", "basement": "keller", "type": "typ", "year": "baujahr", "efficiency_rating": "energieeffizienz", "terrace": "aussenbereich"}
files = [f for f in os.listdir("scrapping_data")]
anzahl = len(files)
for i, file in enumerate(files):
    if file == "2022-07-24_14_15_35_437050.csv":
        continue
    df = pd.read_csv("scrapping_data/" + file, sep=';')
    # df.rename(neueNamen, axis=1, inplace=True)
    df = df.drop('gesuchte_stadt', axis=1)
    df.to_csv("scrapping_data/" + file, sep=';', index=False)
