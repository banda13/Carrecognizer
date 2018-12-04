import os
import random
import numpy as np

from keras import applications
from keras.engine.saving import load_model
from keras_preprocessing.image import load_img, img_to_array

import matplotlib.pyplot as plt

import paths


class TestCNN(object):

    plot_dir = paths.ROOT_DIR + '/statistics/subplots/'

    def __init__(self, pid, params):
        self.pid = pid
        self.model_path = params['model']
        self.image_width, self.image_height = params['image_width'], params['image_height']

        self.layer_tracked = params['tracked_layer']
        self.test_count_per_class = params['test_count_per_class']
        self.accuracy = params['accuracy']
        self.category_results = params['category_results']
        self.validation_dir = params['test_dir']
        self.class_indices_dir = params['class_indices']
        self.results = params['results']
        self.idx_results = []

        print("TestCNN initialized")

    def test(self):
        print("Testing CNN started..")

        model = load_model(self.model_path)
        class_dictionary = np.load(self.class_indices_dir).item()
        print("Model loaded")

        categories = os.listdir(self.validation_dir)
        num_categories = len(categories)
        category_results = []
        print("Testing %d category" % len(categories))
        for category in categories:
            print("Testing %s" % category)

            images = random.sample(os.listdir(self.validation_dir + "/" + category), self.test_count_per_class)
            match = 0
            predictions_list = []
            idx_prediction_list = []
            for img in images:
                image = load_img(self.validation_dir + "/" + category + "/" + img, target_size=(self.image_width, self.image_height))
                image = img_to_array(image)
                image = image / 255
                image = np.expand_dims(image, axis=0)

                prediction = model.predict(image).reshape(num_categories)
                idx_prediction = np.argsort(-prediction, axis=0)
                inv_map = {v: k for k, v in class_dictionary.items()}
                label = inv_map[idx_prediction[0]]

                if label == category:
                    match += 1

                predictions_list.append(prediction)
                idx_prediction_list.append(idx_prediction)
            category_results.append(predictions_list)
            self.idx_results.append(idx_prediction_list)

            avg_prop = 0 # TODO
            similar_categories = {} # TODO with propabilities, and weight it based on
            accuracy = match / len(images)

            print("Testing ended for category %s, accuracy: %f" % (category, accuracy))
            self.category_results[category] = {
                'match' : match,
                'accuracy': accuracy,
                'probabilities' : predictions_list,
                'avg_probabilities' : avg_prop,
                'similar_categories' : similar_categories
            }
        self.results = category_results
        self.evaluate_tests()

    def evaluate_tests(self):
        class_dictionary = np.load(self.class_indices_dir).item()
        inv_map = {v: k for k, v in class_dictionary.items()}
        labels = class_dictionary.keys()
        for i in range(len(self.results)):
            category = inv_map[i]
            res = np.array(self.results[i])
            means = []
            for col in res.T:
                means.append(np.mean(col))
            np_means = np.array(means)
            plt.title(category)
            plt.ylabel('Percentage')
            plt.bar(labels, np_means)
            plt.xticks(rotation=90)
            plt.savefig(TestCNN.plot_dir + self.pid + '_' + category + ".jpg")
            plt.close()