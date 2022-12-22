from CBR import CBR
import os

# Falls übergeordneter Ordner in IDE geöffnet

if os.getcwd().split("\\")[-1] == 'CBR_Kontext_Immobilienbewertung':
    os.chdir(os.getcwd() + '/CBR')

RETRIEVAL_METOHDE = 'standard'  # "standard", "kontextAttribut", "kontextFiltern"
ADAPTION_METHODE = 'null'       # "null", "3_nn", "cdh", "cdh_kontext", "twin_system", "twin_system_kontext"

cbr = CBR()


print(cbr.test(cbr.cb.getAnz_cases(), RETRIEVAL_METOHDE, ADAPTION_METHODE))
