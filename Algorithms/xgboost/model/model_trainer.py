import pandas
import xgboost as xgb
import numpy as np
import pickle
import sys
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split

np.set_printoptions(threshold=sys.maxsize)
pandas.set_option('display.max_rows', 3000)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def calculate_mean_absolute_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mae = mean_absolute_error(y_train, preds)
    print("MAE of XGBoost: % f" % (mae))


def calculate_mean_squared_error(x_train, y_train, model):
    preds = model.predict(x_train)
    mse = mean_squared_error(y_train, preds, squared=True)
    print("MSE of XGBoost: % f" % (mse))
    rmse = mean_squared_error(y_train, preds, squared=False)
    print("RMSE of XGBoost: % f" % (rmse))


def showFeatureImportance(model, feature_names):
    sorted_idx = model.feature_importances_.argsort()
    plt.barh(feature_names[sorted_idx], model.feature_importances_[sorted_idx])
    plt.xlabel("XGboost Feature Importance")
    plt.show()


def calculate_value_error(x_train, y_train, model):
    pred = model.predict(x_train)
    i = 0
    for row in y_train['Temperature'].values:
        #print(abs(pred[i] - row))
        if abs(pred[i] - row) > 5:
            print(abs(pred[i] - row))
            print(pred[i])
            print(row)
        i = i + 1


def tunningParameters(x_train, y_train):
    from sklearn.model_selection import RandomizedSearchCV

    # Create the random grid
    random_grid = {'max_depth': [6, 10, 15, 20],
                   'learning_rate': [0.001, 0.01, 0.1, 0.2, 0, 3],
                   'subsample': [0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                   'colsample_bytree': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                   'colsample_bylevel': [0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
                   'min_child_weight': [0.5, 1.0, 3.0, 5.0, 7.0, 10.0],
                   'gamma': [0, 0.25, 0.5, 1.0],
                   'reg_lambda': [0.1, 1.0, 5.0, 10.0, 50.0, 100.0],
                   'n_estimators': [int(x) for x in np.linspace(start=200, stop=2000, num=10)]}

    print(random_grid)

    # Use the random grid to search for best hyperparameters
    # First create the base model to tune
    model = xgb.XGBRegressor()
    # Random search of parameters, using 3 fold cross validation,
    # search across 100 different combinations, and use all available cores
    xgb_random = RandomizedSearchCV(estimator=model, param_distributions=random_grid, n_iter=100, cv=3, verbose=2,
                                    random_state=42, n_jobs=-1)
    print("\n")
    # Fit the random search model
    xgb_random.fit(x_train, y_train)

    print("Best Parameters: \n")
    print(xgb_random.best_params_)


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

    model = xgb.XGBRegressor(objective='reg:squarederror', subsample=1.0, reg_lambda=1.0,
                             n_estimators=100, min_child_weight=0.5, max_depth=6, learning_rate=0.2, gamma=0.5,
                             colsample_bytree=1.0, colsample_bylevel=0.7)

    model.fit(x_train, y_train)

    # try:
    #     showFeatureImportance(model, feature_names)
    # except:
    #     print("El modelo no tiene el atributo FeatureImportance")
    calculate_mean_absolute_error(x_test, y_test, model)
    calculate_mean_squared_error(x_test, y_test, model)
    #calculate_value_error(x_test, y_test, model)

    name = path_to_project + '/algorithms/xgboost/model/train.dat'
    pickle.dump(model, open(name, "wb"))


run("")
