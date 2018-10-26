import math
import numpy as np
from PIL import ImageFile
from keras.preprocessing.image import ImageDataGenerator
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense
from keras import applications

# dimensions of our images.
from keras.utils import to_categorical

img_width, img_height = 224, 224

top_model_weights_path = 'bottleneck_fc_model.h5'
train_data_dir = '../data/train'
validation_data_dir = '../data/test'
epochs = 50
batch_size = 16
num_classes = 19


def save_bottlebeck_features():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    datagen = ImageDataGenerator(rescale=1. / 255)

    # build the VGG16 network
    model = applications.VGG16(include_top=False, weights='imagenet')

    generator = datagen.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)

    nb_train_samples = len(generator.filenames)
    bottleneck_features_train = model.predict_generator(
        generator, int(math.ceil(nb_train_samples / batch_size)))
    np.save('bottleneck_features_train.npy',
            bottleneck_features_train)

    generator = datagen.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)
    nb_validation_samples = len(generator.filenames)
    print(int(math.ceil(nb_train_samples / batch_size)))
    print(int(math.ceil(nb_validation_samples / batch_size)))
    bottleneck_features_validation = model.predict_generator(
        generator, int(math.ceil(nb_validation_samples / batch_size)))
    np.save('bottleneck_features_validation.npy',
            bottleneck_features_validation)


def train_top_model():
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    datagen_top = ImageDataGenerator(
        rescale=1. / 255)
    generator_top = datagen_top.flow_from_directory(
        train_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)

    train_data = np.load('bottleneck_features_train.npy')
    train_labels = generator_top.classes
    train_labels = to_categorical(train_labels, num_classes=num_classes)

    generator_top = datagen_top.flow_from_directory(
        validation_data_dir,
        target_size=(img_width, img_height),
        batch_size=batch_size,
        class_mode=None,
        shuffle=False)

    validation_data = np.load('bottleneck_features_validation.npy')
    validation_labels = generator_top.classes
    validation_labels = to_categorical(validation_labels, num_classes=num_classes)

    model = Sequential()
    model.add(Flatten(input_shape=train_data.shape[1:]))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(optimizer='rmsprop',
                  loss='categorical_crossentropy', metrics=['accuracy'])

    model.fit(train_data, train_labels,
              epochs=epochs,
              batch_size=batch_size,
              validation_data=(validation_data, validation_labels))
    model.save_weights(top_model_weights_path)


save_bottlebeck_features()
train_top_model()