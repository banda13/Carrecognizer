import os
import uuid
import json
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

        '''
        Basic stuff
        '''
        self.train_dir = paths.TRAIN_DIR
        self.test_dir = paths.TEST_DIR
        self.categories = os.listdir(self.train_dir)
        self.num_classes = len(self.categories)

        '''
        Pre processing (pre classifier + pre processor)
        '''
        self.pre_classifier_categories_count = len(VggPreClassifier.bad_vgg_categories)

        self.data_soruces = CleverLoader.data_soruce_dirs
        self.pre_loader_filter = LoaderFilter.NO
        self.p_train = 0.8
        self.p_test = 0.2
        self.limit = 10000

        '''
        Classify (cnn3 transfer train + cnn7 fine tune)
        '''
        self.image_width = 250
        self.image_height = 250

        model = Sequential()
        model.add(Convolution2D(128, 3, 3, input_shape=(7, 7, 512), activation='relu'))
        model.add(Dropout(0.5))
        model.add(MaxPooling2D(pool_size=(2, 2)))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))
        model.compile(optimizer=RMSprop(lr=0.0001, rho=0.9, epsilon=None, decay=0.0),
                           loss='categorical_crossentropy', metrics=['accuracy'])

        # CNN3 - transfer train
        self.cnn3_params = {
            "bottleneck_train_features" : paths.ROOT_DIR + "/model/bottleneck/bottleneck_features_train.npy",
            "bottleneck_test_features" : paths.ROOT_DIR + "/model/bottleneck/bottleneck_features_validation.npy",
            "bottleneck_model" : paths.ROOT_DIR + "/model/bottleneck/bigmodel.h5",
            "top_model_weights" : paths.ROOT_DIR + '/model/bottleneck/bottleneck_' + str(self.pid) + ".h5",
            "class_indices" : paths.ROOT_DIR + "/model/" + str(self.pid) + "_class_indices.npy",
            "top_model" : model,
            "epochs" : 20,
            "batch_size" : 16,
            "augmentation": {
                "shear_range": 0.2,
                "zoom_range" : 0.2,
                "horizontal_flip" : True,
                "rescale":1. / 255
            },
            "accuracy": None,
            "loss": None,
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
        History statistic
        '''
        # stats
        self.creation_date = datetime.datetime.now()
        self.all_run_time_in_sec = 0
        self.cnn_stats = {}
        self.tests_stats = {}

        # files
        print("New classifier created with id: %s" % (str(self.pid)))

    def train(self):
        print("Training started")


test = ConvolutionalNeuralNetwork()
test.create()
test.save()
test.load(test.pid)

