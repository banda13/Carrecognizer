import os
import random
import paths
from shutil import copy

i = 0
limit = 100
destination = "/temp/car/"
source = paths.N_SCOUT_IMG_DIR

while i < limit:
    try:
        make_folder = random.choice(os.listdir(source))
        model_folder = random.choice(os.listdir(source + '/' + make_folder))
        copy(source + '/' + make_folder + '/' + model_folder + '/' + random.choice(os.listdir(source + '/' + make_folder + '/' + model_folder)), destination)
        i+=1
    except Exception as e:
        print(e)
