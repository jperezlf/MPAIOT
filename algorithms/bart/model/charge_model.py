import pandas
import numpy as np
from sklearn import preprocessing
from xbart import XBART
import sys
import json

np.set_printoptions(threshold=sys.maxsize)
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def mean_absolute_error(y_true, y_pred):
    """Calculates MAE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))


# load data
data = pandas.read_csv('training.csv', header=0)
dataset = data.drop_duplicates()
feature_names = dataset.columns.values

features_to_delete = np.array(['value'])
feature_names = np.setdiff1d(feature_names, features_to_delete)

Y_train = dataset.filter(items=['value'])
X_train = dataset.filter(items=feature_names)

X_train = preprocessing.scale(X_train)

xbt = XBART(max_depth_num=1000)
xbt.fit(X_train, Y_train.values.ravel())

data = json.loads(sys.argv[-1])

dataset = pandas.DataFrame(data=data, dtype=float)

preds = xbt.predict(dataset[0:])

preds = np.array(preds).tolist()

print(json.dumps(preds))
