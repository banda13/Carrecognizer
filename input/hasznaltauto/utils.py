import os

def count_images_per_class():
    for type in os.listdir("../../data/hasznaltauto/"):
        print("Category: %s, Sample: %d " % (type, len(os.listdir("../../data/hasznaltauto/" + type))))

count_images_per_class()
