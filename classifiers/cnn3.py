import time

import numpy as np
from keras.engine.saving import load_model
from keras.preprocessing.image import ImageDataGenerator, img_to_array, load_img
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, Convolution2D, MaxPooling2D, GlobalAveragePooling2D
from keras.optimizers import RMSprop, Adam, SGD
from keras import applications, regularizers
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

import paths


class Cnn3(object):

    def __init__(self, pid, core_params, classification_params, in_params, out_params):
        self.img_width, self.img_height = classification_params['image_width'], classification_params['image_height']
        self.id = pid
        print("Using cnn3 classifier with id ", str(self.id))
        self.train_dir = core_params['train_dir']
        self.test_dir = core_params['test_dir']

        # VGG16
        self.bottleneck_train_features = in_params['bottleneck_train_features']
        self.bottleneck_test_features = in_params['bottleneck_test_features']
        self.bottleneck_model = in_params['bottleneck_model']

        # TOP model
        self.top_model_weights = in_params['top_model_weights']
        self.class_indices = in_params['class_indices']

        # TRAIN and MODEL params
        self.epochs = in_params['epochs']
        self.batch_size = in_params['batch_size']
        self.augmentation = in_params['augmentation']
        self.top_model = in_params['top_model']

        self.history = None
        self.out_params = out_params
        print("Cnn3 initialized")

    def save_bottlebeck_features(self):
        print("Saving bottleneck features started")

        # build the VGG16 network
        model = applications.VGG16(include_top=False, weights='imagenet',
                                   input_shape=(self.img_width, self.img_height, 3))

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        datagen = ImageDataGenerator(self.augmentation)

        generator = datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        nb_train_samples = len(generator.filenames)
        predict_size_train = int(math.ceil(nb_train_samples / self.batch_size))
        bottleneck_features_train = model.predict_generator(generator, predict_size_train)
        np.save(self.bottleneck_train_features, bottleneck_features_train)
        print("Bottleneck train features saved as ", self.bottleneck_train_features)

        datagen = ImageDataGenerator(rescale=1. / 255)
        generator = datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        nb_validation_samples = len(generator.filenames)
        predict_size_validation = int(math.ceil(nb_validation_samples / self.batch_size))
        bottleneck_features_validation = model.predict_generator(generator, predict_size_validation)
        np.save(self.bottleneck_test_features, bottleneck_features_validation)
        print("Bottleneck validation features saved as ", self.bottleneck_test_features)

        model.save(self.bottleneck_model)
        print("Bottleneck models saved")

    def train_top_model(self):

        print("Training top model started")
        ImageFile.LOAD_TRUNCATED_IMAGES = True
        datagen_top = ImageDataGenerator(rescale=1. / 255)

        generator_top = datagen_top.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        num_classes = len(generator_top.class_indices)
        np.save(self.class_indices, generator_top.class_indices)
        print("Class indices save as ", self.class_indices)

        train_data = np.load(self.bottleneck_train_features)
        train_labels = generator_top.classes
        train_labels = to_categorical(train_labels, num_classes=num_classes)

        datagen_top = ImageDataGenerator(rescale=1. / 255)
        generator_top = datagen_top.flow_from_directory(
            self.test_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode=None,
            shuffle=False)

        validation_data = np.load(self.bottleneck_test_features)
        validation_labels = generator_top.classes
        validation_labels = to_categorical(
            validation_labels, num_classes=num_classes)

        input_shape = train_data.shape[:1]

        self.history = self.top_model.fit(train_data, train_labels,
                                          epochs=self.epochs,
                                          batch_size=self.batch_size,
                                          validation_data=(validation_data, validation_labels))

        self.top_model.save_weights(self.top_model_weights)
        print("Top model trained, weights saved as ", self.top_model_weights)

        (eval_loss, eval_accuracy) = self.top_model.evaluate(
            validation_data, validation_labels, batch_size=self.batch_size, verbose=1)

        print("Accuracy: {:.2f}%".format(eval_accuracy * 100))
        print("Loss: {}".format(eval_loss))

        self.out_params['accuracy'] = eval_accuracy
        self.out_params['loss'] = eval_loss

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
        stat_plot_dir = paths.STAT_DIR + str(self.id) + "_" + str(time.time()) + ".png"
        plt.savefig(stat_plot_dir)
        self.out_params['plot'] = stat_plot_dir
        self.out_params['histroy'] = self.history.history

        with open(paths.STAT_DIR + str(self.id) + "_" + str(time.time()) + '.json', 'w') as outfile:
            json.dump(self.history.history, outfile, indent=4)

    @staticmethod
    def visualize_class_activation_map(img_path):
        model = load_model(paths.ROOT_DIR + "/model/bottleneck/bigmodel.h5")
        original_img = cv2.imread(img_path, 1)
        width, height, _ = original_img.shape

        # Reshape to the network input shape (3, w, h).
        img = np.array([np.transpose(np.float32(original_img), (2, 0, 1))])

        # Get the 512 input weights to the softmax.
        layers = model.layers
        class_weights = model.layers[-2].get_weights()[0]
        final_conv_layer = model.layers[-2]
        get_output = K.function([model.layers[0].input],
                                [final_conv_layer.output,
                                 model.layers[-1].output])
        [conv_outputs, predictions] = get_output([img])
        conv_outputs = conv_outputs[0, :, :, :]

        # Create the class activation map.
        cam = np.zeros(dtype=np.float32, shape=conv_outputs.shape[1:3])
        target_class = 1
        for i, w in enumerate(class_weights[:, target_class]):
            cam += w * conv_outputs[i, :, :]


    def predict(self, image_path, img_name):

        class_dictionary = np.load(self.class_indices).item()

        num_classes = len(class_dictionary)

        orig = cv2.imread(image_path)

        print("Loading and preprocessing image...")
        image = load_img(image_path, target_size=(self.img_width, self.img_height))
        image = img_to_array(image)
        image = image / 255
        image = np.expand_dims(image, axis=0)
        # TODO show what' s left

        # build the VGG16 network
        model = applications.VGG16(include_top=False, weights='imagenet')
        # get the bottleneck prediction from the pre-trained VGG16 model
        bottleneck_prediction = model.predict(image)

        # build top model
        model = Sequential()
        model.add(Flatten(input_shape=bottleneck_prediction.shape[1:], name="csakmert"))
        model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
        model.add(Dense(num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])

        model.load_weights(self.top_model_weights)

        # use the bottleneck prediction on the top model to get the final
        # classification
        class_predicted = model.predict_classes(bottleneck_prediction)
        probabilities = model.predict_proba(bottleneck_prediction)

        inID = class_predicted[0]

        inv_map = {v: k for k, v in class_dictionary.items()}

        label = inv_map[inID]

        # get the prediction label
        print("Image ID: {}, Label: {}, Probability {}".format(inID, label, probabilities[0][inID]))

        # display the predictions with the image
        cv2.putText(orig, "Predicted: {}".format(label), (10, 30),
                    cv2.FONT_HERSHEY_PLAIN, 1.5, (43, 99, 255), 2)

        K.clear_session()

        # cv2.imwrite("statistics/" + img_name, orig)
        cv2.destroyAllWindows()
        if probabilities[0][inID] > 0.5:
            return label
        else:
            return "Nem tudom talán " + label + " (" + str(probabilities[0][inID]) + "%)"

    def print_graph_nodes(self, filename):
        import tensorflow as tf
        g = tf.GraphDef()
        g.ParseFromString(open(filename, 'rb').read())
        print()
        print(filename)
        print("=======================INPUT=========================")
        print([n for n in g.node if n.name.find('input') != -1])
        print("=======================OUTPUT========================")
        print([n for n in g.node if n.name.find('output') != -1])
        print("===================KERAS_LEARNING=====================")
        print([n for n in g.node if n.name.find('keras_learning_phase') != -1])
        print("======================================================")
        print()

    def model_to_graph(self):
        train_data = np.load(self.bottleneck_train_features)
        prefix_output_node_names_of_final_network = 'output_node'
        class_dictionary = np.load(self.class_indices).item()
        inv_map = {v: k for k, v in class_dictionary.items()}

        node_names = list(inv_map.values())
        num_classes = len(node_names)

        bottleneck_model_name = "bottleneck_graph.pb"
        bottleneck_model_name_txt = "bottleneck_graph.pbtxt"
        bottleneck_model = applications.VGG16(include_top=False, weights='imagenet')

        top_mode_name = "top_graph.pb"
        top_mode_name_txt = "top_graph.pbtxt"
        train_data = np.load(self.bottleneck_train_features)
        model = Sequential()
        model.add(Flatten(input_shape=train_data.shape[1:], name="csakmert"))
        model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
        model.add(Dense(num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        model.load_weights(self.top_model_weights)

        K.set_learning_phase(0)

        print('output nodes names are: ', node_names)

        sess = K.get_session()

        [print(node.op.name) for node in bottleneck_model.outputs]
        [print(node.op.name) for node in bottleneck_model.inputs]
        print(bottleneck_model.input_shape)
        print(bottleneck_model.output_shape)
        graph_def = sess.graph.as_graph_def()
        bottle_constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(),
                                                                          [node.op.name for node in
                                                                           bottleneck_model.outputs])
        graph_io.write_graph(bottle_constant_graph, "model/", bottleneck_model_name, as_text=False)
        graph_io.write_graph(bottle_constant_graph, "model/", bottleneck_model_name_txt, as_text=True)
        print('saved the bottom constant graph (ready for inference) at: ', osp.join("model/", bottleneck_model_name))

        K.clear_session()

        [print(node.op.name) for node in model.outputs]
        [print(node.op.name) for node in bottleneck_model.inputs]
        print(model.input_shape)
        print(model.output_shape)
        graph_def = sess.graph.as_graph_def()
        top_constant_graph = graph_util.convert_variables_to_constants(sess, sess.graph.as_graph_def(),
                                                                       [node.op.name for node in model.outputs])
        graph_io.write_graph(top_constant_graph, "model/", top_mode_name, as_text=False)
        graph_io.write_graph(top_constant_graph, "model/", top_mode_name_txt, as_text=True)
        print('saved the top constant graph (ready for inference) at: ', osp.join("model/", top_mode_name))
