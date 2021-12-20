import pandas
import numpy as np
import statsmodels.api as sm
import pickle
import sys

np.set_printoptions(threshold=sys.maxsize)
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def mean_absolute_error(y_true, y_pred):
    """Calculates MAE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))


# load data
if sys.argv[1]:
    path_to_project = sys.argv[1]
    data = pandas.read_csv(path_to_project + '/training/training.csv', header=0)
else:
    data = pandas.read_csv('training.csv', header=0)
dataset = data.drop_duplicates()
feature_names = dataset.columns.values

features_to_delete = np.array(['value'])
feature_names = np.setdiff1d(feature_names, features_to_delete)

Y_train = dataset.filter(items=['value'])
X_train = dataset.filter(items=feature_names)

model = sm.OLS(Y_train, X_train)

model = model.fit()

name = path_to_project + '/algorithms/linearregressionstatsmodel/model/train.dat'
pickle.dump(model, open(name, "wb"))
