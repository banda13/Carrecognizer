import os

def count_images_per_class():
    cars = {}
    for type in os.listdir("../data/hasznaltauto/"):
        count = len(os.listdir("../data/hasznaltauto/" + type))
        # print("Category: %s, Sample: %d " % (type, count))
        cars[type] = count
    return cars

# count_images_per_class()
