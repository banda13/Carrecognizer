import os
import uuid
import json
import paths
from enum import Enum
from preprocess.clever_loader import LoaderFilter, CleverLoader
from preprocess.pre_classification import VggPreClassifier



class Encoder(json.JSONEncoder):
    def default(self, obj):
        if obj is not None:
            if isinstance(obj, Enum):
                return {"__enum__": str(obj)}
        return json.JSONEncoder.default(self, obj)

def decoder_hook(d):
    if "__enum__" in d:
        name, member = d["__enum__"].split(".")
        return getattr(LoaderFilter[name], member)
    else:
        return d

class ConvolutionalNeuralNetwork(object):

    def __init__(self):
        self.pid = None

    def load(self, pid):
        self.pid = pid
        with open('data.json', 'r') as params:
            self.__dict__=json.load(params)
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
        self.categories_count = len(self.categories)

        '''
        Pre processing
        '''
        # pre classifier
        self.pre_classifier_categories_count = len(VggPreClassifier.bad_vgg_categories)

        # pre processing
        self.data_soruces = CleverLoader.data_soruce_dirs
        self.pre_loader_filter = LoaderFilter.NO
        self.p_train = 0.8
        self.p_test = 0.2
        self.limit = 10000

        '''
        Classify
        '''
        self.image_width = 250
        self.image_height = 250


test = ConvolutionalNeuralNetwork()
#test.create()
#test.save()
test.load(test.pid)

