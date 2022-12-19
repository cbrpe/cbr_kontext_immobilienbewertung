from keras.models import Sequential, model_from_json
import numpy as np
import joblib
from CaseBase import CaseBase
import os
import pandas as pd
import CDH_Methoden as cdhm

FILES_IN_NETZE_FOLDER = ["model.json", "weights.h5", "scalerX.save", "scalerY.save"]
PREDICTORS = ['wohnflaeche', 'grundstueckflaeche', 'anz_zimmer', 'keller', 'baujahr', 'energieeffizienz', 'zustand', 'kategorie']

class CDH:

    network_no_context_caseBase: Sequential
    network_no_context_differences: Sequential
    network_context_caseBase: Sequential
    network_context_differences: Sequential

    def __init__(self, cb: CaseBase) -> None:
        self.network_no_context_caseBase = self.search_for_network("network_no_context_caseBase", cb)
        self.network_no_context_differences = self.search_for_network("network_no_context_differences", cb)
        self.network_context_caseBase = self.search_for_network("network_context_caseBase", cb)
        self.network_context_differences = self.search_for_network("network_context_differences", cb)

    def search_for_network(self, network: str, cb: CaseBase):
        if not os.path.isdir("objects/Differences"):
            os.mkdir("objects/Differences")

        if not os.path.exists(os.path.join(os.getcwd(), "objects\Differences\differences.csv")):
            self.createDifferencesData(cb, True)

        path = f'objects/Netze/{network}'
        if not os.path.isdir(path):
            os.mkdir(path)

        for file in FILES_IN_NETZE_FOLDER:
            if not os.path.exists(os.path.join(os.getcwd(), path, file)):
                cdhm.trainiereANN(network)
                break

        json_file = open(path + '/model.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        loaded_model = model_from_json(loaded_model_json)
        loaded_model.load_weights(path + "/weights.h5")

        return loaded_model

    def createDifferencesData(self, cb: CaseBase, anzVergleiche: int = None) -> None:

        columns = cb.getColums_Retrieval()[:]

        columns += ['kontextWert']
        columns += ['price1']
        columns += ['price2']
        columns += ['priceDelta']

        if not anzVergleiche:
            anzahl_cases = cb.getAnz_cases()
        else:
            anzahl_cases = anzVergleiche

        data = []
        for i in range(anzahl_cases):
            print(f"{i}/{anzahl_cases}")
            case_dict = cb.cases.iloc[[i]].to_dict(orient='records')[0]
            case_id = case_dict['id']
            
            dfRetrieval = cb.retrieval(case_dict, "kontextAttribut")
            dfRetrieval = dfRetrieval[dfRetrieval.id != case_id]
            for j in range(3):
                besterCaseDict = cb.cases.loc[cb.cases['id'] == dfRetrieval.iloc[[j]].to_dict(orient='records')[0]['id']].to_dict(orient='records')[0]
                differences = cdhm.getDifferences(case_dict, besterCaseDict, columns)
                data.append(differences)

        dfDifferences = pd.DataFrame(data, columns=columns)
        dfDifferences.to_csv("objects/Differences/differences.csv", sep=';', index=False)
        
    def bestimmeAnpassung(self, situationCaseDict: dict, bestCaseDict: dict, kontext: bool) -> float:

        if kontext:
            inputs = cdhm.getDifferences(situationCaseDict, bestCaseDict, PREDICTORS + ['kontextWert'])
            model = self.network_context_differences
            pfad = "objects/Netze/network_context_differences/"
        else:
            inputs = cdhm.getDifferences(situationCaseDict, bestCaseDict, PREDICTORS)
            model = self.network_no_context_differences
            pfad = "objects/Netze/network_no_context_differences/"

        inputs = np.array([inputs])

        PredictorScaler = joblib.load(pfad + r"scalerX.save")
        TargetVarScaler = joblib.load(pfad + r"scalerY.save")
        
        inputs = PredictorScaler.transform(inputs)
        Predictions = model.predict(inputs, verbose=0)
        Predictions = TargetVarScaler.inverse_transform(Predictions)

        return Predictions[0][0]   

    def bestimmeANNWert(self, situationCaseDict: dict, kontext: bool) -> float:

        inputs = []
        for attribut in PREDICTORS:
            if attribut != "kategorie":
                inputs.append(situationCaseDict[attribut])


        if kontext:
            inputs.append(situationCaseDict['kontextWert'])
            model = self.network_context_caseBase
            pfad = "objects/Netze/network_context_caseBase/"
        else:
            model = self.network_no_context_caseBase
            pfad = "objects/Netze/network_no_context_caseBase/"

        inputs = np.array([inputs])

        PredictorScaler = joblib.load(pfad + r"scalerX.save")
        TargetVarScaler = joblib.load(pfad + r"scalerY.save")
        
        inputs = PredictorScaler.transform(inputs)
        Predictions = model.predict(inputs, verbose=0)
        Predictions = TargetVarScaler.inverse_transform(Predictions)

        return Predictions[0][0]   