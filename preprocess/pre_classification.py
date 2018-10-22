import os
import csv
from shutil import copy, move
from keras.preprocessing.image import load_img
from keras.preprocessing.image import img_to_array
from keras.applications.vgg16 import preprocess_input
from keras.applications.vgg16 import decode_predictions
from keras.applications.vgg16 import VGG16


class VggPreClassifier(object):
    dirs = ["../data/hasznaltauto/", "../data/autotrader/"]
    fieldnames = ["image", "label", "percentage"]

    """
    These categories usually determine something inside a car 
    Not full list, but great for cleaning the train data set
    """
    bad_vgg_categories = ["car_mirror", "neck_brace", "knee_pad", "odometer", "seat_belt", "gasmask", "backpack", "magnetic_compass",
                          "can_opener", "carpenter's_kit", "dumbbell", "binoculars", "paper_towel", "mask", "cassette_player",
                          "disk_brake", "radio", "oil_filter", "bulletproof_vest", "spotlight", "tape_player", "projector",
                          "reel", "envelope", "wardrobe", "CD_player", "oxygen_mask", "sunglasses", "reflex_camera"]
    percentage_limit = 0.1

    def __init__(self):
        self.model = VGG16()
        print("VGG pre classifier initialized")

    def classify(self, name, image):

        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        yhat = self.model.predict(image)
        label = decode_predictions(yhat)
        label = label[0][0]
        # print('%s -> %s (%.2f%%)' % (name, label[1], label[2] * 100))
        return label

    def prepare(self):
        vgg_classes = set()
        for source in self.dirs:
            for category in os.listdir(source):
                print("Classifying category: ", category)
                with open(source + category + '/vgg_classifications.csv', 'w') as csvfile:
                    writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                    writer.writeheader()
                    for image in os.listdir(source + category):
                        try:
                            label = self.classify(image,
                                                  load_img(source + category + "\\" + image, target_size=(224, 224)))
                            vgg_classes.add(label[1])
                            writer.writerow({self.fieldnames[0]: image, self.fieldnames[1]: label[1], self.fieldnames[2]: label[2]})
                        except Exception as e:
                            print("Error in file: %s. %s" %(image, str(e)))
        print("Classifying done, found %d unique category" %len(vgg_classes))
        for vgg_class in vgg_classes:
            print(vgg_class)

    def cleanup(self):
        all_deleted = 0
        for source in self.dirs:
            for category in os.listdir(source):
                if category == 'deleted':
                    continue
                deleted_from_category = 0
                print("Cleaning category: ", category)
                if not os.path.exists(source + "deleted"):
                    os.makedirs(source + "deleted")
                with open(source + category + '/vgg_classifications.csv', 'r') as csvfile:
                    reader = csv.DictReader(csvfile, fieldnames=self.fieldnames)
                    for row in reader:
                        image, cat, percentage = row[self.fieldnames[0]], row[self.fieldnames[1]], row[self.fieldnames[2]]
                        if cat in self.bad_vgg_categories and float(percentage) > self.percentage_limit:
                            # os.remove(source + category + "/" + image)
                            try:
                                move(source + category + '/' + image, source + "deleted/" + image)
                                deleted_from_category += 1
                            except Exception as e:
                                print("Skipping file %s. Error: %s " % (image, str(e)))
                print("%d images deleted from category %s " % (deleted_from_category, category))
                all_deleted += deleted_from_category


vgg = VggPreClassifier()
vgg.cleanup()