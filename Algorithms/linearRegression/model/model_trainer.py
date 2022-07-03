import pandas
import numpy as np
from sklearn.linear_model import LinearRegression
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
    print("MAE of Linear Regression: % f" % (mae))


def calculate_mean_squared_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mse = mean_squared_error(y_train, preds, squared=True)
    print("MSE of Linear Regression: % f" % (mse))
    rmse = mean_squared_error(y_train, preds, squared=False)
    print("RMSE of Linear Regression: % f" % (rmse))


def tunningParameters(x_train, y_train):
    from sklearn.model_selection import RandomizedSearchCV

    fit_intercept = [True, False]
    normalize = [True, False]
    copy_X = [True, False]
    n_jobs = [int(x) for x in np.linspace(1, 100, num=1)]

    # Create the random grid
    random_grid = {'fit_intercept': fit_intercept,
                   'normalize': normalize,
                   'copy_X': copy_X,
                   'n_jobs': n_jobs}

    print(random_grid)

    # Use the random grid to search for best hyperparameters
    # First create the base model to tune
    model = LinearRegression()
    # Random search of parameters, using 3 fold cross validation,
    # search across 100 different combinations, and use all available cores
    rf_random = RandomizedSearchCV(estimator=model, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                   random_state=42, n_jobs=-1)
    print("\n")
    # Fit the random search model
    rf_random.fit(x_train, y_train.values.ravel())

    print("Best Parameters: \n")
    print(rf_random.best_params_)

def showFeatureImportance(model, feature_names):
    sorted_idx = model.feature_importances_.argsort()
    plt.barh(feature_names[sorted_idx], model.feature_importances_[sorted_idx])
    plt.xlabel("Linear Regression Feature Importance")
    plt.show()


def run(path_to_project):
    try:
        path_to_project = sys.argv[1]
    except IndexError:
        pass

    data = pandas.read_csv(path_to_project + '/Files/Dataset.csv', header=0)

    dataset = data.drop_duplicates()
    feature_names = dataset.columns.values

    features_to_delete = np.array(['Temperature'])
    feature_names = np.setdiff1d(feature_names, features_to_delete)

    y_train = dataset.filter(items=['Temperature'])
    x_train = dataset.filter(items=feature_names)
    x_train, x_test, y_train, y_test = train_test_split(x_train, y_train, shuffle=True, test_size=0.2, random_state=123)

    model = LinearRegression()
    model.fit(x_train, y_train)

    # try:
    #     showFeatureImportance(model, feature_names)
    # except:
    #     print("El modelo no tiene el atributo FeatureImportance")
    calculate_mean_absolute_error(x_test, y_test, model)
    calculate_mean_squared_error(x_test, y_test, model)

    name = path_to_project + '/algorithms/linearRegression/model/train.dat'
    pickle.dump(model, open(name, "wb"))


run("")
