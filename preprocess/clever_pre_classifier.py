import os
import csv
import numpy as np
from shutil import copy, move

from keras.engine.saving import load_model
from keras_preprocessing.image import img_to_array, load_img

import paths


class MyPreClassifier(object):
    dirs = [paths.N_SCOUT_DIR]
    fieldnames = ["image", "label", "percentage"]

    percentage_limit = 0.05

    def __init__(self):
        self.model = load_model(paths.ROOT_DIR + "/model/preclassifier/v1-mymodel.h5")
        print("My pre classifier initialized")

    def classify(self, name, image):
        image = img_to_array(image)
        image = image / 255
        image = np.expand_dims(image, axis=0)
        is_it_a_car_or_its_susan = self.model.predict(image)
        if is_it_a_car_or_its_susan <= 0.01:
            return ('car', is_it_a_car_or_its_susan)
        else:
            return ('notcar', is_it_a_car_or_its_susan)

    def prepare(self):
        for source in self.dirs:
            for make in os.listdir(source):
                if len(os.listdir(source + make)) > 0 and not os.path.isdir(
                        source + make + '/' + os.listdir(source + make)[0]):
                    print("Classifying make: ", make)
                    with open(source + make + '/my_classifications.csv', 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                        writer.writeheader()
                        for image in os.listdir(source + make):
                            try:
                                label = self.classify(image,
                                                      load_img(source + make + "\\" + image, target_size=(150, 150)))
                                writer.writerow({self.fieldnames[0]: image, self.fieldnames[1]: label[0],
                                                 self.fieldnames[2]: label[1]})
                            except Exception as e:
                                print("Error in file: %s. %s" % (image, str(e)))
                else:
                    for model in os.listdir(source + make):
                        if model.endswith('.csv'):
                            continue
                        print("Classifying make: %s model: %s" % (make, model))
                        with open(source + make + '/' + model + '/my_classifications.csv', 'w') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                            writer.writeheader()
                            for image in os.listdir(source + make + '/' + model):
                                try:
                                    if image.endswith('.csv'):
                                        continue
                                    label = self.classify(image,
                                                          load_img(source + make + "/" + model + "/" + image,
                                                                   target_size=(224, 224)))
                                    writer.writerow({self.fieldnames[0]: image, self.fieldnames[1]: label[1],
                                                     self.fieldnames[2]: label[2]})
                                except Exception as e:
                                    print("Error in file: %s. %s" % (image, str(e)))
        print("Classifying done")

    def cleanup(self):
        all_deleted = 0
        for source in self.dirs:
            for category in os.listdir(source):
                if category == 'deleted':
                    continue
                deleted_from_category = 0
                print("Cleaning category: ", category)
                if not os.path.exists(source + "deleted"):
                    os.makedirs(source + "deleted")
                try:
                    with open(source + category + '/my_classifications.csv', 'r') as csvfile:
                        reader = csv.DictReader(csvfile, fieldnames=self.fieldnames)
                        for row in reader:
                            image, cat, percentage = row[self.fieldnames[0]], row[self.fieldnames[1]], row[
                                self.fieldnames[2]]
                            if cat == 'notcar':
                                # os.remove(source + category + "/" + image)
                                try:
                                    move(source + category + '/' + image, source + "deleted/" + image)
                                    deleted_from_category += 1
                                except Exception as e:
                                    print("Skipping file %s. Error: %s " % (image, str(e)))
                except Exception as e:
                    print("Skipping category %s because it do not exists" % category)
                print("%d images deleted from category %s " % (deleted_from_category, category))
                all_deleted += deleted_from_category
