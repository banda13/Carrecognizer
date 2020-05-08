import tensorflow.compat.v1 as tf

from classifiers.pipline.make_detection import string_int_label_map_pb2

tf.disable_v2_behavior()
from google.protobuf import text_format



def create_categories_from_labelmap(label_map_path, use_display_name=True):
  label_map = load_labelmap(label_map_path)
  max_num_classes = max(item.id for item in label_map.item)
  return convert_label_map_to_categories(label_map, max_num_classes,
                                         use_display_name)

def create_category_index_from_labelmap(label_map_path):
  label_map = load_labelmap(label_map_path)
  max_num_classes = max(item.id for item in label_map.item)
  categories = convert_label_map_to_categories(label_map, max_num_classes)
  return create_category_index(categories)

def load_labelmap(path):
  with tf.gfile.GFile(path, 'r') as fid:
    label_map_string = fid.read()
    label_map = string_int_label_map_pb2.StringIntLabelMap()
    try:
      text_format.Merge(label_map_string, label_map)
    except text_format.ParseError:
      label_map.ParseFromString(label_map_string)
  return label_map


def convert_label_map_to_categories(label_map,
                                    max_num_classes,
                                    use_display_name=True):
  categories = []
  list_of_ids_already_added = []
  if not label_map:
    label_id_offset = 1
    for class_id in range(max_num_classes):
      categories.append({
          'id': class_id + label_id_offset,
          'name': 'category_{}'.format(class_id + label_id_offset)
      })
    return categories
  for item in label_map.item:
    if not 0 < item.id <= max_num_classes:
      print('Ignore item %d since it falls outside of requested '
                   'label range.', item.id)
      continue
    if use_display_name and item.HasField('display_name'):
      name = item.display_name
    else:
      name = item.name
    if item.id not in list_of_ids_already_added:
      list_of_ids_already_added.append(item.id)
      categories.append({'id': item.id, 'name': name})
  return categories

def create_category_index(categories):
  category_index = {}
  for cat in categories:
    category_index[cat['id']] = cat
  return category_index

def reframe_box_masks_to_image_masks(box_masks, boxes, image_height,
                                     image_width):
  def reframe_box_masks_to_image_masks_default():

    """The default function when there are more than 0 box masks."""
    def transform_boxes_relative_to_boxes(boxes, reference_boxes):
      boxes = tf.reshape(boxes, [-1, 2, 2])
      min_corner = tf.expand_dims(reference_boxes[:, 0:2], 1)
      max_corner = tf.expand_dims(reference_boxes[:, 2:4], 1)
      transformed_boxes = (boxes - min_corner) / (max_corner - min_corner)
      return tf.reshape(transformed_boxes, [-1, 4])

    box_masks_expanded = tf.expand_dims(box_masks, axis=3)
    num_boxes = tf.shape(box_masks_expanded)[0]
    unit_boxes = tf.concat(
        [tf.zeros([num_boxes, 2]), tf.ones([num_boxes, 2])], axis=1)
    reverse_boxes = transform_boxes_relative_to_boxes(unit_boxes, boxes)
    return tf.image.crop_and_resize(
        image=box_masks_expanded,
        boxes=reverse_boxes,
        box_ind=tf.range(num_boxes),
        crop_size=[image_height, image_width],
        extrapolation_value=0.0)
  image_masks = tf.cond(
      tf.shape(box_masks)[0] > 0,
      reframe_box_masks_to_image_masks_default,
      lambda: tf.zeros([0, image_height, image_width, 1], dtype=tf.float32))
  return tf.squeeze(image_masks, axis=3)
