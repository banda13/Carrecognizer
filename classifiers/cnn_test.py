import csv
import time

from keras import regularizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras.optimizers import RMSprop, Adam, SGD

from classifiers.cnn3 import Cnn3

class cnn3_test(object):

    def __init__(self):
        print("Initializing cnn3 teszt enviroment")
        base_classifier = Cnn3()

        self.shape = base_classifier.get_top_model_input_shape()
        self.num_classes = 20
        self.tests = []

        self.epochs = 1

        self.fieldnames = ['id', 'acc', 'val_acc', 'comment', 'time', 'epochs', 'loss', 'optimalizer', 'classes', 'lr', 'dropout', 'model']

        with open('mycsvfile.csv', 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
            writer.writeheader()


    def setup_models(self):

        print("Building test models")
        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0005),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'kis dropout + kis lr', 'model': model, 'epochs': self.epochs, 'dropout': 0.1, 'loss': 'categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes, 'lr': 0.0005})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'nagy dropout + nagy lr', 'model': model, 'epochs': self.epochs, 'dropout': 0.5, 'loss': 'categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes, 'lr': 0.001})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0001),
                      loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'sparse loss ','model': model,'epochs': self.epochs, 'dropout': 0.5, 'loss': 'sparse_categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes, 'lr': 0.0001})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'regularized' ,'model': model,'epochs': self.epochs, 'dropout': 0, 'loss': 'categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes, 'lr': 0.0001})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(4096, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'big model', 'model': model, 'epochs': self.epochs, 'dropout': 0,
                           'loss': 'categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes,
                           'lr': 0.0001})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(4096, activation='relu', kernel_regularizer=regularizers.l2(0.01)))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=SGD(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'big model', 'model': model, 'epochs': self.epochs, 'dropout': 0,
                           'loss': 'categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes,
                           'lr': 0.0001})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'hidden layer', 'model': model, 'epochs': self.epochs, 'dropout': 0.5, 'loss': 'categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes, 'lr': 0.0001})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.4))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=RMSprop(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'hidden layer ++', 'model': model, 'epochs': self.epochs,'dropout': 0.4, 'loss': 'categorical_crossentropy', 'optimalizer': 'RMSprop', 'classes': self.num_classes, 'lr': 0.0001})

        model = Sequential()
        model.add(Flatten(input_shape=self.shape, name="csakmert"))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer=Adam(lr=0.0001),
                      loss='categorical_crossentropy', metrics=['accuracy'])
        self.tests.append({'comment': 'Adam', 'model': model, 'epochs': self.epochs, 'dropout': 0.5, 'loss': 'categorical_crossentropy', 'optimalizer': 'Adam', 'classes': self.num_classes, 'lr': 0.0001})

    def run_tests(self):
        for test in self.tests:
            try:
                print("START: ", str(test))
                start = time.time()
                cnn = Cnn3()
                #cnn.epochs = test['epochs']
                #cnn.set_top_model(test['model'])
                #cnn.train_top_model()

                # test['id'] = cnn.id
                # test['acc'] = cnn.history.history['acc']
                # test['val_acc'] = cnn.history.history['val_acc']
                # test['time'] = time.time() - start

                test['id'] = str(cnn.id)
                test['acc'] = 3 #cnn.history.history['acc']
                test['val_acc'] = 3 #cnn.history.history['val_acc']
                test['time'] = time.time() - start
                test['model'] = str(test['model'])

                with open('mycsvfile.csv', 'a') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                    writer.writerow(test)
                print("----------------------------------------")

            except Exception as e:
                print("ERROR!!!!!!! ", str(e))

