import csv
import os
import random

from shutil import copy, copyfile
from keras.preprocessing.image import ImageDataGenerator

"""
Separates train and test data and copies them to the folder, 
that match their category
"""
def sort_data_to_folders(train_p, test_p):
    root = "data/car_ims/"
    train_root = "data/train/"
    test_root =  "data/test/"
    annotation_file = "data/anno.csv"

    with open(annotation_file, 'rt') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        data = {}
        for row in reader:
            data[row["Image"]] = row["class"]
        keys = list(data.keys())
        train_size = int(len(keys) * train_p)
        test_size = int(len(keys) * test_p)
        random.shuffle(keys)
        for name in keys[:train_size]:
            directory = train_root + data[name] + "/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            copyfile(root + name, directory)
        print("sorting train images to directories done!")

        for name in keys[-test_size:]:
            directory = test_root + data[name] + "/"
            if not os.path.exists(directory):
                os.makedirs(directory)
            copyfile(root + name, directory)
        print("sorting test images to directories done!")

        image_gen = ImageDataGenerator(rescale=1.0 / 255)
        train_iterator = image_gen.flow_from_directory("data/car_ims/",
                                                       batch_size=128,
                                                       target_size=(224, 224))

sort_data_to_folders(.8, .2)
