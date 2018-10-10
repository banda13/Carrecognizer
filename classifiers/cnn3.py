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
from PIL import ImageFile

class Cnn3(object):

    def __init__(self):
        self.img_width, self.img_height = 224, 224
        self.id = uuid.uuid4()

        self.top_model_weights = 'classifiers/pre_train/bottleneck_' + str(self.id) + ".h5"
        self.epochs = 25
        self.batch_size = 16

        self.train_dir = "data/train/"
        self.test_dir = "data/test/"

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

        np.save('bottleneck_features_train.npy', bottleneck_features_train)

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

        np.save('classifiers/pre_train/bottleneck_features_validation.npy',
                bottleneck_features_validation)

        try:
            model.save("bigmodel.h5")
        except Exception as e:
            print("nem jött össze")

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
        np.save('class_indices.npy', generator_top.class_indices)

        train_data = np.load('bottleneck_features_train.npy')

        train_labels = generator_top.classes

        train_labels = to_categorical(train_labels, num_classes=num_classes)

        generator_top = datagen_top.flow_from_directory(
            self.test_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        nb_validation_samples = len(generator_top.filenames)

        validation_data = np.load('classifiers/pre_train/bottleneck_features_validation.npy')

        validation_labels = generator_top.classes
        validation_labels = to_categorical(
            validation_labels, num_classes=num_classes)

        model = Sequential()
        model.add(Flatten(input_shape=train_data.shape[1:]))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.00001),
                      loss='categorical_crossentropy', metrics=['accuracy'])

        history = model.fit(train_data, train_labels,
                            epochs=self.epochs,
                            batch_size=self.batch_size,
                            validation_data=(validation_data, validation_labels))

        model.save_weights(self.top_model_weights)

        (eval_loss, eval_accuracy) = model.evaluate(
            validation_data, validation_labels, batch_size=self.batch_size, verbose=1)

        print("Accuracy: {:.2f}%".format(eval_accuracy * 100))
        print("Loss: {}".format(eval_loss))

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
        plt.savefig("statistics/" + str(self.id) + ".png")