import keras

from PIL import ImageFile

from keras import backend as K
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.layers import Input, Lambda, Dense, BatchNormalization, Flatten
from keras.layers import Convolution2D, MaxPooling2D, Dropout
from keras.models import Model
from keras.optimizers import Adam, Adagrad, SGD, RMSprop
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

class Cnn(object):

    batch_size = 24
    image_size = (128, 128)
    input_shape = image_size + (3,)
    NUM_CLASSES = 2

    def __init__(self, images, labels):
        input_tensor = Input(shape=self.input_shape)

        # Conv block 64 filters
        x = Convolution2D(64, 3)(input_tensor)
        x = Convolution2D(64, 3)(x)
        x = MaxPooling2D()(x)

        # Conv block 32 filters
        x = Convolution2D(32, 3)(x)
        x = Convolution2D(32, 3)(x)
        x = MaxPooling2D()(x)
        x = Flatten()(x)

        # Dense block for classification
        x = Dense(32, activation='relu')(x)
        x = Dense(32, activation='relu')(x)
        pred_layer = Dense(self.NUM_CLASSES, activation='softmax', name='predictions')(x)
        # Build and compile model
        model = Model(inputs=input_tensor, outputs=pred_layer)
        model.compile(optimizer=SGD(), loss='categorical_crossentropy', metrics=['accuracy'])
        self.model = model

        self.model.summary()

        ImageFile.LOAD_TRUNCATED_IMAGES = True
        image_gen = ImageDataGenerator(rescale=1.0 / 255)
        train_iterator = image_gen.flow_from_directory("data/train/",
                                                       batch_size=24,
                                                       target_size=(128, 128))
        val_iterator = image_gen.flow_from_directory("data/test",
                                                     batch_size=1,
                                                     target_size=(128, 128),
                                                     shuffle=False)
        val_steps = val_iterator.n  # number of val images
        # Train the model
        model.fit_generator(train_iterator,
                            steps_per_epoch=10,
                            epochs=50,
                            validation_data=val_iterator,
                            validation_steps=val_steps)

        # Slow down learning rate and continue to train
        model.optimizer.lr = 1E-5
        model.fit_generator(train_iterator,
                            steps_per_epoch=10,
                            epochs=100,
                            validation_data=val_iterator,
                            validation_steps=val_steps)

