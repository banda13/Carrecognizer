import os
import random
import time

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

        self.test_count_per_class = params['test_count_per_class']
        self.accuracy = params.get('accuracy', 0)
        self.top3_accuracy = params.get('top3_accuracy', 0)
        self.avg_probability = params.get('probability', 0)
        self.category_results = params.get('category_results', {})
        self.validation_dir = params['test_dir']
        self.class_indices_dir = params['class_indices']
        self.results = params.get('results', None)
        self.idx_results = []
        self.test_time = params.get('test_time', None)

        print("TestCNN initialized")

    def test(self):
        print("Testing CNN started..")
        start_time = time.time()

        model = load_model(self.model_path)
        class_dictionary = np.load(self.class_indices_dir).item()
        inv_map = {v: k for k, v in class_dictionary.items()}
        reverse_inv_map = dict(zip(inv_map.values(),inv_map.keys()))
        print("Model loaded")

        categories = os.listdir(self.validation_dir)
        num_categories = len(categories)
        category_results = []
        probabilities = []
        accucacies = []
        top3_accuracies = []
        print("Testing %d category" % len(categories))
        for category in categories:
            print("Testing %s" % category)

            images = random.sample(os.listdir(self.validation_dir + "/" + category), self.test_count_per_class)
            match = 0
            top3_match = 0
            predictions_list = []
            idx_prediction_list = []
            for img in images:
                image = load_img(self.validation_dir + "/" + category + "/" + img, target_size=(self.image_width, self.image_height))
                image = img_to_array(image)
                image = image / 255
                image = np.expand_dims(image, axis=0)

                prediction = model.predict(image).reshape(num_categories)
                idx_prediction = np.argsort(-prediction, axis=0)
                label = inv_map[idx_prediction[0]]
                top3_label = [inv_map[idx_prediction[0]], inv_map[idx_prediction[1]], inv_map[idx_prediction[2]]]

                if label == category:
                    match += 1
                if category in top3_label:
                    top3_match += 1

                predictions_list.append(prediction)
                idx_prediction_list.append(idx_prediction)
            category_results.append(predictions_list)
            self.idx_results.append(idx_prediction_list)

            means = []
            prob_max = []
            prob_min = []
            for cat in np.array(category_results).T:
                means.append(np.mean(cat))
                prob_max.append(np.max(cat))
                prob_min.append(np.min(cat))

            idx = reverse_inv_map[category]
            category_mean = means[idx]
            category_max = prob_max[idx]
            category_min = prob_min[idx]
            accuracy = match / len(images)
            top3_accuracy = top3_match / len(images)

            probabilities.append(category_mean)
            accucacies.append(accuracy)
            top3_accuracies.append(top3_accuracy)

            print("Testing ended for category %s, accuracy: %f" % (category, accuracy))
            self.category_results[category] = {
                'match' : float(match),
                'accuracy': float(accuracy),
                'top3_accuracy': float(top3_accuracy),
                # 'probabilities' : predictions_list,
                'avg_probabilities' : float(category_mean),
                'max_probabilities' : float(category_max),
                'min_probabilities' : float(category_min)
            }
        self.results = category_results
        self.accuracy = float(np.mean(np.array(accucacies)))
        self.top3_accuracy = float(np.mean(np.array(top3_accuracies)))
        self.avg_probability = float(np.mean(np.array(probabilities)))
        self.test_time = time.time() - start_time
        self.evaluate_tests()
        return {
            'accuracy': self.accuracy,
            'top3_accuracy': self.top3_accuracy,
            'avg_probability': self.avg_probability,
            'run_time': self.test_time,
            'category_results': self.category_results
        }

    def evaluate_tests(self):
        plt.close()
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
            img_title = TestCNN.plot_dir + self.pid + '_' + category + ".jpg"
            plt.savefig(img_title)
            plt.close()

            self.category_results[category]['plot'] = img_title
        return self.category_results
