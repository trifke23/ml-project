"""Shared utility functions for the ML project."""
import os
import sys

import pandas as pd
import numpy as np
from src.exception import CustomException
from src.logger import configure_logger, logging
from pathlib import Path
import dill #dill je biblioteka koja se koristi za serijalizaciju i deserializaciju Python objekata, slično kao pickle, ali sa podrškom za više tipova objekata, uključujući lambda funkcije, generatori i druge složenije strukture podataka.

def save_object(file_path, obj):
    try:
        dir_path = os.path.dirname(file_path) ##dobijamo direktorijum iz putanje do fajla
        os.makedirs(dir_path, exist_ok=True) ##kreiramo direktorijum ako ne postoji

        with open(file_path, 'wb') as file_obj: ##otvaramo fajl u binarnom režimu za pisanje
            dill.dump(obj, file_obj) ##serijalizujemo objekat i zapisujemo ga u fajl
    except Exception as e:
        raise CustomException(e, sys) ##ako dođe do greške prilikom serijalizacije, hvata se izuzetak i baca se CustomException
