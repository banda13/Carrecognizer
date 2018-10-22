import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.optimizers import RMSprop
from keras import applications, Input, Model
from keras.utils.np_utils import to_categorical
import matplotlib.pyplot as plt
import math
import cv2
import uuid
import time
import json
from PIL import ImageFile
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io
from keras.models import load_model
from keras import backend as K
import os.path as osp
import os
import tensorflow as tf


class Cnn4(object):

    train_dir = "data/train/"
    test_dir = "data/test/"
    img_width, img_height = 224, 224

    def __init__(self, name="test"):
        self.batch_size = 32
        self.name = name
        self.model_path = "model/" + name + ".h5"
        self.class_indices_path = "model/" + name + "-classes.npy"

    def build_model(self, num_classes):
        print("Building model for %d classes" % num_classes)
        input_tensor = Input(shape=(self.img_width, self.img_height, 3))
        model = applications.VGG16(include_top=False, weights='imagenet', input_tensor=input_tensor)

        model_output = model(input_tensor)

        top_model = Flatten()(model_output)
        top_model = Dense(256, activation='relu')(top_model)
        top_model = Dropout(0.5)(top_model)
        top_model = Dense(num_classes, activation='softmax')(top_model)

        new_model = Model(input=input_tensor, output=top_model)

        new_model.compile(optimizer='SGD',
                           loss='categorical_crossentropy', metrics=['accuracy'])

        new_model.summary()
        return new_model

    def train(self):
        print("Training %s started" % self.name)
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        idg_train = ImageDataGenerator(rescale=1. / 255)
        idg_test = ImageDataGenerator(rescale=1. / 255)

        print("Setting up generators..")
        train_generator = idg_train.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False)

        test_generator = idg_train.flow_from_directory(
            self.test_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False)

        train_samples = 1000 # len(train_generator.filenames)
        test_samples =  500 # len(test_generator.filenames)

        num_classes = len(train_generator.class_indices)
        model = self.build_model(num_classes)
        print("Training started..")

        history = model.fit_generator(
            train_generator,
            samples_per_epoch=train_samples,
            epochs=10,
            validation_data=test_generator,
            validation_steps=test_samples)

        print("Training ended")
        self.evaluate(history)
        model.save(self.model_path)

    def evaluate(self, history):
        plt.figure(1)
        plt.subplot(211)
        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')

        plt.subplot(212)
        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig("statistics/" + self.name + "_" + str(time.time()) + ".png")

        with open('statistics/' + self.name + "_" + str(time.time()) + '.json', 'w') as outfile:
            json.dump(history.history, outfile, indent=4)

    def predict(self, image_path):
        print("Predicting image: %s " % image_path)
        orig = cv2.imread(image_path)

        print("Loading and preprocessing image...")
        image = load_img(image_path, target_size=(self.img_width, self.img_height))
        image = img_to_array(image)
        image = image / 255
        image = np.expand_dims(image, axis=0)

        print("Loading model: %s" % self.model_path)
        model = load_model(self.model_path)

        prediction = model.predict(image)
        print(prediction)
        return prediction



