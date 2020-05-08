import os
import json
from shutil import copy2

import paths
from classifiers.cnn8 import Cnn8
from classifiers.cnn_test import TestCNN
from classifiers.lstm0 import NameGenerator
from utils.json_utils import decoder_hook, Encoder

import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True # dynamically grow the memory used on the GPU


class CNN8Controller(object):

    def __init__(self):
        self.name = None
        self.history_location = None
        self.train_dir = paths.TRAIN_DIR
        self.validation_dir = paths.VALIDATION_DIR
        self.test_dir = paths.TEST_DIR
        self.cnn = None

        self.name = None
        self.categories = os.listdir(paths.TRAIN_DIR)
        self.num_classes = len(self.categories)
        self.description = None

        self.train_size_per_class = min([len(self.train_dir + '/' + x) for x in os.listdir(self.train_dir)])
        self.validation_size_per_class = min([len(self.validation_dir + '/' + x) for x in os.listdir(self.validation_dir)])
        self.test_size_per_class = min([len(self.test_dir + '/' + x) for x in os.listdir(self.test_dir)])
        self.img_width = 160
        self.img_height = 160

        self.lr = 0.00008
        self.batch_size = 16
        self.epochs = 100
        self.workers = 4
        self.fine_tune_from = 100

        self.transfer_train = {
            'train_time': 0,
            'accuracy': -1,
            'loss': -1
        }
        self.fine_tune = {
            'train_time': 0,
            'accuracy': -1,
            'loss': -1
        }
        self.test = {

        }

        self.acc = None
        self.val_acc = None
        self.loss = None
        self.val_loss = None

    def create(self, lr=None,b=None,e=None,w=None,f=None):
        self.name = NameGenerator().get_name()
        self.history_dir = paths.ROOT_DIR + '/model/' + self.name + '/'
        self.history_location = paths.ROOT_DIR + '/history/' + self.name + ".json"
        if lr is not None:
            self.lr = lr
        if b is not None:
            self.batch_size = b
        if e is not None:
            self.epochs = e
        if w is not None:
            self.workers = w
        if f is not None:
            self.fine_tune_from = f
        self.cnn = self.create_cnn()

    def create_cnn(self):
        cnn = Cnn8(self.name, {
            'image_width': self.img_width,
            'image_height': self.img_height,
            'train_dir': self.train_dir,
            'validation_dir': self.validation_dir,
            'test_dir': self.test_dir,
            'batch_size': self.batch_size,
            'learning_rate': self.lr,
            'epochs': self.epochs,
            'workers': self.workers,
            'fine_tune_from': self.fine_tune_from,
            'transfer_train_params': self.transfer_train,
            'fine_tune_params': self.fine_tune,
            'test_params': self.test
        })
        cnn.prepare()
        return cnn

    def load(self, pid):
        self.name = pid
        self.history_location = paths.ROOT_DIR + '/history/' + self.name + ".json"
        with open(self.history_location, 'r') as params:
            self.__dict__ = json.load(params, object_hook=decoder_hook)
            print("Deserialization done")
        self.cnn = self.create_cnn()

    def save(self):
        with open(self.history_location, 'w') as history_file:
            json.dump(str(self.__dict__), history_file, indent=4, cls=Encoder)
        print("Serialization done")

    def make_transfer_train(self):
        self.transfer_train = self.cnn.transfer_train()
        self.save()
        self.finalize()

    def make_fine_tune(self):
        self.fine_tune = self.cnn.fine_tune()
        self.save()
        self.finalize()

    def make_test(self):
        cnn = TestCNN(self.name, {
            'model': self.cnn.cnn_dir + 'model.h5',
            'image_width': self.img_width,
            'image_height': self.img_height,
            'validation_size_per_class': self.validation_size_per_class,
            'validation_dir': self.validation_dir,
            'class_indices': self.cnn.cnn_dir + "class_indices.npy"
        })
        self.test = cnn.test()
        self.test['category_results'] = cnn.evaluate_tests()
        if not os.path.exists(self.cnn.cnn_dir + 'plots'):
            os.mkdir(self.cnn.cnn_dir + 'plots')
            for key, p in self.test['category_results'].items():
                copy2(p['plot'], self.cnn.cnn_dir + 'plots')
        self.save()

    def finalize(self):
        self.acc = self.cnn.acc
        self.val_acc = self.cnn.val_acc
        self.loss = self.cnn.loss
        self.val_loss = self.cnn.val_loss
        self.save()

        with open(self.cnn.cnn_dir + 'props.json', 'w') as history_file:
            json.dump(self.__dict__, history_file, indent=4, cls=Encoder)
        print("Serialization into cnn folder done")


controller = CNN8Controller()
controller.create()
controller.save()
# controller.load('Dorst')
controller.make_transfer_train()
controller.make_fine_tune()
controller.make_test()