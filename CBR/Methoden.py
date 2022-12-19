from random import randint
from datetime import datetime

FEHLER_TEXTE = ["", "k.A.", "kA  Wohnfläche  ", "kA  Grundstücksfl  ", "Straße nicht freigegeben"]
ZUSTAND_ARTEN = {'renoviert': 0, 'gepflegt': 1,  'teilsaniert': 2, 'renovierungsbedürftig': 3}
KELLER_ARTEN = {'voll unterkellert': 2, 'teilweise unterkellert': 1, 'nicht unterkellert': 0}
ENERGIEEFFIZIENZ_ARTEN = {'A++': 9, 'A+': 8, 'A': 7, 'B': 6, 'C': 5, 'D': 4, 'E': 3, 'F': 2, 'G': 1, 'H': 0}
KATEGORIE_ARTEN = ['reihenhaus', 'villa', 'einfamilienhaus', 'doppelhaushälfte', 'bungalow', 'mehrfamilienhaus']

def generate_id(n:int = 8) -> int:
    n = 8
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def isEmpty(self, value: str) -> bool:
    if value is None or str(value) == 'nan' or value == "" or str(value).isspace() or value in FEHLER_TEXTE:
        return True
    else:
        return False

def transform(value: any, attr: str, ):
    if value is None or str(value) == 'nan' or value == "" or str(value).isspace() or value in FEHLER_TEXTE:
        return None
    else:
        if attr == 'zimmer':
            value = float(str(value).replace(',', '.'))
        elif attr == 'zustand':
            if type(value) == str:
                check = False
                if 'projektiert' in value:
                    value = 0
                    check = True
                else:
                    for condition in ZUSTAND_ARTEN.keys():
                        if condition in value:
                            value = ZUSTAND_ARTEN[condition]
                            check = True
                            break
                if not check:
                    value = None
        elif attr == 'keller':
            if type(value) == str:
                check = False
                value = value.lower()
                for keller in KELLER_ARTEN.keys():
                    if keller in value:
                        value = KELLER_ARTEN[keller]
                        check = True
                        break
                if not check:
                    value = None
        elif attr == 'energieeffizienz':
            if type(value) == str:
                if value in ENERGIEEFFIZIENZ_ARTEN.keys():
                    value = ENERGIEEFFIZIENZ_ARTEN[value]
                else:
                    value = None
        elif attr == 'baujahr':
            value = str(value)
            value = value.lower()

            if 'um' in value:
                value = value.replace('um', '').replace(' ', '')

            if 'vor' in value:
                value = value.replace('vor', '').replace(' ', '')

            if 'neu' in value:
                value = str(datetime.now().year)

            if 'ca.' in value:
                value = value.replace('ca.', '').replace(' ', '')

            if '/' in value:
                value = value.split('/')[0]

            try:
                value = int(float(value))
            except ValueError:
                value = None  
        elif attr == 'kategorie':
            if type(value) == str:
                check = False
                value = value.lower()
                for kategorie in KATEGORIE_ARTEN:
                    if kategorie in value:
                        value = kategorie
                        check = True
                        break

                if 'schloss' in value or 'herrenhaus' in value:
                    value = 'villa'
                    check = True
                elif 'wohn & geschäftshaus' in value:
                    value = 'stadthaus'
                    check = True
                elif 'bauernhaus' in value or 'stadthaus' in value :
                    value = 'einfamilienhaus'
                    check = True
                elif 'Finca' in value:
                    value = 'bungalow'
                    check = True

                if not check:
                    value = None

    return value      
