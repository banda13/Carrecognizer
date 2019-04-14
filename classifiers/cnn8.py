import os
import time
import numpy as np
import matplotlib.pyplot as plt

from PIL import ImageFile
from keras import Sequential, Model
from keras.applications import MobileNetV2
from keras.callbacks import EarlyStopping, ModelCheckpoint, History, TensorBoard
from keras.engine.saving import load_model
from keras.layers import GlobalAveragePooling2D, Dense, Dropout
from keras.optimizers import RMSprop
from keras.regularizers import l2
from keras_preprocessing.image import ImageDataGenerator

import paths


class Cnn8(object):

    def __init__(self, pid, params):
        self.img_width, self.img_height = params['image_width'], params['image_height']
        self.id = pid
        print("Using cnn8 classifier with id ", str(self.id))
        self.train_dir = params['train_dir']
        self.validation_dir = params['validation_dir']
        self.test_dir = params['test_dir']

        self.cnn_dir = paths.ROOT_DIR + 'model/' + self.id + '/'

        self.batch_size = params['batch_size']
        self.learning_rate = params['learning_rate']
        self.epochs = params['epochs']
        self.workers = params['workers']

        self.fine_tune_from = params['fine_tune_from']

        self.train_generator, self.validation_generator, self.test_generator = None, None, None
        self.transfer_train_time = params['transfer_train_params']['train_time']
        self.tt_acc = params['transfer_train_params']['accuracy']
        self.tt_loss = params['transfer_train_params']['loss']

        self.fine_tune_time = params['fine_tune_params']['train_time']
        self.ft_acc = params['fine_tune_params']['accuracy']
        self.ft_loss = params['fine_tune_params']['loss']

        # TODO test params

    def prepare(self):
        print("Setting up CNN v8..")
        if not os.path.exists(self.cnn_dir):
            os.makedirs(self.cnn_dir)

        ImageFile.LOAD_TRUNCATED_IMAGES = True

        # Rescale all images by 1./255 and apply image augmentation
        train_datagen = ImageDataGenerator(
            shear_range=0.2,
            zoom_range=0.2,
            rotation_range=20,
            width_shift_range=0.2,
            height_shift_range=0.2,
            rescale=1. / 255)

        validation_datagen = ImageDataGenerator(rescale=1. / 255)

        test_datagen = ImageDataGenerator(rescale=1. / 255)

        self.train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical')

        self.validation_generator = validation_datagen.flow_from_directory(
            self.validation_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical')

        self.test_generator = test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.img_width, self.img_height),
            batch_size=self.batch_size,
            class_mode='categorical')

        print("Generators are ready, saving class indices")
        np.save((self.cnn_dir + "class_indices.npy"), self.train_generator.class_indices)
        self.IMG_SHAPE = (self.img_width, self.img_height, 3)
        self.num_classes = len(self.train_generator.class_indices)

        print("Creating transfer train model")

        # Create the base model from the pre-trained model MobileNet V2 on imagenet data
        self.base_model = MobileNetV2(input_shape=self.IMG_SHAPE,
                                      include_top=False,
                                      weights='imagenet')
        #  its already trained, we just use the features
        self.base_model.trainable = False

        top_model = Sequential()
        top_model.add(GlobalAveragePooling2D())
        top_model.add(Dense(128, activation='relu', kernel_regularizer=l2(0.01)))
        top_model.add(Dropout(0.5))
        top_model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
        top_model.add(Dropout(0.5))
        top_model.add(Dense(64, activation='relu', kernel_regularizer=l2(0.01)))
        top_model.add(Dropout(0.5))
        top_model.add(Dense(self.num_classes, activation='softmax', kernel_regularizer=l2(0.01)))
        self.model = Model(input=self.base_model.input, output=top_model(self.base_model.output))
        self.model.compile(optimizer=RMSprop(lr=self.learning_rate),
                           loss='categorical_crossentropy',
                           metrics=['accuracy'])
        print("Model created for id %s" % self.id)
        self.steps_per_epoch = self.train_generator.n // self.batch_size
        self.validation_steps = self.validation_generator.n // self.batch_size
        self.test_steps = self.test_generator.n // self.batch_size

        print("Initializing callbacks")
        self.callbacks = [EarlyStopping(monitor='val_loss',
                                        min_delta=0,
                                        patience=3,
                                        verbose=0, mode='auto'),
                          ModelCheckpoint(filepath=(self.cnn_dir + "model-weights.h5"), verbose=1, save_best_only=True),
                          History(),
                          TensorBoard(log_dir="logs/{}".format(self.id))]
        try:
            self.model.load_weights((self.cnn_dir + "model-weights.h5"))
            print("Found weights for %s, loading them and continue training" % self.id)
        except OSError:
            pass
        print("Cnn is ready for train")

    def transfer_train(self):
        start_time = time.time()
        print("Transfer training started")
        self.history = self.model.fit_generator(self.train_generator,
                                                steps_per_epoch=self.steps_per_epoch,
                                                epochs=self.epochs,
                                                workers=self.workers,
                                                callbacks=self.callbacks,
                                                validation_data=self.validation_generator,
                                                validation_steps=self.validation_steps)
        self.tt_loss, self.tt_acc = self.model.evaluate_generator(self.test_generator,
                                                                                       self.test_steps)
        self.transfer_train_time += time.time() - start_time
        print("Transfer train ended at: %d sec" % self.transfer_train_time)

        self.model.save(self.cnn_dir + 'model.h5')
        self.acc = self.history.history['acc']
        self.val_acc = self.history.history['val_acc']

        self.loss = self.history.history['loss']
        self.val_loss = self.history.history['val_loss']
        self.create_plot('transfer_train', self.acc, self.val_acc,
                         self.loss, self.val_loss)

    def create_plot(self, name, acc, val_acc, loss, val_loss):
        plt.figure(figsize=(8, 8))
        plt.subplot(2, 1, 1)
        plt.plot(acc, label='Training Accuracy')
        plt.plot(val_acc, label='Validation Accuracy')
        plt.legend(loc='lower right')
        plt.ylabel('Accuracy')
        plt.ylim([min(plt.ylim()), 1])
        plt.title('Training and Validation Accuracy')

        plt.subplot(2, 1, 2)
        plt.plot(loss, label='Training Loss')
        plt.plot(val_loss, label='Validation Loss')
        plt.legend(loc='upper right')
        plt.ylabel('Cross Entropy')
        plt.ylim([0, max(plt.ylim())])
        plt.title('Training and Validation Loss')
        plt.savefig(self.cnn_dir + name + ".png")
        plt.close()

    def fine_tune(self):
        start_time = time.time()
        print("Fine tune started")
        self.base_model.trainable = True

        # Let's take a look to see how many layers are in the base model
        print("Unfreezing %d layer from %d: " % (self.fine_tune_from, len(self.base_model.layers)))

        # Freeze all the layers before the `fine_tune_at` layer
        for layer in self.base_model.layers[:self.fine_tune_from]:
            layer.trainable = False

        # Recomiple model
        self.model.compile(loss='categorical_crossentropy',
                           optimizer=RMSprop(lr=2e-5),
                           metrics=['accuracy'])

        history_fine = self.model.fit_generator(self.train_generator,
                                                steps_per_epoch=self.steps_per_epoch,
                                                epochs=self.epochs,
                                                callbacks=self.callbacks,
                                                workers=4,
                                                validation_data=self.validation_generator,
                                                validation_steps=self.validation_steps)
        self.ft_loss, self.ft_acc = self.model.evaluate_generator(self.test_generator,self.test_steps)
        self.model.save(self.cnn_dir + 'model.h5')
        self.fine_tune_time += time.time() - start_time
        print("Fine tuning model ended %d" % self.fine_tune_time)

        self.acc += history_fine.history['acc']
        self.val_acc += history_fine.history['val_acc']

        self.loss += history_fine.history['loss']
        self.val_loss += history_fine.history['val_loss']
        self.create_plot('fine_tune', self.acc, self.val_acc, self.loss, self.val_loss)

    def test(self):
        start_time = time.time()
        print("Test started")
