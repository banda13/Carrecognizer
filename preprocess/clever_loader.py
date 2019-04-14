import os
from collections import Counter

import cv2
import paths
import random
import numpy as np
from enum import Enum
import matplotlib.pyplot as plt

from preprocess.clever_pre_classifier import MyPreClassifier
from preprocess.pre_classification import VggPreClassifier


class PreClassificationState(Enum):
    NO = 0
    VGG_CLEANUP = 1
    VGG_CLASSIFY = 2
    MY_CLEANUP = 4
    MY_CLASSIFY = 5
    JUST_COPY = 6


class LoaderFilter(Enum):
    NO = 0
    BLACK_AND_WHITE = 1
    GRAY_SCALE = 2
    EDGE_DETECTION = 3
    BACKGROUND_SUBTRACT = 4
    LAPLACE_GRADIENT = 5


class CleverLoader(object):
    # data_soruce_dirs = [('autoscout', paths.SCOUT_DIR), ('autotrader', paths.TRADER_DIR), ('hasznaltauto', paths.HASZNALT_DIR)] # ,
    #TODO testing categorizetion on the new categories
    data_soruce_dirs = [('autoscout', paths.N_SCOUT_DIR)]
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
        if not self.pre_filtering == PreClassificationState.JUST_COPY:
            if self.pre_filtering == PreClassificationState.VGG_CLEANUP or self.pre_filtering == PreClassificationState.VGG_CLASSIFY:
                print("VGG pre classification activated")
                vgg = VggPreClassifier()
                if self.pre_filtering == PreClassificationState.VGG_CLASSIFY:
                    vgg.prepare()
                vgg.cleanup()

            if self.pre_filtering == PreClassificationState.MY_CLASSIFY or self.pre_filtering == PreClassificationState.MY_CLEANUP:
                print("My pre classifier activated")
                pre_class = MyPreClassifier()
                if self.pre_filtering == PreClassificationState.MY_CLASSIFY:
                    pre_class.prepare()
                pre_class.cleanup()

        categorie_summs, source_categories_summs = self.summ_categoris()
        for category in categorie_summs.keys():
            if category == 'deleted':
                continue

            img_counter = self.limit
            summ_in_category = sum(c[category] for c in source_categories_summs)
            p = self.limit / float(summ_in_category)
            i = 0
            for cat_source in source_categories_summs:
                if category in cat_source:
                    category_count = round(cat_source[category] * p)
                    img_counter -= category_count

                    if category_count > 0:
                        print("Loading images from data source %s in category : %s" % (self.data_soruce_dirs[i][1], category))
                        self.sort_train_vs_text(self.data_soruce_dirs[i][0], self.data_soruce_dirs[i][1], self.p_train, self.p_test, category_count, [category])
                    i += 1
                else:
                    print("%s category missing from source %s " % (category, self.data_soruce_dirs[i][1]))

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

    def fordeground_extraction(self, image):
        mask = np.zeros(image.shape[:2], np.uint8)

        bgdModel = np.zeros((1, 65), np.float64)
        fgdModel = np.zeros((1, 65), np.float64)

        rect = (50, 50, 450, 290)
        cv2.grabCut(image, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)

        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
        img = image * mask2[:, :, np.newaxis]
        return img

    def summ_categoris(self):
        cary_by_dirs = []
        input_summ = Counter()
        for source in self.data_soruce_dirs:
            cars = {}
            for type in os.listdir(source[1]):
                count = len(os.listdir(source[1] + type))
                # print("Category: %s, Sample: %d " % (type, count))
                cars[type] = count
            cary_by_dirs.append(cars)
            input_summ += Counter(cars)
        input_summ_with_limit = {}
        for key, value in input_summ.items():
            if int(value) > self.limit:
                print(key + ": " + str(value))
                input_summ_with_limit[key] = value
        return input_summ_with_limit, cary_by_dirs

    def sort_train_vs_text(self, s_name, s, p_train, p_test, limit, sorting_categories):
        root_dir = s
        source = s_name
        mog2 = cv2.createBackgroundSubtractorMOG2()
        if sorting_categories is None:
            categories = os.listdir(root_dir)
            print("%d category founded" % len(categories))
        else:
            categories = sorting_categories
        for category in categories:
            try:
                files_in_category = os.listdir(root_dir + category)
            except FileNotFoundError:
                print("Skip category %s " % category)
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
                try:
                    image = None
                    if self.filter == LoaderFilter.BLACK_AND_WHITE:
                        image = cv2.imread(image_source_dir, cv2.IMREAD_GRAYSCALE)
                        (thresh, im_bw) = cv2.threshold(image, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                    elif self.filter == LoaderFilter.EDGE_DETECTION:
                        image = cv2.imread(image_source_dir)
                        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                        blurred = cv2.GaussianBlur(gray, (3, 3), 0)
                        image = self.auto_canny(blurred)
                    elif self.filter == LoaderFilter.BACKGROUND_SUBTRACT:
                        image = cv2.imread(image_source_dir)
                        # TODO did not find any good algorithm
                    elif self.filter == LoaderFilter.LAPLACE_GRADIENT:
                        img = cv2.imread(image_source_dir)
                        # TODO
                    elif self.filter == LoaderFilter.GRAY_SCALE:
                        image = cv2.imread(image_source_dir, cv2.IMREAD_GRAYSCALE)
                    elif self.filter == LoaderFilter.NO:
                        image = cv2.imread(image_source_dir)
                    else:
                        print("Fatal error, please specify a valid preprocessing filter")
                    cv2.imwrite(destination, image)
                except Exception as e:
                    print(e)

            print("%s category done in %s" % (category, source))


# loader = CleverLoader(0.8, 0.2, 20000, f=LoaderFilter.NO)
# loader.load()