import sys
from Algorithms.decisionTreeRegressor.model import model_trainer as decisiontreeregressor
from Algorithms.ridge.model import model_trainer as ridge
from Algorithms.lasso.model import model_trainer as lasso
from Algorithms.linearRegression.model import model_trainer as linearregression
from Algorithms.elasticNet.model import model_trainer as elasticNet
from Algorithms.randomForest.model import model_trainer as randomforest
from Algorithms.robustRegression.model import model_trainer as robustregression
from Algorithms.sgd.model import model_trainer as sgd
from Algorithms.svr.model import model_trainer as svr
from Algorithms.xgboost.model import model_trainer as xgboost

PROJECT_PATH = sys.argv[1]

decisiontreeregressor.run(PROJECT_PATH)
print("Entrenando algoritmo Decision Tree Regressor\n")

ridge.run(PROJECT_PATH)
print("Entrenando algoritmo Ridge\n")

lasso.run(PROJECT_PATH)
print("Entrenando algoritmo LASSO Regression\n")

linearregression.run(PROJECT_PATH)
print("Entrenando algoritmo Linear Regression\n")

elasticNet.run(PROJECT_PATH)
print("Entrenando algoritmo Elastic Net\n")

randomforest.run(PROJECT_PATH)
print("Entrenando algoritmo Ramdom Forest\n")

robustregression.run(PROJECT_PATH)
print("Entrenando algoritmo Robust Regression RANSAC\n")

sgd.run(PROJECT_PATH)
print("Entrenando algoritmo Stochastic Gradient Descent\n")

svr.run(PROJECT_PATH)
print("Entrenando algoritmo Suport Vector Regression\n")

xgboost.run(PROJECT_PATH)
print("Entrenando algoritmo entrenamiento XGBoost\n")
