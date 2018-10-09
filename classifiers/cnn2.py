import os
import json
import time
import datetime
import uuid

from PIL import ImageFile

import matplotlib.pyplot as plt
import numpy as np
from tensorflow.contrib.layers.python.layers import target_column
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Lambda, Dense, BatchNormalization, Flatten
from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D, Dropout
from tensorflow.python.keras.optimizers import Adam, SGD
from keras import regularizers
from IPython.display import SVG
from keras.utils.vis_utils import model_to_dot

from keras.models import load_model

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator

from test import safer_manual_accuracy_test


class Cnn2(object):

    def __init__(self):
        self.classifier = None
        self.history = None
        self.id = uuid.uuid4()
        self.name = "cnn_model" + str(self.id)

        # CNN PROPERTIES
        self.learning_rate = 0.0001  # TODO slow down learing rate, check results (0.001 to big maybe)

    def build(self):
        self.classifier = Sequential()
        self.history = None

        self.classifier.add(Convolution2D(32, 3, 3, input_shape=(64, 64, 3), activation='relu'))

        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

        # TODO there maybe needed one mpre convolution2D layer
        # self.classifier.add(Convolution2D(32, 3, 3, activation='relu'))
        # self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

        # TODO one more conv2D layer? :)

        self.classifier.add(Flatten())

        self.classifier.add(Dense(128, activation='relu'))

        # TODO some dropout maybe prevent overfitting
        self.classifier.add(Dropout(0.5))

        # TODO még 1 Dense réteg is lehet segít hogy bonyolultabban közeltsen a háló
        self.classifier.add(Dense(1, kernel_regularizer=regularizers.l2(0.01), activation='sigmoid'))
        # TODO l2 regularizáció vagy esetleg early stopping is jó lehet h elkerüljük az overfittinget

        # TODO try SGD optimalizer pl:
        # SGD(lr=1e-4, momentum=0.9)
        self.classifier.compile(optimizer=Adam(lr=self.learning_rate), loss='binary_crossentropy', metrics=['accuracy'])
        print("Model build")

    def train(self, continuous_train=False):
        if continuous_train:
            self.load()
        else:
            self.build()

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image_gen = ImageDataGenerator(rescale=1.0 / 255)

        train_set = image_gen.flow_from_directory("data/train/",
                                                  # TODO change batch size
                                                  batch_size=32,
                                                  target_size=(64, 64),
                                                  class_mode='binary')
        test_set = image_gen.flow_from_directory("data/test",
                                                 batch_size=32,
                                                 target_size=(64, 64),
                                                 class_mode='binary',
                                                 shuffle=False)
        try:
            self.history = self.classifier.fit_generator(
                train_set,
                steps_per_epoch=100,  # 8000
                # TODO try more epoch with slow learning rate
                epochs=5,  # 10
                validation_data=test_set,
                validation_steps=800  # 800
            )
        except KeyboardInterrupt as e:
            if continuous_train:
                self.save()

        self.save()
        self.evaluate()

    def evaluate(self):
        if self.history is None:
            raise Exception("Train the model before evaluate it")
        manual_accuracy = safer_manual_accuracy_test(self)
        self.history.history['manual_acc'] = manual_accuracy
        with open('statistics/cnn_ ' + self.name + '.json', 'w') as outfile:
            json.dump(self.history.history, outfile, indent=4)

        plt.figure()
        plt.plot(self.history.history['loss'], label="train_loss")
        plt.plot(self.history.history['acc'], label="train_acc")
        if 'val_loss' in self.history.history:
            plt.plot(self.history.history['val_loss'], label="val_loss")
        if 'val_acc' in self.history.history:
            plt.plot(self.history.history['val_acc'], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Loss/Accuracy")
        plt.legend()

        plt.savefig("statistics/" + self.name + ".png")
        # plt.show()

    def use(self, img_name):
        if self.classifier is None:
            self.load()
        test_image = image.load_img(img_name, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        prediction = self.classifier.predict(test_image)
        asd = np.argmax(prediction)
        asd2 = prediction[0][0]
        return asd2
        # return np.argmax(prediction)

    def show_the_model(self):
        if self.classifier is None:
            self.build()
        SVG(model_to_dot(self.classifier).create(prog='dot', format='svg'))

    def clear(self):
        if self.classifier is not None:
            self.classifier = None
        if os.path.isfile("model/" + self.name + ".h5"):
            os.remove("model/" + self.name + ".h5")
            print("Model deleted")
        else:
            print("Model does not exist")

    def save(self):
        if self.classifier is None:
            raise Exception("Train the model before save it")

        self.classifier.save("model/" + self.name + ".h5")
        print("Model saved")

    def load(self):
        del self.classifier
        if os.path.isfile("model/" + self.name + ".h5"):
            self.classifier = load_model("model/" + self.name + ".h5")
            print("Model loaded")
        else:
            self.build()
            print("Model doest not exists, new model build")
