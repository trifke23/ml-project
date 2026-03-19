"""Shared utility functions for the ML project."""
import os
import sys

import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import configure_logger, logging
from pathlib import Path
import dill #dill je biblioteka koja se koristi za serijalizaciju i deserializaciju Python objekata, slično kao pickle, ali sa podrškom za više tipova objekata, uključujući lambda funkcije, generatori i druge složenije strukture podataka.
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path) ##dobijamo direktorijum iz putanje do fajla
        os.makedirs(dir_path, exist_ok=True) ##kreiramo direktorijum ako ne postoji

        with open(file_path, 'wb') as file_obj: ##otvaramo fajl u binarnom režimu za pisanje
            dill.dump(obj, file_obj) ##serijalizujemo objekat i zapisujemo ga u fajl
    except Exception as e:
        raise CustomException(e, sys) ##ako dođe do greške prilikom serijalizacije, hvata se izuzetak i baca se CustomException

def evaluate_models(X_train, y_train, X_test, y_test, models, param):
    try:
        X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=42) ##delimo podatke na trening i test skupove, gde je test_size 0.2 (20% podataka ide u test skup), a random_state 42 (za reproduktivnost rezultata
        report = {}
        
        for i in range(len(list(models))):
            model = list(models.values())[i] ##uzimamo model iz rečnika modela
            para=param[list(models.keys())[i]] ##uzimamo parametre za taj model iz rečnika parametara
            model.fit(X_train, y_train) ##treniramo model na trening podacima

            gs=GridSearchCV(model, para, cv=5, n_jobs=n_jobs, verbose= verbose, refit =refit) ##kreiramo GridSearchCV objekat koji će tražiti najbolje hiperparametre za model koristeći 5-fold cross-validation
            gs.fit(X_train, y_train) ##treniramo GridSearchCV objekat na trening podacima, što će izvršiti pretragu hiperparametara i pronaći najbolje parametre za model
            
            model.set_params(**gs.best_params_) ##postavljamo najbolje parametre na model koristeći set_params metodu, gde gs.best_params_ sadrži najbolje pronađene parametre nakon pretrage
            model.fit(X_train, y_train) ##ponovo treniramo model sa najboljim parametrima na trening podacima


            y_train_pred = model.predict(X_train) ##predviđamo ciljne vrednosti za trening skup
            y_test_pred = model.predict(X_test) ##predviđamo ciljne vrednosti za test skup
            
            train_model_score = r2_score(y_train, y_train_pred) ##računamo R2 skor za trening skup
            test_model_score = r2_score(y_test, y_test_pred) ##računamo R2 skor za test skup
            
            report[list(models.keys())[i]] = test_model_score ##čuvamo R2 skor za test skup u izveštaju, koristeći ime modela kao ključ

        return report
    except Exception as e:
        raise CustomException(e, sys)