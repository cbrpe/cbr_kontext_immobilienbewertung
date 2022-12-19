from dataclasses import dataclass, field
import pandas as pd
import os
import json
from Methoden import generate_id, transform
import Similarity

COLMUNS_RETRIEVAL =  ["wohnflaeche", "grundstueckflaeche", "anz_zimmer", "kategorie", "keller", "baujahr", "energieeffizienz", "zustand"]
COLMUNS_NOT_RETRIEVAL = ['preis', 'id', 'plz', 'strasse', 'stadt', 'stadtteil', 'kontextLabel', 'kontextWert']
KONTEXTLABEL = {'ländlichsehr peripher': 0, 'ländlichperipher': 1, 'ländlichzentral': 2, 'ländlichsehr zentral': 3, 'teilweise städtischsehr peripher': 4, 'teilweise städtischperipher': 5, 'teilweise städtischzentral': 6, 'teilweise städtischsehr zentral': 7, 'überwiegend städtischsehr peripher': 8, 'überwiegend städtischperipher': 9, 'überwiegend städtischzentral': 10, 'überwiegend städtischsehr zentral': 11}
RETRIEVAL_VORGEHENSWEISEN = ['standard', 'kontextFiltern', 'kontextAttribut']

@dataclass
class CaseBase:
    casebase_file_path: str
    scrapping_folder_path: str
    used_files_path: str
    cases: pd.DataFrame = field(default_factory=pd.DataFrame)
    _anz_cases: int = 0

    def __init__(self, casebase_file_path: str, scrapping_folder_path: str, used_files_path: str) -> None:
        self.casebase_file_path = casebase_file_path
        self.scrapping_folder_path = scrapping_folder_path
        self.used_files_path = used_files_path

        if not os.path.isfile(self.casebase_file_path):
            pd.DataFrame(columns=COLMUNS_RETRIEVAL+COLMUNS_NOT_RETRIEVAL).to_csv(casebase_file_path, sep=';', index = False)

        self.cases = pd.read_csv(casebase_file_path, sep=';')
        self._anz_cases = len(self.cases)

        self.updateCaseBase()
    
    def getAnz_cases(self):
        return len(self.cases)

    def getColums_Retrieval(self):
        return COLMUNS_RETRIEVAL
    
    def save(self) -> None:
        self.cases.to_csv(self.casebase_file_path, sep=";", index = False)

    def preprocessing(self) -> None:
        df = self.cases
        for column in COLMUNS_RETRIEVAL:
            df[column] = df[column].apply(transform, args=(column,))

        self.cases = df

    def add_Case(self, case: dict) -> None:
        caseRichtigeStruktur = {}
        dfKontextLabel = pd.read_csv("objects/Kontextinformationen.csv", sep=';', engine='python', encoding = "ISO-8859-1")
        for column in COLMUNS_RETRIEVAL + COLMUNS_NOT_RETRIEVAL:
            if column == 'id':
                caseRichtigeStruktur['id'] = generate_id()
            elif column == 'kontextLabel':
                try:
                    caseRichtigeStruktur[column] = KONTEXTLABEL[dfKontextLabel.loc[dfKontextLabel['plz'] == case['plz']]['KontextLabel'].values[0].strip()]
                except Exception as e:
                    print(e)
                    print(case['plz'])
                    return None
            elif column == 'kontextWert':
                try:
                    caseRichtigeStruktur[column] = dfKontextLabel.loc[dfKontextLabel['plz'] == case['plz']]['avg_preis'].values[0]
                except Exception:
                    return None
            else:
                caseRichtigeStruktur[column] = case[column]

        self.cases = pd.concat([self.cases, pd.DataFrame.from_records([caseRichtigeStruktur])])
        # self.cases = self.cases.append(caseRichtigeStruktur, ignore_index=True)
        self._anz_cases += 1

    def updateCaseBase(self) -> None:
        if not os.path.isfile(self.used_files_path):
            with open(self.used_files_path, 'w') as file:
                used_files = []
                with open(self.used_files_path, "w") as file:
                    json.dump(used_files, file)
        else:
            with open(self.used_files_path) as file:
                used_files = json.load(file)

        files = [f for f in os.listdir(self.scrapping_folder_path) if (os.path.isfile(os.path.join(self.scrapping_folder_path, f)) and f not in used_files)]
        anzahl = len(files)
        for i, file in enumerate(files):
            print(f'{i}/{anzahl}')
            if i > 5:
                break
            df = pd.read_csv(self.scrapping_folder_path + "/" + file, sep=';')
            if len(df) > 0:
                for row in df.to_dict(orient='records'):
                    self.add_Case(row)
            used_files.append(file)

        with open(self.used_files_path, "w") as file:
            json.dump(used_files, file)

        self.preprocessing()
        self.cases.dropna(subset=["wohnflaeche", "grundstueckflaeche", "anz_zimmer", "kategorie", "keller", "baujahr", "energieeffizienz", "zustand"], inplace=True)
        self.cases = self.cases[["id", "plz", "stadt", "strasse", "stadtteil", "preis", "wohnflaeche", "grundstueckflaeche", "anz_zimmer", "kategorie", "keller", "baujahr", "energieeffizienz", "zustand", "kontextLabel", "kontextWert"]]
        self.save()

    def retrieval(self, case: dict, vorgehen: str = "standard") -> pd.DataFrame:
        if vorgehen not in RETRIEVAL_VORGEHENSWEISEN:
            vorgehen = "standard"

        GEWICHTUNGS_SET = "weight"
        columns_retrieval = COLMUNS_RETRIEVAL[:]
        if vorgehen == "kontextAttribut":
            columns_retrieval += ['kontextWert']
            GEWICHTUNGS_SET = "weight_context"

        dfSimilarity = pd.DataFrame(columns=list(columns_retrieval) + ['kontextLabel', 'summe', 'preis', 'id'])
        dfSimilarity = dfSimilarity.assign(preis=self.cases['preis'])
        dfSimilarity = dfSimilarity.assign(id=self.cases['id'])

        dfCaseBase = self.cases

        dfGewichtungen = pd.read_csv("objects/Gewichtungen.csv", sep=';' )
        if vorgehen == 'kontextFiltern':
            dfSimilarity = dfSimilarity.assign(kontextLabel=self.cases['kontextLabel'])
            kontextlabel = case['kontextLabel']
            dfCaseBase  = dfCaseBase[dfCaseBase['kontextLabel'] == kontextlabel]

        for column in columns_retrieval:
            attributInfo = dfGewichtungen[dfGewichtungen['feature'] == column].iloc[0]
            s = dfCaseBase[column]
            if attributInfo['similarity_type'] == 'numeric':
                dfSimilarity[column] = s.apply(Similarity.numericSimalarity, args=(case[column], float(attributInfo['mean']), attributInfo[GEWICHTUNGS_SET]))
            else:
                dfSimilarity[column] = s.apply(Similarity.binarySimalarity, args=(case[column], attributInfo[GEWICHTUNGS_SET]))
       
        dfSimilarity['summe'] = dfSimilarity[columns_retrieval].sum(axis=1)
        dfSimilarity = dfSimilarity.sort_values('summe', ascending=False)
        dfSimilarity = dfSimilarity.sort_values('summe', ascending=False)

        return dfSimilarity