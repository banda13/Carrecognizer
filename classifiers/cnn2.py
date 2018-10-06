import keras
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Input, Lambda, Dense, BatchNormalization, Flatten
from tensorflow.python.keras.layers import Convolution2D, MaxPooling2D, Dropout

from keras.preprocessing.image import ImageDataGenerator

class Cnn2(object):

    def train(self):
        classifier = Sequential()

        classifier.add(Convolution2D(32, 3, 3, input_shape=(64, 64, 3), activation='relu'))

        classifier.add(MaxPooling2D(pool_size=(2, 2)))

        classifier.add(Flatten())

        classifier.add(Dense(output_dim=128, activation='relu'))
        classifier.add(Dense(output_dim=1, activation='sigmoid'))

        classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

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
        classifier.fit_generator(
            train_set,
            steps_per_epoch=8000,
            epochs=10,
            validation_data=test_set,
            validation_steps=800
        )