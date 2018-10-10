import numpy as np
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.optimizers import RMSprop
from keras import applications
from keras.utils.np_utils import to_categorical
import matplotlib.pyplot as plt
import math
import cv2
import uuid
import json
from PIL import ImageFile


class Cnn3(object):

    def __init__(self):
        self.img_width, self.img_height = 224, 224
        self.id = uuid.uuid4()
        self.train_dir = "data/train/"
        self.test_dir = "data/test/"

        # VGG16
        self.bottleneck_test_features = "model/bottleneck/bottleneck_features_train.npy"
        self.bottleneck_train_features = "model/bottleneck/bottleneck_features_validation.npy"
        self.bottleneck_model = "model/bottleneck/bigmodel.h5"

        # TOP model

        self.top_model_weights = 'classifiers/pre_train/bottleneck_' + str(self.id) + ".h5"
        self.class_indices = "model/" + str(self.id) + "class_indices.npy"

        # TRAIN params
        self.epochs = 25
        self.batch_size = 16
        self.learning_rate = 0.00001

        self.model = None
        self.history = None

    def save_bottlebeck_features(self):
        # build the VGG16 network
        model = applications.VGG16(include_top=False, weights='imagenet')

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        datagen = ImageDataGenerator(rescale=1. / 255)

        generator = datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        print(len(generator.filenames))
        print(generator.class_indices)
        print(len(generator.class_indices))

        nb_train_samples = len(generator.filenames)
        num_classes = len(generator.class_indices)

        predict_size_train = int(math.ceil(nb_train_samples / self.batch_size))

        bottleneck_features_train = model.predict_generator(
            generator, predict_size_train)

        np.save(self.bottleneck_train_features, bottleneck_features_train)

        generator = datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        nb_validation_samples = len(generator.filenames)

        predict_size_validation = int(
            math.ceil(nb_validation_samples / self.batch_size))

        bottleneck_features_validation = model.predict_generator(
            generator, predict_size_validation)

        np.save(self.bottleneck_test_features, bottleneck_features_validation)
        model.save(self.bottleneck_model)

    def train_top_model(self):

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        datagen_top = ImageDataGenerator(rescale=1. / 255)
        generator_top = datagen_top.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical',
            shuffle=False)

        nb_train_samples = len(generator_top.filenames)
        num_classes = len(generator_top.class_indices)

        # save the class indices to use use later in predictions
        np.save(self.class_indices, generator_top.class_indices)

        train_data = np.load(self.bottleneck_train_features)

        train_labels = generator_top.classes

        train_labels = to_categorical(train_labels, num_classes=num_classes)

        generator_top = datagen_top.flow_from_directory(
            self.test_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        nb_validation_samples = len(generator_top.filenames)

        validation_data = np.load(self.bottleneck_test_features)

        validation_labels = generator_top.classes
        validation_labels = to_categorical(
            validation_labels, num_classes=num_classes)

        self.model = Sequential()
        self.model.add(Flatten(input_shape=train_data.shape[1:]))
        self.model.add(Dense(256, activation='relu'))
        self.model.add(Dropout(0.5))
        self.model.add(Dense(num_classes, activation='softmax'))

        self.model.compile(optimizer=RMSprop(lr=self.learning_rate),
                           loss='categorical_crossentropy', metrics=['accuracy'])

        self.history = self.model.fit(train_data, train_labels,
                                      epochs=self.epochs,
                                      batch_size=self.batch_size,
                                      validation_data=(validation_data, validation_labels))

        self.model.save_weights(self.top_model_weights)

        (eval_loss, eval_accuracy) = self.model.evaluate(
            validation_data, validation_labels, batch_size=self.batch_size, verbose=1)

        print("Accuracy: {:.2f}%".format(eval_accuracy * 100))
        print("Loss: {}".format(eval_loss))

    def evaluate(self):
        plt.figure(1)
        plt.subplot(211)
        plt.plot(self.history.history['acc'])
        plt.plot(self.history.history['val_acc'])
        plt.title('model accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')

        plt.subplot(212)
        plt.plot(self.history.history['loss'])
        plt.plot(self.history.history['val_loss'])
        plt.title('model loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.savefig("statistics/" + str(self.id) + ".png")

        with open('statistics/' + str(self.id) + '.json', 'w') as outfile:
            json.dump(self.history.history, outfile, indent=4)
