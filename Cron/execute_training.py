import os
from Algorithms.decisiontreeclassifier.model import model_trainer as decisiontreeclassifier
from Algorithms.gaussiannaivebayes.model import model_trainer as gaussiannaivebayes
from Algorithms.lasso.model import model_trainer as lasso
from Algorithms.linearregression.model import model_trainer as linearregression
from Algorithms.linearregressionstatsmodel.model import model_trainer as linearregressionstatsmodel
from Algorithms.logisticregression.model import model_trainer as logisticregression
from Algorithms.randomforest.model import model_trainer as randomforest
from Algorithms.robustregression.model import model_trainer as robustregression
from Algorithms.sgd.model import model_trainer as sgd
from Algorithms.svr.model import model_trainer as svr
from Algorithms.xgboost.model import model_trainer as xgboost

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
