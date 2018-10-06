import datetime

from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Lambda, Dense, BatchNormalization, Flatten
from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D, Dropout

from keras.models import load_model

from keras.preprocessing.image import ImageDataGenerator


class Cnn2(object):

    def __init__(self):
        self.classifier = Sequential()
        self.history = None

        self.classifier.add(Convolution2D(32, 3, 3, input_shape=(64, 64, 3), activation='relu'))

        self.classifier.add(MaxPooling2D(pool_size=(2, 2)))

        self.classifier.add(Flatten())

        self.classifier.add(Dense(128, activation='relu'))
        self.classifier.add(Dense(1, activation='sigmoid'))

        self.classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])[]

    def train(self):

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
        self.classifier.fit_generator(
            train_set,
            steps_per_epoch=8000,
            epochs=10,
            validation_data=test_set,
            validation_steps=800
        )

    def save(self):
        if self.classifier is None:
            raise Exception("Train the model before save it")

        self.classifier.save("models/cnn_model.h5")

    def load(self):
        del self.classifier
        self.classifier = load_model("models/cnn_model.h5")

