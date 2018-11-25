import os
import uuid
import json
import time
import datetime
import dateutil.parser as dp

from keras import Sequential
from keras.layers import Convolution2D, Dropout, MaxPooling2D, Flatten, Dense, regularizers
from keras.optimizers import RMSprop
from keras.models import model_from_json
from keras.models import load_model
from keras_preprocessing.image import ImageDataGenerator

import paths
from enum import Enum

from classifiers.cnn3 import Cnn3
from preprocess.clever_loader import LoaderFilter, CleverLoader, PreClassificationState
from preprocess.pre_classification import VggPreClassifier

PUBLIC_ENUMS = {
    'LoaderFilter': LoaderFilter,
    'PreClassificationState': PreClassificationState
}

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if obj is not None:
            if isinstance(obj, Enum):
                return {"__enum__": str(obj)}
            if isinstance(obj, Sequential):
                return {"__sequential__": obj.to_json()}
            if isinstance(obj, datetime.datetime):
                return {'__isoformat__': obj.isoformat()}
        return json.JSONEncoder.default(self, obj)


def decoder_hook(d):
    if d.get('__enum__'):
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    if d.get('__sequential__'):
        return model_from_json(d["__sequential__"])
    if d.get('__sequential__'):
        return dp.parse(d.get('__isoformat__'))
    else:
        return d


class ConvolutionalNeuralNetwork(object):

    def __init__(self):
        self.pid = None

    def load(self, pid):
        self.pid = pid
        with open('data.json', 'r') as params:
            self.__dict__= json.load(params, object_hook=decoder_hook)
            print("Deserialization done")

    def save(self):
        with open('data.json', 'w') as history_file:
            serialized = json.dump(self.__dict__, history_file, indent=4, cls=Encoder)
        print("Serialization done")

    def create(self):
        self.pid = str(uuid.uuid4())
        self.test = True

        num_classes = len(os.listdir(paths.TRAIN_DIR))
        '''
        Basic stuff
        '''
        self.core = {
            "train_dir": paths.TRAIN_DIR,
            "test_dir": paths.TEST_DIR,
            "categories": os.listdir(paths.TRAIN_DIR),
            "num_classes": len(os.listdir(paths.TRAIN_DIR))
        }

        '''
        Pre processing (pre classifier + pre processor)
        '''
        self.preclassifier = {
           "pre_classifier_categories_count" : len(VggPreClassifier.bad_vgg_categories)
        }

        self.preprocessor = {
            "data_soruces": CleverLoader.data_soruce_dirs,
            "pre_loader_filter": LoaderFilter.NO,
            "p_train": 0.8,
            "p_test": 0.2,
            "limit": 100,
            "run_time": None
        }

        '''
        Classify (cnn3 transfer train + cnn7 fine tune)
        '''
        self.classification = {
            "image_width" : 250,
            "image_height" : 250
        }

        model = Sequential()
        model.add(Convolution2D(128, 3, 3, input_shape=(7, 7, 512), activation='relu'))
        model.add(Dropout(0.5))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(num_classes, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
        model.compile(optimizer=RMSprop(lr=0.0001, rho=0.9, epsilon=None, decay=0.0),
                           loss='categorical_crossentropy', metrics=['accuracy'])

        # CNN3 - transfer train (in and out params)
        self.cnn3_in = {
            "bottleneck_train_features" : paths.ROOT_DIR + "/model/bottleneck/bottleneck_features_train.npy",
            "bottleneck_test_features" : paths.ROOT_DIR + "/model/bottleneck/bottleneck_features_validation.npy",
            "bottleneck_model" : paths.ROOT_DIR + "/model/bottleneck/bigmodel.h5",
            "top_model_weights" : paths.ROOT_DIR + '/model/bottleneck/bottleneck_' + str(self.pid) + ".h5",
            "class_indices" : paths.ROOT_DIR + "/model/" + str(self.pid) + "_class_indices.npy",
            "top_model" : model,
            "epochs" : 1,
            "batch_size" : 16,
            "augmentation": {
                "shear_range": 0.2,
                "zoom_range" : 0.2,
                "horizontal_flip" : True,
                "rescale":1. / 255
            },
        }
        self.cnn3_out = {
            "accuracy": None,
            "loss": None,
            "plot": None,
            "histroy": None
        }

        # recomiple model for cnn7
        model.compile(optimizer=RMSprop(lr=0.001, rho=0.8, epsilon=None, decay=0.0),
                      loss='categorical_crossentropy', metrics=['accuracy'])

        # CNN7 - fine tune
        self.cnn7_params = {
            "top_model": model
        }

        '''
        History
        '''
        self.history = {
            "creation_date" : datetime.datetime.now(),
            "train_time" : 0.0
        }


        # files
        print("New classifier created with id: %s" % (str(self.pid)))

    def preprocess(self):
        print("Preprocessing started")
        start_time = time.time()
        loader = CleverLoader(self.preprocessor['p_train'], self.preprocessor['p_test'], self.preprocessor['limit'], f=self.preprocessor['pre_loader_filter'])
        loader.load()
        self.preprocessor['run_time'] = time.time() - start_time
        self.save()

    def train(self):
        print("Training started")
        start_time = time.time()
        cnn = Cnn3(self.pid, self.core, self.classification, self.cnn3_in, self.cnn3_out)
        cnn.save_bottlebeck_features()
        cnn.train_top_model()
        cnn.evaluate()
        self.cnn3_out = cnn.out_params
        self.history['train_time'] = time.time() - start_time
        self.save()

    def test(self):
        print("Testing started")

    def evaluate(self):
        print("Evaluating started")


test = ConvolutionalNeuralNetwork()
test.create()
test.save()
# test.load(test.pid)
test.preprocess()
test.train()

