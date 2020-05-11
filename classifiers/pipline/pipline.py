import os
import json

import h5py
import keras
import numpy as np
import tensorflow as tf
config = tf.ConfigProto()
config.gpu_options.allow_growth = True

from keras.engine.saving import load_model
from keras_preprocessing.image import load_img, img_to_array

from classifiers.pipline.make_detection.object_detector import ObjectDetector

PATH_TO_FROZEN_GRAPH = "make_detection/model/fine_tuned_model/frozen_inference_graph.pb"
PATH_TO_LABELS = "make_detection/annotations/label_map.pbtxt"

class ClassifierPipline:

    def __init__(self, width, height):
        self.image_width = width
        self.image_height = height

        print("Loading make detector...")
        self.obj = ObjectDetector(PATH_TO_FROZEN_GRAPH, PATH_TO_LABELS)

        print("Loading make classifier...")
        self.make_classifier = self.load_keras_model("make_classifier/Fer")

        print("Loading model classifiers...")
        self.model_classifiers = {}
        for name in os.listdir("model_classifier/"):
            print("Loading: {}...".format(name))
            # if name == 'Cabat':
            classifier = self.load_keras_model("model_classifier/" + name)
            model = classifier['categories'][0].split("-")[0].lower().replace("_", "").strip()
            self.model_classifiers[model] = classifier

    def load_keras_model(self, path):
        class_dictionary = np.load(path + "/class_indices.npy", allow_pickle=True).item()
        inv_map = {v: k for k, v in class_dictionary.items()}
        reverse_inv_map = dict(zip(inv_map.values(), inv_map.keys()))

        # to fix keras compatibility issues
        f = h5py.File(path + "/model.h5", 'r+')
        data_p = f.attrs['training_config']
        data_p = data_p.decode().replace("learning_rate", "lr").encode()
        f.attrs['training_config'] = data_p
        f.close()

        model = load_model(path + "/model.h5")

        with open(path + "/props.json") as f:
            data = json.load(f)
            return {
                "model": model,
                "class_dictionary": class_dictionary,
                "inv_map": inv_map,
                "reverse_inv_map": reverse_inv_map,
                "categories": data["categories"],
                "num_classes": data["num_classes"]
            }

    def load_image(self, image_path):
        image_big = load_img(image_path)
        image_small = load_img(image_path, target_size=(self.image_width, self.image_height))
        image_small = img_to_array(image_small)
        image_small = image_small / 255
        image_small = np.expand_dims(image_small, axis=0)
        return image_big, image_small

    def make_top3_prediction(self, classifier, image):
        prediction = classifier['model'].predict(image).reshape(classifier['num_classes'])
        idx_prediction = np.argsort(-prediction, axis=0)
        top3_label = {
            classifier["inv_map"][idx_prediction[0]].lower().replace("_", "").strip(): prediction[idx_prediction[0]],
            classifier["inv_map"][idx_prediction[1]].lower().replace("_", "").strip(): prediction[idx_prediction[1]],
            classifier["inv_map"][idx_prediction[2]].lower().replace("_", "").strip(): prediction[idx_prediction[2]]}
        return top3_label

    def classify(self, img_path):
        # preprocessing image
        image, image_np = self.load_image(img_path)

        # executing make detection
        object_detection_result, _ = self.obj.read_image_and_run_object_detection(image)
        result = self.obj.get_category_info(object_detection_result)
        print(result)

        # executing make classification
        top3_make = self.make_top3_prediction(self.make_classifier, image_np)

        final = {}
        # decide make
        if len(result) == 0:
            for make, acc in top3_make.items():
                if acc > 0.2:
                    classifier = self.model_classifiers[make]
                    for model, acc in self.make_top3_prediction(classifier, image_np).items():
                        if model not in final or acc > final[model]:
                            final[model] = acc
        else:
            obj_res = result[0]
            make = obj_res[0].lower().replace("_", "").strip()
            classifier = self.model_classifiers[make]
            for model, acc in self.make_top3_prediction(classifier, image_np).items():
                if model not in final or acc > final[model]:
                    final[model] = acc
        print(final)
        return final




if __name__ == "__main__":
    print("Testing classification pipline")
    pipline = ClassifierPipline(160, 160)
    pipline.classify("test.jpg")
