import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor,
    GradientBoostingRegressor,
    RandomForestRegressor,
)
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from sklearn.model_selection import GridSearchCV

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Split training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "XGBRegressor": XGBRegressor(),
                "CatBoost Regressor": CatBoostRegressor(verbose=False),
                "AdaBoost Regressor": AdaBoostRegressor(),
            }

            params = {
                "Decision Tree": {
                    "criterion": ["squared_error", "friedman_mse", "absolute_error", "poisson"],
                },
                "Random Forest": {
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Gradient Boosting": {
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "subsample": [0.6, 0.7, 0.75, 0.8, 0.85, 0.9],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "Linear Regression": {},
                "XGBRegressor": {
                    "learning_rate": [0.1, 0.01, 0.05, 0.001],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
                "CatBoost Regressor": {
                    "depth": [6, 8, 10],
                    "learning_rate": [0.01, 0.05, 0.1],
                    "iterations": [30, 50, 100],
                },
                "AdaBoost Regressor": {
                    "learning_rate": [0.1, 0.01, 0.5, 0.001],
                    "n_estimators": [8, 16, 32, 64, 128, 256],
                },
            }

            best_model_score = -1
            best_model_name = None
            best_model = None

            for name, model in models.items():
                logging.info(f"Training {name}...")
                param_grid = params[name]
                if param_grid:
                    gs = GridSearchCV(model, param_grid, cv=3, scoring="r2", n_jobs=-1)
                    gs.fit(X_train, y_train)
                    final_model = gs.best_estimator_
                else:
                    model.fit(X_train, y_train)
                    final_model = model

                y_pred = final_model.predict(X_test)
                score = r2_score(y_test, y_pred)

                logging.info(f"{name} R2 score: {score}")

                if score > best_model_score:
                    best_model_score = score
                    best_model_name = name
                    best_model = final_model

            if best_model_score < 0.6:
                raise CustomException("No suitable model found with acceptable R2 score")

            logging.info(f"Best model: {best_model_name} with R2 score: {best_model_score}")

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            return best_model_score

        except Exception as e:
            raise CustomException(e, sys)



# import os
# import sys
# from dataclasses import dataclass

# from catboost import CatBoostRegressor
# from sklearn.ensemble import (
#     AdaBoostRegressor,
#     GradientBoostingRegressor,
#     RandomForestRegressor,
# )
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import r2_score
# from sklearn.neighbors import KNeighborsRegressor
# from sklearn.tree import DecisionTreeRegressor
# from xgboost import XGBRegressor

# from src.exception import CustomException
# from src.logger import logging

# from src.utils import save_object,evaluate_models

# @dataclass
# class ModelTrainerConfig:
#     trained_model_file_path=os.path.join("artifacts","model.pkl")

# class ModelTrainer:
#     def __init__(self):
#         self.model_trainer_config=ModelTrainerConfig()


#     def initiate_model_trainer(self,train_array,test_array):
#         try:
#             logging.info("Split training and test input data")
#             X_train,y_train,X_test,y_test=(
#                 train_array[:,:-1],
#                 train_array[:,-1],
#                 test_array[:,:-1],
#                 test_array[:,-1]
#             )
#             models = {
#                 "Random Forest": RandomForestRegressor(),
#                 "Decision Tree": DecisionTreeRegressor(),
#                 "Gradient Boosting": GradientBoostingRegressor(),
#                 "Linear Regression": LinearRegression(),
#                 "XGBRegressor": XGBRegressor(),
#                 "CatBoosting Regressor": CatBoostRegressor(verbose=False),
#                 "AdaBoost Regressor": AdaBoostRegressor(),
#             }
#             params={
#                 "Decision Tree": {
#                     'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
#                     # 'splitter':['best','random'],
#                     # 'max_features':['sqrt','log2'],
#                 },
#                 "Random Forest":{
#                     # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
#                     # 'max_features':['sqrt','log2',None],
#                     'n_estimators': [8,16,32,64,128,256]
#                 },
#                 "Gradient Boosting":{
#                     # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
#                     'learning_rate':[.1,.01,.05,.001],
#                     'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
#                     # 'criterion':['squared_error', 'friedman_mse'],
#                     # 'max_features':['auto','sqrt','log2'],
#                     'n_estimators': [8,16,32,64,128,256]
#                 },
#                 "Linear Regression":{},
#                 "XGBRegressor":{
#                     'learning_rate':[.1,.01,.05,.001],
#                     'n_estimators': [8,16,32,64,128,256]
#                 },
#                 "CatBoosting Regressor":{
#                     'depth': [6,8,10],
#                     'learning_rate': [0.01, 0.05, 0.1],
#                     'iterations': [30, 50, 100]
#                 },
#                 "AdaBoost Regressor":{
#                     'learning_rate':[.1,.01,0.5,.001],
#                     # 'loss':['linear','square','exponential'],
#                     'n_estimators': [8,16,32,64,128,256]
#                 }
                
#             }

#             model_report:dict=evaluate_models(X_train=X_train,y_train=y_train,X_test=X_test,y_test=y_test,
#                                              models=models,param=params)
            
#             ## To get best model score from dict
#             best_model_score = max(sorted(model_report.values()))

#             ## To get best model name from dict

#             best_model_name = list(model_report.keys())[
#                 list(model_report.values()).index(best_model_score)
#             ]
#             best_model = models[best_model_name]

#             if best_model_score<0.6:
#                 raise CustomException("No best model found")
#             logging.info(f"Best found model on both training and testing dataset")

#             save_object(
#                 file_path=self.model_trainer_config.trained_model_file_path,
#                 obj=best_model
#             )

#             predicted=best_model.predict(X_test)

#             r2_square = r2_score(y_test, predicted)
#             return r2_square
            



            
#         except Exception as e:
#             raise CustomException(e,sys)



























































































































