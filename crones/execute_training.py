import os
from algorithms.decisiontreeclassifier.model import model_trainer as decisiontreeclassifier
from algorithms.gaussiannaivebayes.model import model_trainer as gaussiannaivebayes
from algorithms.lasso.model import model_trainer as lasso
from algorithms.linearregression.model import model_trainer as linearregression
from algorithms.linearregressionstatsmodel.model import model_trainer as linearregressionstatsmodel
from algorithms.logisticregression.model import model_trainer as logisticregression
from algorithms.randomforest.model import model_trainer as randomforest
from algorithms.robustregression.model import model_trainer as robustregression
from algorithms.sgd.model import model_trainer as sgd
from algorithms.svr.model import model_trainer as svr
from algorithms.xgboost.model import model_trainer as xgboost

PROJECT_PATH = os.environ.get("PROJECT_PATH")

decisiontreeclassifier.run(PROJECT_PATH)
print("Entrenando algoritmo Decision Tree Classifier")

gaussiannaivebayes.run(PROJECT_PATH)
print("Entrenando algoritmo Gaussian Naive Bayes")

lasso.run(PROJECT_PATH)
print("Entrenando algoritmo LASSO Regression")

linearregression.run(PROJECT_PATH)
print("Entrenando algoritmo Linear Regression Múltiple")

linearregressionstatsmodel.run(PROJECT_PATH)
print("Entrenando algoritmo Linear Regression Múltiple Stats Model")

logisticregression.run(PROJECT_PATH)
print("Entrenando algoritmo Logistic Regression")

randomforest.run(PROJECT_PATH)
print("Entrenando algoritmo Ramdom Forest")

robustregression.run(PROJECT_PATH)
print("Entrenando algoritmo Robust Regression RANSAC")

sgd.run(PROJECT_PATH)
print("Entrenando algoritmo Stochastic Gradient Descent")

svr.run(PROJECT_PATH)
print("Entrenando algoritmo Suport Vector Regression")

xgboost.run(PROJECT_PATH)
print("Entrenando algoritmo entrenamiento XGBoost")
