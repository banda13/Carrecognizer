# from keras.engine.saving import load_model
from keras_preprocessing.image import load_img, img_to_array, ImageDataGenerator

import numpy as np
#
# model = load_model("new_model.h5")
#
# image_width, image_height = 160, 160
# num_categories = 4
#
# image = load_img("data2/autoscout/images/Opel/Corsa/Opel_Corsa_206519_119.jpg", target_size=(image_width, image_height))
# image = img_to_array(image)
# image = image / 255
# image = np.expand_dims(image, axis=0)
#
# prediction = model.predict(image).reshape(num_categories)
# print(np.argmax(prediction))

train_datagen = ImageDataGenerator(
    shear_range=0.2,
    zoom_range=0.2,
    rotation_range=20,
    width_shift_range=0.2,
    height_shift_range=0.2,
    rescale=1. / 255)

train_generator = train_datagen.flow_from_directory(
    "data/train",
    target_size=(160, 160),
    batch_size=16,
    class_mode=None)

num_classes = len(train_generator.class_indices)
np.save("class_indices.npy", train_generator.class_indices)