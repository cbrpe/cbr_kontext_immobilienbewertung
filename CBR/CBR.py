from CaseBase import CaseBase
from CDH import CDH
from random import randrange

class CBR:
    cb: CaseBase
    cdh: CDH

    def __init__(self) -> None:
        self.cb = CaseBase(casebase_file_path="objects/caseBase.csv", scrapping_folder_path="../Scrapping/data/scrapping_data", used_files_path="../Scrapping/data/visited/visited.json")
        self.cdh = CDH(self.cb)

    def test(self, no_tests: int, vorgehenRetrieval: str = "standard", vorgehenAdaption: str = "null" ) -> float:
        # vorgehenRetrieval: "standard", "kontextAttribut", "kontextFiltern"
        # vorgehenAdaption: "null", "3_nn", "cdh", "cdh_kontext", "twin_system", "twin_system_kontext"

        y = []
        y_solution = []

        for k in range(no_tests):
            anzahl_cases = self.cb.getAnz_cases()

            if no_tests == anzahl_cases:
                zufalls_case_no = k
            else:
                zufalls_case_no = randrange(anzahl_cases)

            zufalls_case_dict = self.cb.cases.iloc[[zufalls_case_no]].to_dict(orient='records')[0]
            zufalls_case_id = zufalls_case_dict['id']

            df = self.cb.retrieval(zufalls_case_dict, vorgehenRetrieval)
            df = df[df.id != zufalls_case_id]

            if vorgehenAdaption == '3_nn':
                solution_cbr = 0
                for i in range(3):
                    solution_cbr += df['preis'].iloc[i]

                solution_cbr = solution_cbr/3
            elif vorgehenAdaption == 'cdh':
                anpassung = self.cdh.bestimmeAnpassung(zufalls_case_dict, self.cb.cases[self.cb.cases.id==df['id'].iloc[0]].to_dict(orient='records')[0], False)
                solution_cbr = df['preis'].iloc[0] + anpassung
            elif vorgehenAdaption == 'cdh_kontext':
                anpassung = self.cdh.bestimmeAnpassung(zufalls_case_dict, self.cb.cases[self.cb.cases.id==df['id'].iloc[0]].to_dict(orient='records')[0], True)
                solution_cbr = df['preis'].iloc[0] + anpassung
            elif vorgehenAdaption == 'twin_system':
                ann_wert = self.cdh.bestimmeANNWert(self.cb.cases[self.cb.cases.id==df['id'].iloc[0]].to_dict(orient='records')[0], False)
                solution_cbr = (df['preis'].iloc[0] + ann_wert)/2
            elif vorgehenAdaption == 'twin_system_kontext':
                ann_wert = self.cdh.bestimmeANNWert(self.cb.cases[self.cb.cases.id==df['id'].iloc[0]].to_dict(orient='records')[0], True)
                solution_cbr = (df['preis'].iloc[0] + ann_wert)/2
            else:
                solution_cbr = df['preis'].iloc[0]
            
            solution = zufalls_case_dict['preis']

            y.append(solution_cbr)
            y_solution.append(solution)

        summe = 0
        for i in range(len(y)):
            summe += 100 * abs(y[i] - y_solution[i])/y[i]
        
        mape  = summe /  len(y_solution)

        return 100 - mape