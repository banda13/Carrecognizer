from classifiers.cnn import Cnn
from classifiers.classifier_utils import classes_stat, image_plots
from classifiers.cnn2 import Cnn2
from loader import Loader

import keras
from keras import backend as K
from keras.applications.vgg16 import VGG16, preprocess_input
from keras.layers import Input, Lambda, Dense, BatchNormalization, Flatten
from keras.layers import Convolution2D, MaxPooling2D, Dropout
from keras.models import Model
from keras.optimizers import Adam, Adagrad, SGD, RMSprop
from keras.utils import to_categorical
from keras.preprocessing.image import ImageDataGenerator, array_to_img, img_to_array, load_img

#loader = Loader()
#images, labels = loader.load_train_data()
#print(images.shape)
#cnn = Cnn(None, None)
cnn = Cnn2()
cnn.train()
