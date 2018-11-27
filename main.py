import os
import uuid
import json
import time
import datetime

from keras import Sequential
from keras.layers import Convolution2D, Dropout, MaxPooling2D, Flatten, Dense, regularizers
from keras.optimizers import RMSprop

import paths

from classifiers.cnn3 import Cnn3
from classifiers.cnn7_fine_tune import Cnn7
from classifiers.cnn_test import TestCNN
from classifiers.lstm0 import NameGenerator
from preprocess.clever_loader import LoaderFilter, CleverLoader
from preprocess.pre_classification import VggPreClassifier
from utils.json_utils import decoder_hook, Encoder


class ConvolutionalNeuralNetwork(object):

    def __init__(self):
        self.pid = None
        self.history_location = None

    def load(self, pid):
        self.pid = pid
        self.history_location = paths.ROOT_DIR + '/history/' + self.pid + ".json"
        with open(self.history_location, 'r') as params:
            self.__dict__ = json.load(params, object_hook=decoder_hook)
            print("Deserialization done")

    def save(self):
        with open(self.history_location, 'w') as history_file:
            json.dump(self.__dict__, history_file, indent=4, cls=Encoder)
        print("Serialization done")

    def create(self):
        self.pid = NameGenerator().get_name() # str(uuid.uuid4())
        self.history_location = paths.ROOT_DIR + '/history/' + self.pid + ".json"
        self.test = True

        categories = os.listdir(paths.TRAIN_DIR)
        num_classes = len(categories)
        '''
        Basic stuff
        '''
        self.core = {
            "train_dir": paths.TRAIN_DIR,
            "test_dir": paths.TEST_DIR,
            "categories": categories,
            "num_classes": num_classes
        }

        '''
        Pre processing (pre classifier + pre processor)
        '''
        self.preclassifier = {
            "pre_classifier_categories_count": len(VggPreClassifier.bad_vgg_categories)
        }

        data_source_dirs = CleverLoader.data_soruce_dirs
        self.preprocessor = {
            "data_soruces": data_source_dirs,
            "pre_loader_filter": LoaderFilter.NO,
            "p_train": 0.8,
            "p_test": 0.2,
            "limit": 10000,
            "run_time": None
        }

        '''
        Classify (cnn3 transfer train + cnn7 fine tune)
        '''
        self.classification = {
            "image_width": 250,
            "image_height": 250
        }

        lr = 0.0001
        model = Sequential()
        model.add(Convolution2D(128, 3, 3, input_shape=(7, 7, 512), activation='relu'))
        model.add(Dropout(0.5))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten(input_shape=(7, 7, 512)))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
        model.compile(optimizer=RMSprop(lr=lr, rho=0.9, epsilon=None, decay=0.0),
                      loss='categorical_crossentropy', metrics=['accuracy'])

        # CNN3 - transfer train (in and out params)
        self.cnn3_in = {
            "bottleneck_train_features": paths.ROOT_DIR + "/model/bottleneck/bottleneck_features_train.npy",
            "bottleneck_test_features": paths.ROOT_DIR + "/model/bottleneck/bottleneck_features_validation.npy",
            "bottleneck_model": paths.ROOT_DIR + "/model/bottleneck/bigmodel.h5",
            "top_model_weights": paths.ROOT_DIR + '/model/bottleneck/bottleneck_' + str(self.pid) + ".h5",
            "class_indices": paths.ROOT_DIR + "/model/" + str(self.pid) + "_class_indices.npy",
            "top_model": model,
            "epochs": 50,
            "batch_size": 16,
            "augmentation": {
                "shear_range": 0.1,
                "zoom_range": 0.1,
                "horizontal_flip": True,
                "rescale": 1. / 255
            },
            "learning_rate": lr
        }
        self.cnn3_out = {
            "accuracy": None,
            "loss": None,
            "plot": None,
            "histroy": None
        }

        # recomiple model for cnn7
        model.compile(optimizer=RMSprop(lr=lr, rho=0.8, epsilon=None, decay=0.0),
                      loss='categorical_crossentropy', metrics=['accuracy'])

        # CNN7 - fine tune
        self.cnn7_in = {
            "epochs": 20,
            "batch_size": 16,
            "num_classes": num_classes,
            "frozen_layers": 15,
            "learning_rate": 1e-5,
            "momentum": 0.6,
            "augmentation": {
                "rotation_range": 30,
                "width_shift_range": 0.2,
                "height_shift_range": 0.2,
                "fill_mode": 'nearest',
                "shear_range": 0.2,
                "zoom_range": 0.2,
                "horizontal_flip": True,
                "rescale": 1. / 255
            },
            "top_model": model,
            "top_model_weights": paths.ROOT_DIR + '/model/bottleneck/bottleneck_' + str(self.pid) + ".h5",
            "model": paths.ROOT_DIR + '/model/' + str(self.pid) + ".h5"
        }

        self.cnn7_out = {
            "plot": None,
            "histroy": None
        }

        '''
        History
        '''
        self.history = {
            "creation_date": datetime.datetime.now(),
            "transfer_train_time": 0.0,
            "fine_tune_train_time": 0.0
        }

        '''
        Test
        '''
        self.test = {
            "model": paths.ROOT_DIR + '/model/' + str(self.pid) + ".h5",
            "test_count_per_class": 1000,
            "run_time": 0,
            "accuracy": 0,
            "category_results": [],
            "data_source_dirs": data_source_dirs
        }

        print("New classifier created with id: %s" % (str(self.pid)))

    def preprocess(self):
        print("Preprocessing started")
        start_time = time.time()
        loader = CleverLoader(self.preprocessor['p_train'], self.preprocessor['p_test'], self.preprocessor['limit'],
                              f=self.preprocessor['pre_loader_filter'])
        loader.load()
        self.preprocessor['run_time'] = time.time() - start_time
        self.save()

    def transfer_train(self):
        print("Transfer train started")
        start_time = time.time()
        cnn = Cnn3(self.pid, self.core, self.classification, self.cnn3_in, self.cnn3_out)
        # cnn.save_bottlebeck_features()
        cnn.train_top_model()
        cnn.evaluate()
        self.cnn3_out = cnn.out_params
        self.history['transfer_train_time'] = time.time() - start_time
        self.save()

    def fine_tune_train(self):
        print("Fine tune train started")
        start_time = time.time()
        cnn = Cnn7(self.pid, self.core, self.classification, self.cnn7_in, self.cnn7_out)
        cnn.fine_tune()
        cnn.evaluate()
        self.cnn7_out = cnn.out_params
        self.history['fine_tune_train_time'] = time.time() - start_time
        self.save()

    def test_classifiers(self):
        print("Testing started")
        start_time = time.time()
        cnn = TestCNN(self.pid, self.test)
        cnn.test()
        self.test['run_time'] = time.time() - start_time
        self.save()

test = ConvolutionalNeuralNetwork()
test.create()
test.save()
# test.load(test.pid)
test.preprocess()
test.transfer_train()
test.fine_tune_train()
