# this can be used to create data for the clusterer
import os
import csv
import paths
import random
from shutil import copy

from dao.services.scout_service import lookup_for_id

sample_size = 100

i = 0
destination = "../temp/"
source = paths.N_SCOUT_DIR

with open(destination + 'props.csv', 'w', encoding='utf-8-sig') as file:
    writer = csv.writer(file, delimiter=';', quotechar='"', lineterminator = '\n')
    writer.writerow(['id', 'make', 'model', 'body'])
    while i < sample_size:
        try:
            makemodel_folder = random.choice(os.listdir(source))
            image = random.choice(os.listdir(source + '/' + makemodel_folder))
            image_data = lookup_for_id(image.split('_')[2])
            if image_data is not None:
                writer.writerow([image, image_data.make, image_data.model, image_data.body])
                copy(source + '/' + makemodel_folder + '/' + image, destination)
                i += 1
        except Exception as e:
            print(e)