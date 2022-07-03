import pandas
import numpy as np
import pickle
import sys
from sklearn.linear_model import RANSACRegressor, LinearRegression
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
    print("MAE of Robust Regression: % f" % (mae))


def calculate_mean_squared_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mse = mean_squared_error(y_train, preds, squared=True)
    print("MSE of Robust Regression: % f" % (mse))
    rmse = mean_squared_error(y_train, preds, squared=False)
    print("RMSE of Robust Regression: % f" % (rmse))


def tunningParameters(x_train, y_train):
    from sklearn.model_selection import RandomizedSearchCV

    # base_estimator = LinearRegression()
    min_samples = [2, 5, 10, 15, 20, 100, 200, 500, 1000]
    max_trials = [int(x) for x in np.linspace(start=10, stop=500, num=10)]
    loss = ['absolute_loss', 'squared_loss']
    random_state = [None, 42]

    # Create the random grid
    random_grid = {'min_samples': min_samples,
                   'max_trials': max_trials,
                   'loss': loss,
                   'random_state': random_state}
    print(random_grid)

    # Use the random grid to search for best hyperparameters
    # First create the base model to tune
    model = RANSACRegressor(base_estimator=LinearRegression())
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
    plt.xlabel("RANSAC Feature Importance")
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

    model = RANSACRegressor(base_estimator=LinearRegression(), max_trials=500, random_state=42, min_samples=100, loss='absolute_loss')
    model.fit(x_train, y_train)

    # try:
    #     showFeatureImportance(model, feature_names)
    # except:
    #     print("El modelo no tiene el atributo FeatureImportance")
    calculate_mean_absolute_error(x_test, y_test, model)
    calculate_mean_squared_error(x_test, y_test, model)

    name = path_to_project + '/algorithms/robustRegression/model/train.dat'
    pickle.dump(model, open(name, "wb"))


run("")
