import math

def numericSimalarity(x: float, caseWert: float, mean: float, weight: float) -> float:
    abstand = math.sqrt((x - caseWert)**2)
    sim = 1 - (abstand / mean)
    if sim < 0:
        sim = 0

    return sim * weight

def binarySimalarity(x: str, caseWert: str, weight: float) -> float:
    if x == caseWert:
        sim = 1
    else:
        sim = 0
        
    return sim * weight