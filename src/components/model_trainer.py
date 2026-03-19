"""Model training component."""

import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import configure_logger, logging
from src.utils import save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            if not logging.getLogger().handlers:
                configure_logger()

            logging.info("Splitting training and test input data")

            x_train, y_train, x_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(random_state=42),
                "Decision Tree": DecisionTreeRegressor(random_state=42),
                "Gradient Boosting": GradientBoostingRegressor(random_state=42),
                "Linear Regression": LinearRegression(),
                "XGBoost": XGBRegressor(objective="reg:squarederror", random_state=42),
                "CatBoost": CatBoostRegressor(verbose=False, random_state=42),
                "AdaBoost": AdaBoostRegressor(random_state=42),
                "KNeighbors": KNeighborsRegressor(),
            }

            best_model_name = None
            best_model = None
            best_model_score = float("-inf")

            for model_name, model in models.items():
                logging.info("Training model: %s", model_name)
                model.fit(x_train, y_train)

                y_pred = model.predict(x_test)
                test_model_score = r2_score(y_test, y_pred)
                logging.info("%s R2 score: %.4f", model_name, test_model_score)

                if test_model_score > best_model_score:
                    best_model_name = model_name
                    best_model = model
                    best_model_score = test_model_score

            if best_model is None:
                raise RuntimeError("No model was trained successfully.")

            logging.info("Best model found: %s with R2 score %.4f", best_model_name, best_model_score)

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            logging.info(
                "Best model saved at %s",
                self.model_trainer_config.trained_model_file_path,
            )

            return best_model_score
        except Exception as e:
            raise CustomException(e, sys)
