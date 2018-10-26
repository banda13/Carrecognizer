import json
import time

import matplotlib.pyplot as plt
from keras import applications, Model
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
from keras.models import Sequential
from keras.layers import Dropout, Flatten, Dense, regularizers, Convolution2D, MaxPooling2D

# path to the model weights files.
weights_path = 'pre_train/vgg16_weights.h5'
top_model_weights_path = '../model/bottleneck/bottleneck_080e858c-1fb9-42f8-a933-fa3c10900367.h5'
# dimensions of our images.
img_width, img_height = 224, 224

train_data_dir = '../data//train'
validation_data_dir = '../data/test'
epochs = 25
batch_size = 16
num_classes = 19

# build the VGG16 network
base_model = applications.VGG16(weights='imagenet', include_top=False, input_shape=(img_width, img_height, 3))
print('Model loaded.')

# build a classifier model to put on top of the convolutional model
top_model = Sequential()
top_model.add(Convolution2D(128, 3, 3, input_shape=base_model.output_shape[1:], activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(MaxPooling2D(pool_size=(2, 2)))

top_model.add(Flatten())
top_model.add(Dense(128, activation='relu'))
top_model.add(Dropout(0.5))
top_model.add(Dense(num_classes, activation='softmax', kernel_regularizer=regularizers.l2(0.01)))

# note that it is necessary to start with a fully-trained
# classifier, including the top classifier,
# in order to successfully do fine-tuning
top_model.load_weights(top_model_weights_path)

# add the model on top of the convolutional base
model = Model(input=base_model.input, output=top_model(base_model.output))

# set the first 25 layers (up to the last conv block)
# to non-trainable (weights will not be updated)
for layer in model.layers[:15]:
    layer.trainable = False

# compile the model with a SGD/momentum optimizer
# and a very slow learning rate.
model.compile(optimizer=optimizers.SGD(lr=1e-5, momentum=0.5), loss='categorical_crossentropy', metrics=['accuracy'])

# prepare data augmentation configuration
train_datagen = ImageDataGenerator(
    rescale=1. / 255,
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True)

test_datagen = ImageDataGenerator(rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    train_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

nb_train_samples = len(train_generator.filenames)

validation_generator = test_datagen.flow_from_directory(
    validation_data_dir,
    target_size=(img_height, img_width),
    batch_size=batch_size,
    class_mode='categorical')

nb_validation_samples = len(validation_generator.filenames)

# fine-tune the model
try:
    history = model.fit_generator(
        train_generator,
        samples_per_epoch=nb_train_samples // batch_size,
        epochs=epochs,
        validation_data=validation_generator,
        nb_val_samples=nb_validation_samples // batch_size)

    model.save("asd.h5")

    plt.figure(1)
    plt.subplot(211)
    plt.plot(history.history['acc'])
    plt.plot(history.history['val_acc'])
    plt.title('model accuracy')
    plt.ylabel('accuracy')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')

    plt.subplot(212)
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'test'], loc='upper left')
    plt.savefig("statistics/" + 'asd' + "_" + str(time.time()) + ".png")

    with open('statistics/' + 'asd' + "_" + str(time.time()) + '.json', 'w') as outfile:
        json.dump(history.history, outfile, indent=4)
except Exception as e:
    model.save("asd.h5")