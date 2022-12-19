import pandas as pd

df2 = pd.read_csv('objects/plz.csv', sep=';', engine='python', encoding = "ISO-8859-1")
df = pd.read_csv('objects/caseBase.csv', sep=';', engine='python', encoding = "ISO-8859-1")
KONTEXTLABEL = {'ländlichsehr peripher': 0, 'ländlichperipher': 1, 'ländlichzentral': 2, 'ländlichsehr zentral': 3, 'teilweise städtischsehr peripher': 4, 'teilweise städtischperipher': 5, 'teilweise städtischzentral': 6, 'teilweise städtischsehr zentral': 7, 'überwiegend städtischsehr peripher': 8, 'überwiegend städtischperipher': 9, 'überwiegend städtischzentral': 10, 'überwiegend städtischsehr zentral': 11}

wert = []
label = []
for index, row in df.iterrows():

    try:
        label.append(KONTEXTLABEL[df2.loc[df2['plz'] == row['plz']]['KontextLabel'].values[0].rstrip()])
    except Exception as e:
        label.append('')

    try:
        wert.append(df2.loc[df2['plz'] == row['plz']]['avg_preis'].values[0])
    except Exception as e:
        wert.append('')

df['kontextLabel'] = label
df['kontextWert'] = wert

df.to_csv('objects/caseBaseKontextLabel.csv', sep=';')
