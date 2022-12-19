from typing import List
import numpy as np
from keras.layers import Dense
from keras.models import Sequential
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd 
import joblib

def findeBesteHyperParameter(ANN_type: str):
    # Defining the list of hyper parameters to try
    batch_size_list = [5, 10, 15, 20]
    epoch_list  =   [5, 10, 50, 100]
    
    SearchResultsData=pd.DataFrame(columns=['TrialNumber', 'Parameters', 'Accuracy'])
    
    # initializing the trials
    TrialNumber=0
    for batch_size_trial in batch_size_list:
        for epochs_trial in epoch_list:
            TrialNumber+=1
            
            accuracy = trainiereANN(batch_size_trial, epochs_trial, ANN_type)
            
            print(TrialNumber, 'Parameters:','batch_size:', batch_size_trial,'-', 'epochs:',epochs_trial, 'Accuracy:', accuracy)
            
            SearchResultsData=SearchResultsData.append(pd.DataFrame(data=[[TrialNumber, str(batch_size_trial)+'-'+str(epochs_trial), accuracy]],
                                                                    columns=['TrialNumber', 'Parameters', 'Accuracy'] ))
    return(SearchResultsData)

def trainiereANN(ANN_type: str):

    HYPERPARAMETER_DICT = {"network_context_differences": [15, 5], "network_no_context_differences": [20, 10], "network_context_caseBase": [5, 50], "network_no_context_caseBase": [20, 10]}

    Predictors=['wohnflaeche', 'grundstueckflaeche', 'anz_zimmer', 'keller', 'baujahr', 'energieeffizienz', 'zustand']
    INPUT_DIM = 7

    if ANN_type == "network_context_differences" or ANN_type == "network_context_caseBase":
        Predictors = Predictors + ["kontextWert"]
        INPUT_DIM = INPUT_DIM + 1

    if ANN_type == "network_context_differences" or ANN_type == "network_no_context_differences":
        TargetVariable=['priceDelta']
        Predictors = Predictors + ["kategorie"]
        INPUT_DIM = INPUT_DIM + 1
        df = pd.read_csv("objects/Differences/differences.csv", sep=';')
        df = df[df['priceDelta'] !=0]
    else:
        TargetVariable=['preis']
        df = pd.read_csv("objects/caseBase.csv", sep=';')
    
    X=df[Predictors].values
    y=df[TargetVariable].values

    PredictorScaler=StandardScaler()
    TargetVarScaler=StandardScaler()
    PredictorScalerFit=PredictorScaler.fit(X)
    TargetVarScalerFit=TargetVarScaler.fit(y)

    X=PredictorScalerFit.transform(X)
    y=TargetVarScalerFit.transform(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    model = Sequential()

    model.add(Dense(units=5, input_dim=INPUT_DIM, kernel_initializer='normal', activation='relu'))
    model.add(Dense(units=5, kernel_initializer='normal', activation='tanh'))
    model.add(Dense(1, kernel_initializer='normal'))

    model.compile(loss='mean_squared_error', optimizer='adam')
    model.fit(X_train, y_train, batch_size = HYPERPARAMETER_DICT[ANN_type][0], epochs = HYPERPARAMETER_DICT[ANN_type][1], verbose=0)

    path = f"objects/Netze/{ANN_type}/"
    model_json = model.to_json()
    with open(path + "model.json", "w") as json_file:
        json_file.write(model_json)

    model.save_weights(path + "weights.h5")
    joblib.dump(PredictorScalerFit, path + "scalerX.save") 
    joblib.dump(TargetVarScalerFit, path + "scalerY.save") 

def getDifferences(x: dict, y: dict, columns: List) -> List:

    werte = []
    for column in columns:
        if column == "kategorie":
            if x[column] == y[column]:
                werte.append(0)
            else:
                werte.append(1)
        elif column == "price1":
            werte.append(x["price"])
        elif column == "price2":
            werte.append(y["price"])
        elif column == "priceDelta":
            werte.append(round(x["price"] - y["price"], 2))
        else:
            werte.append(round(x[column] - y[column], 2))

    return werte
