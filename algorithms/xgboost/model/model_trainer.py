import pandas
import xgboost as xgb
import numpy as np
from sklearn.model_selection import train_test_split
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
    data = pandas.read_csv(path_to_project + '/crones_datos/file.csv', header=0)
else:
    data = pandas.read_csv('training.csv', header=0)
dataset = data.drop_duplicates()
feature_names = dataset.columns.values

features_to_delete = np.array(['Temperature'])
feature_names = np.setdiff1d(feature_names, features_to_delete)

Y_train = dataset.filter(items=['Temperature'])
X_train = dataset.filter(items=feature_names)

X_train, X_test, Y_train, Y_test = train_test_split(X_train, Y_train, shuffle=True, test_size=0.2, random_state=123)

eval_set = [(X_train, Y_train), (X_test, Y_test)]

xg_reg = xgb.XGBRegressor(objective='reg:squarederror', min_child_weight=0, colsample_bytree=0.8, subsample=0.8,
                          learning_rate=0.1, max_depth=9, n_estimators=1000)

# xg_reg.fit(X_train, Y_train, eval_set=eval_set, eval_metric="rmse", early_stopping_rounds=20)
xg_reg.fit(X_train, Y_train, eval_metric="rmse")

preds = xg_reg.predict(X_test, ntree_limit=0)

if sys.argv[1]:
    name = path_to_project + '/algorithms/xgboost/model/train.dat'
else:
    name = 'train.dat'
pickle.dump(xg_reg, open(name, "wb"))
