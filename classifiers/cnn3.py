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
from tensorflow.python.framework import graph_util
from tensorflow.python.framework import graph_io
from keras import backend as K
import os.path as osp
import os
import tensorflow as tf



class Cnn3(object):

    def __init__(self, mid=None):
        self.img_width, self.img_height = 224, 224
        if mid is None:
            self.id = uuid.uuid4()
            print("Creating new classifier with id ", str(self.id))
        else:
            self.id = mid
            print("Using classifier with id ", str(self.id))
        self.train_dir = "data/train/"
        self.test_dir = "data/test/"

        # VGG16
        self.bottleneck_test_features = "model/bottleneck/bottleneck_features_train.npy"
        self.bottleneck_train_features = "model/bottleneck/bottleneck_features_validation.npy"
        self.bottleneck_model = "model/bottleneck/bigmodel.h5"

        # TOP model
        self.top_model_weights = 'model/bottleneck/bottleneck_' + str(self.id) + ".h5"
        self.class_indices = "model/" + str(self.id) + "class_indices.npy"

        # TRAIN and MODEL params
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

        self.evaluate()

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

    def predict(self, image_path, img_name):

        class_dictionary = np.load('model/class_indices.npy').item()  # TODO add the class variable

        num_classes = len(class_dictionary)

        orig = cv2.imread(image_path)

        print("Loading and preprocessing image...")
        image = load_img(image_path, target_size=(self.img_width, self.img_height))
        image = img_to_array(image)
        image = image / 255
        image = np.expand_dims(image, axis=0)

        # build the VGG16 network
        model = applications.VGG16(include_top=False, weights='imagenet')
        # get the bottleneck prediction from the pre-trained VGG16 model
        bottleneck_prediction = model.predict(image)

        # build top model
        model = Sequential()
        model.add(Flatten(input_shape=bottleneck_prediction.shape[1:]))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))

        model.load_weights(self.top_model_weights)

        # use the bottleneck prediction on the top model to get the final
        # classification
        class_predicted = model.predict_classes(bottleneck_prediction)
        probabilities = model.predict_proba(bottleneck_prediction)

        inID = class_predicted[0]

        inv_map = {v: k for k, v in class_dictionary.items()}

        label = inv_map[inID]

        # get the prediction label
        print("Image ID: {}, Label: {}, Probability {}".format(inID, label, probabilities))

        # display the predictions with the image
        cv2.putText(orig, "Predicted: {}".format(label), (10, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (43, 99, 255), 2)

        cv2.imwrite("statistics/" + img_name, orig)
        cv2.destroyAllWindows()

    def model_to_graph(self):
        class_dictionary = np.load('model/class_indices.npy').item()  # TODO add the class variable
        inv_map = {v: k for k, v in class_dictionary.items()}

        node_names = list(inv_map.values())
        num_classes = len(node_names)

        bottleneck_model_name = "bottleneck_graph.pb"
        bottleneck_model = applications.VGG16(include_top=False, weights='imagenet')

        top_mode_name = "top_graph.pb"
        train_data = np.load(self.bottleneck_train_features)
        model = Sequential()
        model.add(Flatten(input_shape=train_data.shape[1:]))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax'))
        model.load_weights(self.top_model_weights)

        K.set_learning_phase(0)

        print('output nodes names are: ', node_names)

        bottleneck_pred = [None] * len(node_names)
        for i in range(len(node_names)):
            bottleneck_pred[i] = tf.identity(bottleneck_model.output[i], name=node_names[i])

        top_pred = [None] * len(node_names)
        for i in range(len(node_names)):
            top_pred[i] = tf.identity(bottleneck_model.output[i], name=node_names[i])

        with K.get_session() as sess:
            bottle_constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), node_names)
            graph_io.write_graph(bottle_constant_graph, "model/", bottleneck_model_name, as_text=False)
            print('saved the bottom constant graph (ready for inference) at: ', osp.join("model/", bottleneck_model_name))

            top_constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(), node_names)
            graph_io.write_graph(top_constant_graph, "model/", top_mode_name, as_text=False)
            print('saved the top constant graph (ready for inference) at: ', osp.join("model/", top_mode_name))



