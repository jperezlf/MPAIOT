import pandas
import numpy as np
from sklearn.tree import DecisionTreeRegressor
import pickle
import sys
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt


def calculate_mean_absolute_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mae = mean_absolute_error(y_train, preds)
    print("MAE of Decision Tree Regressor: % f" % (mae))


def calculate_mean_squared_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mse = mean_squared_error(y_train, preds, squared=True)
    print("MSE of Decision Tree Regressor: % f" % (mse))
    rmse = mean_squared_error(y_train, preds, squared=False)
    print("RMSE of Decision Tree Regressor: % f" % (rmse))


def showFeatureImportance(model, feature_names):
    sorted_idx = model.feature_importances_.argsort()
    plt.barh(feature_names[sorted_idx], model.feature_importances_[sorted_idx])
    plt.xlabel("Decision Tree Regressor Feature Importance")
    plt.show()


def calculate_value_error(x_train, y_train, model):
    pred = model.predict(x_train)
    i = 0
    for row in y_train['Temperature'].values:
        # print(abs(pred[i] - row))
        if (pred[i] - row) * (pred[i] - row) > 100:
            print((pred[i] - row) * (pred[i] - row))
            print(pred[i])
            print(row)
            print("")
        i = i + 1


def run(path_to_project):
    try:
        path_to_project = sys.argv[1]
    except IndexError:
        pass
    np.set_printoptions(threshold=sys.maxsize)
    pandas.set_option('display.max_rows', 800)
    pandas.set_option('display.max_columns', 500)
    pandas.set_option('display.width', 1000)
    data = pandas.read_csv(path_to_project + '/Files/Dataset.csv', header=0)
    dataset = data.drop_duplicates()

    feature_names = dataset.columns.values
    features_to_delete = np.array(['Temperature'])
    feature_names = np.setdiff1d(feature_names, features_to_delete)

    y_train = dataset.filter(items=['Temperature']).astype('int64')
    x_train = dataset.filter(items=feature_names).astype('int64')
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, shuffle=True, test_size=0.2, random_state=123)

    model = DecisionTreeRegressor()
    model.fit(x_train, y_train)

    # try:
    #     showFeatureImportance(model, feature_names)
    # except:
    #     print("El modelo no tiene el atributo FeatureImportance")
    calculate_mean_absolute_error(x_test, y_test, model)
    calculate_mean_squared_error(x_test, y_test, model)
    calculate_value_error(x_test, y_test, model)

    name = path_to_project + '/algorithms/decisionTreeRegressor/model/train.dat'
    pickle.dump(model, open(name, "wb"))


run("")
