import time
import datetime

import matplotlib.pyplot as plt
import numpy as np
from tensorflow.contrib.layers.python.layers import target_column
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Lambda, Dense, BatchNormalization, Flatten
from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D, Dropout

from keras.models import load_model

from keras.preprocessing import image
from keras.preprocessing.image import ImageDataGenerator



class Cnn2(object):

    def __init__(self):
        self.classifier = None
        self.history = None

    def build(self):
        self.classifier = Sequential()
        self.history = None

        self.classifier.add(Convolution2D(32, 3, 3, input_shape=(64, 64, 3), activation='relu'))

        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

        self.classifier.add(Flatten())

        self.classifier.add(Dense(128, activation='relu'))
        self.classifier.add(Dense(1, activation='sigmoid'))

        self.classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def train(self):
        self.build()
        image_gen = ImageDataGenerator(rescale=1.0 / 255)

        train_set = image_gen.flow_from_directory("data/train/",
                                                  batch_size=32,
                                                  target_size=(64, 64),
                                                  class_mode='binary')
        test_set = image_gen.flow_from_directory("data/test",
                                                 batch_size=32,
                                                 target_size=(64, 64),
                                                 class_mode='binary',
                                                 shuffle=False)
        self.history = self.classifier.fit_generator(
            train_set,
            steps_per_epoch=5000, #8000
            epochs=10, #10
            validation_data=test_set,
            validation_steps=800 #800
        )

    def visualize_history(self):

        if self.history is None:
            raise Exception("Train the model first before visualize history")

        plt.figure()
        plt.plot(self.history.history['loss'], label="train_loss")
        plt.plot(self.history.history['acc'], label="train_acc")
        #plt.plot(self.history.history['val_loss'], label="val_loss")
        #plt.plot(self.history.history['val_acc'], label="val_acc")
        plt.title("Training Loss and Accuracy")
        plt.xlabel("Epoch")
        plt.ylabel("Loss/Accuracy")
        plt.legend()

        plt.savefig("statistics/cnn_" + str(time.time()) + ".png")
        plt.show()

    def use(self, img_name):
        if self.classifier is None:
            self.load()
        test_image = image.load_img(img_name, target_size=(64, 64))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)

        prediction = self.classifier.predict(test_image)
        if prediction[0][0] >= .5:
            print("Its a dog")
        else:
            print("Its a cat")

    def save(self):
        if self.classifier is None:
            raise Exception("Train the model before save it")

        self.classifier.save("model/cnn_model.h5")

    def load(self):
        del self.classifier
        self.classifier = load_model("model/cnn_model.h5")

