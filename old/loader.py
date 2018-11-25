import os
import csv
import cv2
import numpy as np
import scipy.io as sio
import matplotlib.pyplot as plt

from random import shuffle

annotation_file = "data/anno.csv"
train_source_folder = "data/cars_train/"
test_source_folder = "data/cars_test/"
source_folder = "data/car_ims/"

p_train, p_test = 0.2, 0.8
image_w, image_h = 128, int(128 * 1.5)  # FIXME which is optimal?


class Loader(object):
    class MetaData(object):

        def __init__(self, name, labels, clazz, test):
            self.name = name
            self.labels = labels
            self.clazz = clazz
            self.test = test

    """
    Setting up loader will already determine the train and the test sets,
    shuffle them, but the images will not loaded, so its pretty fast! 
    """
    def __init__(self):
        self.img_metadatas = self.set_up_image_metadatas()
        self.total_size = len(self.img_metadatas)
        self.train_size = int(self.total_size * p_train)
        self.test_size = int(self.total_size * p_test)

        shuffle(self.img_metadatas)
        self.train_set = self.img_metadatas[:self.train_size]
        self.test_set = self.img_metadatas[-self.test_size:]
        print("Loading image meta data ready %d train data, %d test data" % (len(self.train_set), len(self.test_set)))

    def load_train_data(self):
        images = []
        labels = []
        counter = 0
        print("Loading train images..")
        for meta in self.train_set:
            image = cv2.imread(source_folder + meta.name)
            image = cv2.resize(image, (image_h, image_w), interpolation=cv2.INTER_LINEAR)
            image = image.astype(np.float32)
            image = np.multiply(image, 1.0 / 255.0)
            images.append(image)
            labels.append(meta.labels)
            if counter % 1000 == 0 and counter > 0:
                plt.imshow(image)
                print("1000 images are loaded.")

            counter += 1
        images = np.array(images)
        labels = np.array(labels)
        print("%d image loaded" % counter)
        return images, labels

    def load_test_data(self):
        # TODO very similar as above the train
        pass

    def peek_image(self, name):
        im = cv2.imread(source_folder + name)
        print("image is", name)
        plt.imshow(im)

    def set_up_image_metadatas(self):
        datas = []
        with open(annotation_file, 'rt') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            for row in reader:
                datas.append(self.MetaData(row["Image"], [row["x1"], row["y1"], row["x2"], row["y2"]], row["class"],
                                           row["test"]))
        return datas
