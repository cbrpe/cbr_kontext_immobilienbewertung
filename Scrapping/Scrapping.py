from bs4 import BeautifulSoup, SoupStrainer 
import urllib.request 
from time import sleep 
import json 
from datetime import datetime
import re 
import os 
import pandas as pd 
import random

folders = ["data/visited/","data/scrapping_data/"]

for folder in folders:
    if not os.path.isdir(folder):
        os.mkdir(folder)
    else:
        print(folder,"existiert bereits")

path_to_visited_urls = "data/visited/visited_urls.json"
if not os.path.isfile(path_to_visited_urls):
    with open(path_to_visited_urls,"w") as file:
        json.dump([],file)

df_cities = pd.read_csv("zip_codes_niedersachsen.csv", sep=";", encoding="iso-8859-1")

cycle_counter=0
while True:
    house_counter=1
    cities_selection = []
    for _ in range(5):
        cities_selection.append(random.choice(df_cities["PLZ"].to_list()))
    cities = [str(x) if len(str(x)) == 5 else "0"+str(x) for x in cities_selection]

    with open(path_to_visited_urls) as file:
        visited_urls = json.load(file)
    
    if len(visited_urls) > 100000:
        visited_urls = []
    
    multiple_house_dict = {}
    cycle_counter+=1
    house_URLs_unique = []
    for city in cities:        
        for page in range(1,6):
            house_URLs = []
            try:
                url = f'https://www.immowelt.de/liste/{city}/haeuser/kaufen?sort=relevanz&sp={page}'
                only_a_tags = SoupStrainer("a")
                soup = BeautifulSoup(urllib.request.urlopen(url).read(),'lxml', parse_only=only_a_tags)
            except Exception as e:
                print("Übersicht: " + str(e) +" "*50, end="\r")
                pass

            for link in soup.find_all("a"):
                if r"/expose/" in str(link.get("href")) and r"/projekte/" not in str(link.get("href")):
                    house_URLs.append(link.get("href"))
                    
            anzahl_vorher = len(house_URLs_unique)
            house_URLs_unique = house_URLs_unique + [house for house in list(set(house_URLs)) if house not in visited_urls]
            anzahl_hinterher = len(house_URLs_unique)
            if anzahl_vorher == anzahl_hinterher:
                break
            
            print(f'Lauf {cycle_counter} | {city} | Seite {page} | {len(house_URLs_unique)} neue URLs', end="\r")
        
    if len(house_URLs_unique)>0:
        print("")
        for URL in house_URLs_unique:
            print(f'Lauf {cycle_counter} | Haus {house_counter}' + f'| Von {len(house_URLs_unique)}' +' '*50, end="\r")
            try:
                house_counter+=1
                house_dict = {}
                try:
                    house = BeautifulSoup(urllib.request.urlopen(URL).read(),'lxml')

                    attribute = ["zeitpunkt", "titel", "preis", "wohnflaeche", "anz_zimmer", "grundstueckflaeche", "strasse", "plz", "stadt", "stadtteil", "kategorie", "anz_stockwerke", "zustand", "keller", "typ", "baujahr", "energieeffizienz", "aussenbereich"]
                    for att in attribute:
                        house_dict[att] = ""

                    house_dict["zeitpunkt"] = str(datetime.now())
                    house_dict["titel"] = house.find("h1", attrs={"class":"ng-star-inserted"}).text
                    house_dict["preis"] = "".join(re.findall(r'[0-9]+',house.find("strong",attrs={"class":"ng-star-inserted"}).text))
                    for value in house.find_all("div", attrs={"class":"hardfact ng-star-inserted"}):
                        if "Wohnfläche" in value.text:
                            house_dict["wohnflaeche"] = value.text.replace(" m²  Wohnfläche ca. ", "").replace(".","").replace(",",".").lstrip()
                        elif "Zimmer" in value.text:
                            house_dict["anz_zimmer"] = value.text.replace("  Zimmer  ", "").lstrip()
                        elif "Grundstücksfl." in value.text:
                            house_dict["grundstueckflaeche"] = value.text.replace(" m²  Grundstücksfl. ca. ", "").replace(".","").replace(",",".").lstrip()

                    house_dict["strasse"] = house.find("span", attrs={"data-cy":"address-street"}).text
                    house_dict["plz"] = "".join(re.findall(r'[0-9]+',house.find("span", attrs={"data-cy":"address-city"}).text))
                    house_dict["stadt"] = "".join(re.findall(r'[a-zA-ZäöüßÄÖÜ]+',house.find("span", attrs={"data-cy":"address-city"}).text.split("(")[0]))
                    house_dict["stadtteil"] = "".join(re.findall(r'\(.*?\)',house.find("span", attrs={"data-cy":"address-city"}).text)).replace("(","").replace(")", "")
                    
                    for value in house.find_all("sd-cell", attrs={"class":"cell ng-star-inserted"}):
                        if "Kategorie" in value.text:
                            house_dict["kategorie"] = value.text.split("Kategorie")[1]
                        elif "Geschosse" in value.text:
                            house_dict["anz_stockwerke"] = value.text.split("Geschosse")[1].replace(" Geschosse", "")
                        elif "Haustyp" in value.text:
                            house_dict["typ"] = value.text.split("Haustyp")[1]
                        elif "Baujahr laut Energieausweis" in value.text:
                            house_dict["baujahr"] = value.text.split("Baujahr laut Energieausweis")[1]
                        elif "Baujahr" in value.text:
                            house_dict["baujahr"] = value.text.split("Baujahr")[1]
                        elif "Effizienzklasse" in value.text:
                            house_dict["energieeffizienz"] = value.text.split("Effizienzklasse")[1]

                    for value in house.find_all("div", attrs={"class":"textlist textlist--icon card-content ng-star-inserted"}):
                        for value in value.find_all("li"):
                            if "keller" in value.text or "Keller" in value.text:
                                house_dict["keller"] = value.text
                            if "Zustand" in value.text:
                                house_dict["zustand"] = value.text
                            if "Terrasse" in value.text or "Balkon" in value.text:
                                house_dict["aussenbereich"] = value.text
                except Exception as e:
                    print(e)
                    continue
                multiple_house_dict[URL] = house_dict
                visited_urls.append(URL)
            except Exception as e:
                print("Detailseite: " + str(e) + " "*50)
                pass
            print("")
    else:
        print("Warten")
        sleep(60)
    if len(multiple_house_dict)>0:
        df = pd.DataFrame(multiple_house_dict).T
        df.to_csv("data/haus/"+re.sub("[.,:,-, ]","_",str(datetime.now()))+".csv",sep=";",index_label="url")
    else:
        print("Keine Daten")
    with open("data/visited/visited_urls.json", "w") as file:
        json.dump(visited_urls, file)
        