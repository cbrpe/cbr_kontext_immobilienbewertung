# # Reading the cleaned numeric car prices data
# import pandas as pd
# import numpy as np
# from sklearn.preprocessing import LabelEncoder
# from keras.utils import np_utils

# # To remove the scientific notation from numpy arrays
# np.set_printoptions(suppress=True)

# CarPricesDataNumeric=pd.read_csv("objects/differences/differences.csv", sep=';')
# # CarPricesDataNumeric = CarPricesDataNumeric.loc[~(CarPricesDataNumeric==0).all(axis=1)]
# # CarPricesDataNumeric = CarPricesDataNumeric[CarPricesDataNumeric['price'] !=0]
# # CarPricesDataNumeric = CarPricesDataNumeric[CarPricesDataNumeric['price'] <= 100000]
# CarPricesDataNumeric = CarPricesDataNumeric.drop_duplicates(keep=False)
# # print(CarPricesDataNumeric.head())
# # Separate Target Variable and Predictor Variables
# TargetVariable=['Klasse']
# Predictors=['wohnflaeche', 'grundstueckflaeche', 'zimmer', 'category', 'basement', 'year', 'efficiency_rating', 'condition', 'kontextWert']

# X=CarPricesDataNumeric[Predictors].values
# y=CarPricesDataNumeric[TargetVariable].values

# encoder = LabelEncoder()
# encoder.fit(y)
# encoded_Y = encoder.transform(Y)
# # convert integers to dummy variables (i.e. one hot encoded)
# dummy_y = np_utils.to_categorical(encoded_Y)

# ### Sandardization of data ###
# from sklearn.preprocessing import StandardScaler
# PredictorScaler=StandardScaler()
# TargetVarScaler=StandardScaler()

# # Storing the fit object for later reference
# PredictorScalerFit=PredictorScaler.fit(X)
# TargetVarScalerFit=TargetVarScaler.fit(y)

# # Generating the standardized values of X and y
# X=PredictorScalerFit.transform(X)
# y=TargetVarScalerFit.transform(y)

# # Split the data into training and testing set
# from sklearn.model_selection import train_test_split
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# # Quick sanity check with the shapes of Training and testing datasets
# print(X_train.shape)
# print(y_train.shape)
# print(X_test.shape)
# print(y_test.shape)

# # importing the libraries
# from keras.models import Sequential
# from keras.layers import Dense
# from keras import optimizers

# # create ANN model
# model = Sequential()

# # Defining the Input layer and FIRST hidden layer, both are same!
# model.add(Dense(8, input_dim=8, activation='relu'))


# # Defining the Second layer of the model
# # after the first layer we don't have to specify input_dim as keras configure it automatically

# model.add(Dense(3, activation='softmax'))


# model.compile(loss="categorical_crossentropy", optimizer= "adam", metrics=['accuracy'])

# # Fitting the ANN to the Training set
# model.fit(X_train, y_train ,batch_size = 10, epochs = 5000, verbose=1)

# # Generating Predictions on testing data
# Predictions=model.predict(X_test)

# # Scaling the predicted Price data back to original price scale
# Predictions=TargetVarScalerFit.inverse_transform(Predictions)
# # for i in range(len(Predictions)):
# #     if Predictions[i] < 0.5:
# #         Predictions[i] = 0
# #     else:
# #         Predictions[i] = 1

# # Scaling the y_test Price data back to original price scale
# y_test_orig=TargetVarScalerFit.inverse_transform(y_test)

# # Scaling the test data back to original scale
# Test_Data=PredictorScalerFit.inverse_transform(X_test)

# TestingData=pd.DataFrame(data=Test_Data, columns=Predictors)
# TestingData['Price']=y_test_orig
# TestingData['PredictedPrice']=Predictions

# # richtig = 0
# # for i in range(len(Predictions)):
# #     if Predictions[i] == y_test_orig[i]:
# #         richtig += 1

# # print(richtig/len(Predictions))

# # Computing the absolute percent error
# APE=abs(TestingData['Price']-TestingData['PredictedPrice'])
# TestingData['APE']=APE

# print('MAE:', np.mean(APE))
# TestingData.to_csv("test.csv", sep=";")

# import pandas as pd
# from keras.models import Sequential
# from keras.layers import Dense
# from keras.wrappers.scikit_learn import KerasClassifier
# from keras.utils import np_utils
# from sklearn.model_selection import cross_val_score
# from sklearn.model_selection import KFold
# from sklearn.preprocessing import LabelEncoder
# from sklearn.pipeline import Pipeline
# # load dataset
# dataframe=pd.read_csv("objects/differences/differences.csv", sep=';')


# TargetVariable=['Klasse']
# Predictors=['wohnflaeche', 'grundstueckflaeche', 'zimmer', 'category', 'basement', 'year', 'efficiency_rating', 'condition']

# X=dataframe[Predictors].values
# y=dataframe[TargetVariable].values

# # encode class values as integers
# encoder = LabelEncoder()
# encoder.fit(y)
# encoded_Y = encoder.transform(y)
# # convert integers to dummy variables (i.e. one hot encoded)
# dummy_y = np_utils.to_categorical(encoded_Y)

# # define baseline model
# def baseline_model():
# 	# create model
# 	model = Sequential()
# 	model.add(Dense(10, input_dim=8, activation='relu'))
# 	model.add(Dense(7, activation='softmax'))
# 	# Compile model
# 	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# 	return model

# estimator = KerasClassifier(build_fn=baseline_model, epochs=50, batch_size=5, verbose=1)
# kfold = KFold(n_splits=2, shuffle=True)
# results = cross_val_score(estimator, X, dummy_y, cv=kfold)
# print("Baseline: %.2f%% (%.2f%%)" % (results.mean()*100, results.std()*100))

# import pandas as pd
# from keras.models import Sequential
# from keras.layers import Dense
# from sklearn.preprocessing import LabelEncoder
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split
# from keras.utils import np_utils

# dataframe=pd.read_csv("objects/differences/differences.csv", sep=';')


# TargetVariable=['Klasse']
# Predictors=['wohnflaeche', 'grundstueckflaeche', 'zimmer', 'category', 'basement', 'year', 'efficiency_rating', 'condition', 'kontextWert']

# X=dataframe[Predictors].values
# y=dataframe[TargetVariable].values

# # encode class values as integers
# encoder = LabelEncoder()
# encoder.fit(y)
# encoded_Y = encoder.transform(y)
# dummy_y = np_utils.to_categorical(encoded_Y)

# model = Sequential()
# model.add(Dense(10, input_dim=9, activation='relu'))
# model.add(Dense(7, activation='softmax'))

# model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# PredictorScaler=StandardScaler()
# PredictorScalerFit=PredictorScaler.fit(X)
# X=PredictorScalerFit.transform(X)

# X_train, X_test, y_train, y_test = train_test_split(X, dummy_y, test_size=0.3, random_state=42)

# model.fit(X_train, y_train ,batch_size = 10, epochs = 20, verbose=1)