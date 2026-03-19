"""Data ingestion component placeholder. Gledamo odakle dolaze podaci i kako ih učitavamo u naš pipeline.
    READ DATA, SPLIT DATA"""

import os 
import sys
from pathlib import Path

if __package__ is None or __package__ == "":
    sys.path.append(str(Path(__file__).resolve().parents[2]))

from src.exception import CustomException
from src.logger import configure_logger, logging
import pandas as pd 
from sklearn.model_selection import train_test_split
from dataclasses import dataclass ##dataclass is a decorator that automatically generates special methods like __init__() and __repr__() for classes, making it easier to create classes that primarily store data.
from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from src.components.model_trainer import ModelTrainerConfig

@dataclass ##koristi se za označavanje klase kao dataclass, što znači da će se automatski generisati metode poput __init__() i __repr__() na osnovu definisanih atributa klase.
class DataIngestionConfig:  ##sve sto je potrebno za konfiguraciju data ingestiona, npr. putanje do fajlova, parametri za splitovanje itd.
    train_data_path: str = os.path.join('artifacts', 'train.csv') ##putanja do train podataka artifacts je folder gde cuvamo sve nase fajlove, a train.csv je fajl gde cuvamo train podatke
    test_data_path: str = os.path.join('artifacts', 'test.csv') ##putanja do test podataka
    raw_data_path: str = os.path.join('artifacts', 'data.csv') ##putanja do raw podataka

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig() ##kreiramo instancu DataIngestionConfig klase, ova tri path ce tu biti sacuvana

    def initiate_data_ingestion(self): 
        if not logging.getLogger().handlers:
            configure_logger()

        logging.info("Data Ingestion method starts") ## ovde mozemo da pisemo odakle da povlaci podatke a u util mozemo da pisemo vezu
        try:
            df = pd.read_csv(os.path.join('notebook/data', 'stud.csv')) ##učitavamo raw podatke iz csv fajla u pandas DataFrame
            logging.info("Dataset read as pandas dataframe")

            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path), exist_ok=True) ##kreiramo direktorijum za train podatke ako ne postoji
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True) ##čuvamo raw podatke u csv fajl

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42) ##splitujemo podatke na train i test setove

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True) ##čuvamo train set u csv fajl
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True) ##čuvamo test set u csv fajl

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e, sys)
        
if __name__ == "__main__":
    obj = DataIngestion() ##kreiramo instancu DataIngestion klase
    train_data, test_data = obj.initiate_data_ingestion() ##pozivamo metodu za data ingestion

    data_transformation = DataTransformation() ##kreiramo instancu DataTransformation klase
    train_arr, test_arr, _ = data_transformation.initiate_data_transformation(train_data, test_data) ##pozivamo metodu za data transformation, prosledjujemo putanje do train i test podataka

    model_trainer = ModelTrainer()
    r2 = model_trainer.initiate_model_trainer(train_arr, test_arr)
    print(f"Best model R2 score: {r2:.4f}")
