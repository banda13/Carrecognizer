import os

import paths


def count_images_per_class():
    cars = {}
    for type in os.listdir(paths.HASZNALT_DIR):
        count = len(os.listdir(paths.HASZNALT_DIR + type))
        # print("Category: %s, Sample: %d " % (type, count))
        cars[type] = count
    return cars

# count_images_per_class()
