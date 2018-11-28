import os
import random
import numpy as np

from keras import applications
from keras.engine.saving import load_model
from keras_preprocessing.image import load_img, img_to_array


class TestCNN(object):

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

        print("TestCNN initialized")

    def test(self):
        print("Testing CNN started..")

        model = load_model(self.model_path)
        class_dictionary = np.load(self.class_indices_dir).item()
        print("Model loaded")

        categories = os.listdir(self.validation_dir)
        print("Testing %d category" % len(categories))
        for category in categories:
            print("Testing %s" % category)

            images = random.sample(os.listdir(self.validation_dir + "/" + category), self.test_count_per_class)
            match = 0
            predictions_list = [{}] * self.layer_tracked
            for img in images:
                image = load_img(self.validation_dir + "/" + category + "/" + img, target_size=(self.image_width, self.image_height))
                image = img_to_array(image)
                image = image / 255
                image = np.expand_dims(image, axis=0)

                class_predicted = model.predict_classes(image)
                probabilities = model.predict_proba(image)
                inID = class_predicted[0]
                inv_map = {v: k for k, v in class_dictionary.items()}
                label = inv_map[inID]

                if label == category:
                    match += 1

                for i in range(len(predictions_list)):
                    pred = predictions_list[i]
                    if pred[label] is None:
                        pred[label] = []
                    pred[label].append(probabilities[i][inID])


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

    def evaluate_tests(self):
        pass