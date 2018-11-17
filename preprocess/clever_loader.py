import os
import cv2
import paths
import random
import numpy as np
from enum import Enum
from shutil import copy2
from preprocess.pre_classification import VggPreClassifier


class PreClassificationState(Enum):
    NO = 0
    CLEANUP = 1
    CLASSIFY = 2


class LoaderFilter(Enum):
    NO = 0
    BLACK_AND_WHITE = 1
    GRAY_SCALE = 2
    EDGE_DETECTION = 3


class CleverLoader(object):
    data_soruce_dirs = [('hasznaltauto', paths.HASZNALT_DIR), ('autotrader', paths.TRADER_DIR)]
    train_dir = paths.TRAIN_DIR
    test_dir = paths.TEST_DIR

    def __init__(self, p_train, p_test, limit, f=LoaderFilter.NO, pre_filtering=PreClassificationState.NO, categories=None):
        self.pre_filtering = pre_filtering
        self.filter = f
        self.categories = categories
        self.p_train = p_train
        self.p_test = p_test
        self.limit = (limit if limit is not None else 1000)
        print("Clever loader initialized, active filter " + str(self.filter))
        print("P_train: %d; P_test: %s, limit: %d" % (self.p_train, self.p_test, self.limit))

    def load(self):
        print('Clever loading..')
        if self.pre_filtering == PreClassificationState.CLEANUP or self.pre_filtering == PreClassificationState.CLASSIFY:
            print("VGG pre classification activated")
            vgg = VggPreClassifier()
            if self.pre_filtering.CLASSIFY:
                vgg.prepare()
            vgg.cleanup()
        for source in self.data_soruce_dirs:
            print("Loading images from data source %s " % source[1])
            self.sort_train_vs_text(source[0], source[1], self.p_train, self.p_test,self.limit)

    def auto_canny(self, image, sigma=0.33):
        v = np.median(image)
        lower = int(max(0, (1.0 - sigma) * v))
        upper = int(min(255, (1.0 + sigma) * v))
        edged = cv2.Canny(image, lower, upper)
        return edged

    def tight_canny(self, image):
        return cv2.Canny(image, 225, 250)

    def wide_canny(self, image):
        return cv2.Canny(image, 10, 200)

    def sort_train_vs_text(self, s_name, s, p_train, p_test, limit):
        root_dir = s
        source = s_name
        if self.categories is None:
            self.categories = os.listdir(root_dir)
            print("%d category founded" % len(self.categories))
        for category in self.categories:
            files_in_category = os.listdir(root_dir + category)

            if len(files_in_category) < limit:
                print("Category %s skipped because of the lack of images: %d" % (category, len(files_in_category)))
                continue

            category_length = len(files_in_category)
            random.shuffle(files_in_category)

            train_count = int(p_train * limit)
            test_count = int(p_test * limit)

            print("%d train and %d test data determined in category %s in %s" % (
                train_count, test_count, category, source))

            if not os.path.exists(self.train_dir + category + "/"):
                os.makedirs(self.train_dir + category + "/")
            if not os.path.exists(self.test_dir + category + "/"):
                os.makedirs(self.test_dir + category + "/")

            for i in range(limit):
                image_source_dir = root_dir + category + "/" + files_in_category[i]
                if i <= train_count:
                    destination = self.train_dir + category + "/" + source + files_in_category[i]
                else:
                    destination = self.test_dir + category + "/" + source + files_in_category[i]
                if self.filter == LoaderFilter.BLACK_AND_WHITE:
                    im_gray = cv2.imread(image_source_dir, cv2.IMREAD_GRAYSCALE)
                    (thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                    cv2.imwrite(destination, im_gray)
                elif self.filter == LoaderFilter.EDGE_DETECTION:
                    image = cv2.imread(image_source_dir)
                    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                    blurred = cv2.GaussianBlur(gray, (3, 3), 0)
                    edges = self.auto_canny(blurred)
                    cv2.imwrite(destination, edges)
                elif self.filter == LoaderFilter.GRAY_SCALE:
                    image = cv2.imread(image_source_dir, 0)
                    cv2.imwrite(destination, image)
                elif self.filter == LoaderFilter.NO:
                    if i <= train_count:
                        copy2(image_source_dir,destination)
                    else:
                        copy2(image_source_dir,destination)
                else:
                    print("Fatal error, please specify a valid preprocessing filter")

            print("%s category done in %s" % (category, source))


loader = CleverLoader(0.8, 0.2, 1000, f=LoaderFilter.EDGE_DETECTION)
loader.load()

