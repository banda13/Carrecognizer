from classifiers.cnn3 import Cnn3
from random import sample
import os

paths = ["data/hasznaltauto/bmw/", "data/hasznaltauto/ford/", "data/hasznaltauto/mercedes/","data/hasznaltauto/volkswagen/"]

for path in paths:
    for car in sample(os.listdir(path), 3):
        Cnn3("e7247c4f-88c1-4f0d-bf62-f7850de6d949").predict(path + car, car)

