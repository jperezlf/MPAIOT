import pandas
import numpy as np
from sklearn.linear_model import Lasso
import pickle
import sys
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt

np.set_printoptions(threshold=sys.maxsize)
pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def calculate_mean_absolute_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mae = mean_absolute_error(y_train, preds)
    print("MAE of Lasso: % f" % (mae))


def calculate_mean_squared_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mse = mean_squared_error(y_train, preds, squared=True)
    print("MSE of Lasso: % f" % (mse))
    rmse = mean_squared_error(y_train, preds, squared=False)
    print("RMSE of Lasso: % f" % (rmse))

def showFeatureImportance(model, feature_names):
    sorted_idx = model.feature_importances_.argsort()
    plt.barh(feature_names[sorted_idx], model.feature_importances_[sorted_idx])
    plt.xlabel("Lasso Feature Importance")
    plt.show()


def run(path_to_project):
    try:
        path_to_project = sys.argv[1]
    except IndexError:
        pass

    data = pandas.read_csv(path_to_project + '/Files/file1.csv', header=0)
    dataset = data.drop_duplicates()

    feature_names = dataset.columns.values
    features_to_delete = np.array(['Temperature'])
    feature_names = np.setdiff1d(feature_names, features_to_delete)

    y_train = dataset.filter(items=['Temperature'])
    x_train = dataset.filter(items=feature_names)
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, shuffle=True, test_size=0.2, random_state=123)

    model = Lasso(selection='random', random_state=42, warm_start=True)
    model.fit(x_train, y_train)

    # try:
    #     showFeatureImportance(model, feature_names)
    # except:
    #     print("El modelo no tiene el atributo FeatureImportance")
    calculate_mean_absolute_error(x_test, y_test, model)
    calculate_mean_squared_error(x_test, y_test, model)

    name = path_to_project + '/algorithms/lasso/model/train.dat'
    pickle.dump(model, open(name, "wb"))

run("")