import pandas
import json
import numpy as np
import sys
sys.path.append(".")
from multiisotonicregression import MultiIsotonicRegressor

np.set_printoptions(threshold=sys.maxsize)
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def mean_absolute_error(y_true, y_pred):
    """Calculates MAE given y_true and y_pred"""
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs(y_true - y_pred))


# load data
data = pandas.read_csv('train.csv', header=0)
dataset = data.drop_duplicates()
feature_names = dataset.columns.values

features_to_delete = np.array(['value'])
feature_names = np.setdiff1d(feature_names, features_to_delete)

Y_train = dataset.filter(items=['value'])
X_train = dataset.filter(items=feature_names)

iso_reg = MultiIsotonicRegressor()
iso_reg.fit(X_train, Y_train.values.ravel())

data = json.loads(sys.argv[-1])

dataset = pandas.DataFrame(data=data, dtype=float)

preds = iso_reg.predict(dataset[0:])

preds = np.array(preds).tolist()

print(json.dumps(preds))

