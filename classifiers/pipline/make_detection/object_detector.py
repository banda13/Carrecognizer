import random

import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow.compat.v1 as tf

from classifiers.pipline.make_detection.utils import create_category_index_from_labelmap, \
    reframe_box_masks_to_image_masks
from classifiers.pipline.make_detection.visualization_utils import visualize_boxes_and_labels_on_image_array

tf.disable_v2_behavior()
import zipfile

from distutils.version import StrictVersion
from collections import defaultdict
from io import StringIO
from PIL import Image
import matplotlib.pyplot as plt

# What model to download.

MODEL_NAME = 'ssd_inception_v2_coco_2018_01_28'
MODEL_FILE = MODEL_NAME + '.tar.gz'
DOWNLOAD_BASE = 'http://download.tensorflow.org/models/object_detection/'


IMAGE_SIZE = (12, 8)


class ObjectDetector:

    def __init__(self, PATH_TO_FROZEN_GRAPH, PATH_TO_LABELS):
        # download model
        """opener = urllib.request.URLopener()
        print("Downloading model file")
        opener.retrieve(DOWNLOAD_BASE + MODEL_FILE, MODEL_FILE)
        tar_file = tarfile.open(MODEL_FILE)

        print("Extracting model into frozen interference graph")
        for file in tar_file.getmembers():
            file_name = os.path.basename(file.name)
            if 'frozen_inference_graph.pb' in file_name:
                tar_file.extract(file, os.getcwd())
        """
        self.detection_graph = tf.Graph()
        with self.detection_graph.as_default():
            od_graph_def = tf.GraphDef()
            with tf.io.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
                s = fid.size()
                self.serialized_graph = fid.read()
                od_graph_def.ParseFromString(self.serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        self.category_index = create_category_index_from_labelmap(PATH_TO_LABELS)

    def load_image_into_numpy_array(self, image):
        (im_width, im_height) = image.size
        return np.array(image.getdata()).reshape(
            (im_height, im_width, 3)).astype(np.uint8)

    def run_inference_for_single_image(self, image):
        with self.detection_graph.as_default():
            with tf.Session() as sess:
                # Get handles to input and output tensors
                ops = tf.get_default_graph().get_operations()
                all_tensor_names = {output.name for op in ops for output in op.outputs}
                tensor_dict = {}
                for key in [
                    'num_detections', 'detection_boxes', 'detection_scores',
                    'detection_classes', 'detection_masks'
                ]:
                    tensor_name = key + ':0'
                    if tensor_name in all_tensor_names:
                        tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
                            tensor_name)
                if 'detection_masks' in tensor_dict:
                    # The following processing is only for single image
                    detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
                    detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
                    # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
                    real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
                    detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
                    detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
                    detection_masks_reframed = reframe_box_masks_to_image_masks(
                        detection_masks, detection_boxes, image.shape[1], image.shape[2])
                    detection_masks_reframed = tf.cast(
                        tf.greater(detection_masks_reframed, 0.5), tf.uint8)
                    # Follow the convention by adding back the batch dimension
                    tensor_dict['detection_masks'] = tf.expand_dims(
                        detection_masks_reframed, 0)
                image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

                # Run inference
                output_dict = sess.run(tensor_dict,
                                       feed_dict={image_tensor: image})

                # all outputs are float32 numpy arrays, so convert types as appropriate
                output_dict['num_detections'] = int(output_dict['num_detections'][0])
                output_dict['detection_classes'] = output_dict[
                    'detection_classes'][0].astype(np.int64)
                output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
                output_dict['detection_scores'] = output_dict['detection_scores'][0]
                if 'detection_masks' in output_dict:
                    output_dict['detection_masks'] = output_dict['detection_masks'][0]
            return output_dict

    def read_image_and_run_object_detection(self, image):
        # image = Image.open(image)
        # the array based representation of the image will be used later in order to prepare the
        # result image with boxes and labels on it.
        image = self.load_image_into_numpy_array(image)
        # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
        image = np.expand_dims(image, axis=0)
        # Actual detection.
        output_dict = self.run_inference_for_single_image(image)
        return output_dict, image

    def get_category_info(self, object_detection_dict, max_boxes_to_draw=20,
    min_score_thresh=.5):
        boxes = object_detection_dict['detection_boxes']
        classes =object_detection_dict['detection_classes']
        scores =object_detection_dict['detection_scores']
        category_index = self.category_index
        result = []
        for i in range(min(max_boxes_to_draw, boxes.shape[0])):
            if scores is None or scores[i] > min_score_thresh:
                if classes[i] in category_index.keys():
                    result.append((category_index[classes[i]]['name'], scores[i]))
        return result

    def visualize_object_detection(self, object_detection_dict, image_np):
        visualize_boxes_and_labels_on_image_array(
            image_np,
            object_detection_dict['detection_boxes'],
            object_detection_dict['detection_classes'],
            object_detection_dict['detection_scores'],
            self.category_index,
            instance_masks=object_detection_dict.get('detection_masks'),
            use_normalized_coordinates=True,
            line_thickness=8)
        plt.figure(figsize=IMAGE_SIZE)
        plt.imshow(image_np)
        plt.show()

if __name__ == '__main__':
    PATH_TO_FROZEN_GRAPH = "model/fine_tuned_model/frozen_inference_graph.pb"
    PATH_TO_LABELS = "annotations/label_map.pbtxt"
    obj = ObjectDetector(PATH_TO_FROZEN_GRAPH, PATH_TO_LABELS)
    image = Image.open("../audi_test.jpg")
    object_detection_result, image_np = obj.read_image_and_run_object_detection(image)
    obj.visualize_object_detection(object_detection_result, image_np)