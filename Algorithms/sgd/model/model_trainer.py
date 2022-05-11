import pandas
import numpy as np
from sklearn.linear_model import SGDRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
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


def run(path_to_project):
    # load data
    try:
        path_to_project = sys.argv[1]
    except IndexError:
        pass

    data = pandas.read_csv(path_to_project + '/crones/file.csv', header=0)
    dataset = data.drop_duplicates()
    feature_names = dataset.columns.values

    features_to_delete = np.array(['Temperature'])
    feature_names = np.setdiff1d(feature_names, features_to_delete)

    Y_train = dataset.filter(items=['Temperature'])
    X_train = dataset.filter(items=feature_names)

    reg = make_pipeline(StandardScaler(),
                        SGDRegressor(max_iter=1000, tol=1e-3))
    reg.fit(X_train, Y_train.values.ravel())

    name = path_to_project + '/algorithms/sgd/model/train.dat'

    pickle.dump(reg, open(name, "wb"))
