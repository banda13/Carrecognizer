from classifiers.cnn4 import Cnn4
from classifiers.cnn3 import Cnn3
from classifiers.cnn2 import Cnn2
from random import sample
import os

from classifiers.cnn_test import cnn3_test
from input.data_loader import sort_into_train_and_test
from input.data_utils import summ_categories

sort_into_train_and_test(0.8, 0.2, 10000, 100)