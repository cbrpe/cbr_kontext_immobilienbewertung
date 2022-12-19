# decision tree for feature importance on a regression problem
from sklearn.datasets import make_regression
from sklearn.tree import DecisionTreeRegressor
# define dataset

import numpy as np
import pandas as pd

# df = pd.read_csv("objects/caseBase_alleAttribute_retrieval_mittelwert - Kopie.csv", sep=";")
# from sklearn.preprocessing import LabelEncoder
# enc = LabelEncoder()
# enc.fit(df['category'])
# df['category'] = enc.transform(df['category'])
# enc.fit(df['terrace'])
# df['terrace'] = enc.transform(df['terrace'])
# enc.fit(df['type'])
# df['type'] = enc.transform(df['type'])

# df.to_csv("objects/caseBase_alleAttribute_retrieval_mittelwert - Kopie.csv", sep=";", index=False)

f = open("objects/casebase_alleAttribute_cart.txt")
f.readline()  # skip the header
data = np.loadtxt(f)

X = data[:, 1:]  # select columns 1 through end
y = data[:, 0]   # select column 0, the stock price

# define the model
model = DecisionTreeRegressor()
# fit the model
model.fit(X, y)
# get importance
importance = model.feature_importances_
# summarize feature importance
for i,v in enumerate(importance):
	print('Feature: %0d, Score: %.5f' % (i,v))