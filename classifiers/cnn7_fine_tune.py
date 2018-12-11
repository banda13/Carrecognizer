import json
import time

import matplotlib.pyplot as plt
from keras import applications, Model
from keras.callbacks import ModelCheckpoint, History, EarlyStopping, RemoteMonitor
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, regularizers, Convolution2D, MaxPooling2D

#top_model_weights_path = '../model/bottleneck/bottleneck_080e858c-1fb9-42f8-a933-fa3c10900367.h5'
#top_model_weights_path = '../model/bottleneck/bottleneck_2984277f-51b3-4567-b55a-83fb4c1874be.h5'
#top_model_weights_path = '../model/bottleneck/bottleneck_215cde26-ad77-4c58-abe3-f26098878e0c.h5'
#top_model_weights_path = '../model/bottleneck/bottleneck_9c292261-370a-4cc4-b2b8-bf071ad22895.h5'
import paths


class Cnn7(object):

    def __init__(self, pid, core_params, classification_params, in_params, out_params):
        self.img_width, self.img_height = classification_params['image_width'], classification_params['image_height']
        self.id = pid
        print("Using cnn7 classifier with id ", str(self.id))
        self.train_dir = core_params['train_dir']
        self.test_dir = core_params['test_dir']

        self.epochs = in_params['epochs']
        self.batch_size = in_params['batch_size']
        self.augmentation = in_params['augmentation']
        self.num_classes = in_params['num_classes']
        self.frozen_layers = in_params['frozen_layers']
        self.learning_rate = in_params['learning_rate']
        # self.momentum = in_params['momentum']

        # self.top_model = in_params['top_model']
        self.top_model = Sequential()
        # model.add(Convolution2D(512, 3, 3, input_shape=(4, 4, 512), activation='relu'))
        # model.add(Dropout(0.1))
        # model.add(MaxPooling2D(pool_size=(2, 2)))

        self.top_model.add(Flatten(input_shape=(4, 4, 512)))
        self.top_model.add(Dense(512, activation='relu'))
        self.top_model.add(Dropout(0.1))
        self.top_model.add(Dense(256, activation='relu'))
        self.top_model.add(Dropout(0.1))
        self.top_model.add(Dense(self.num_classes, activation='softmax', kernel_regularizer=regularizers.l2(0.001)))
        self.top_model_weights_path = in_params['top_model_weights']
        self.model_path = in_params['model']

        self.model = None
        self.history = None
        self.out_params = out_params

    def fine_tune(self):
        self.base_model = applications.VGG19(weights='imagenet', include_top=False, input_shape=(self.img_width, self.img_height, 3))
        print('Base model loaded.')

        self.top_model.load_weights(self.top_model_weights_path)
        print("Top model weights loaded")

        self.model = Model(input=self.base_model.input, output=self.top_model(self.base_model.output))

        for layer in self.model.layers[:self.frozen_layers]:
            layer.trainable = False
        print("%d layer unfreezed, %d freezed" % (self.frozen_layers, (len(self.model.layers) - self.frozen_layers)))

        print("Compiling model")
        self.model.compile(optimizer=optimizers.SGD(lr=self.learning_rate, momentum=0.5), loss='categorical_crossentropy', metrics=['accuracy'])

        # train_datagen = ImageDataGenerator(self.augmentation)
        train_datagen = ImageDataGenerator(
                # rotation_range= 30,
                # width_shift_range= 0.2,
                # height_shift_range= 0.2,
                # fill_mode= 'nearest',
                shear_range= 0.2,
                zoom_range= 0.2,
                horizontal_flip= True,
                rescale= 1. / 255)

        test_datagen = ImageDataGenerator(rescale=1. / 255)

        train_generator = train_datagen.flow_from_directory(
            self.train_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical')

        nb_train_samples = len(train_generator.filenames)

        validation_generator = test_datagen.flow_from_directory(
            self.test_dir,
            target_size=(self.img_height, self.img_width),
            batch_size=self.batch_size,
            class_mode='categorical')

        nb_validation_samples = len(validation_generator.filenames)

        self.checkpointer = ModelCheckpoint(filepath=self.top_model_weights_path, verbose=1, save_best_only=True)
        self.history = History()
        callbacks = [EarlyStopping(monitor='val_loss',
                                   min_delta=0,
                                   patience=5,
                                   verbose=0, mode='auto'),
                     self.history,self.checkpointer]
        try:
            self.history = self.model.fit_generator(
                train_generator,
                samples_per_epoch=nb_train_samples // self.batch_size,
                epochs=self.epochs,
                callbacks=callbacks,
                validation_data=validation_generator,
                nb_val_samples=nb_validation_samples // self.batch_size)
        except KeyboardInterrupt:
            print("Training stopped..")

        self.model.save(self.model_path)

        score = self.model.evaluate_generator(validation_generator, nb_validation_samples // self.batch_size)
        self.out_params['loss'] = score[0]
        self.out_params['accuracy'] = score[1]
        print("Training model ended, model saved")

    def evaluate(self):
        print("Evaluation fine tuned model")
        plt.figure(2)
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

        stat_plot_dir = paths.STAT_DIR + "/fine_" + str(self.id) + "_" + str(time.time()) + ".png"
        plt.savefig(stat_plot_dir)
        self.out_params['plot'] = stat_plot_dir
        self.out_params['history'] = self.history.history

        with open(paths.STAT_DIR + str(self.id) + "_" + str(time.time()) + '.json', 'w') as outfile:
            json.dump(self.history.history, outfile, indent=4)

