import os
import csv
from shutil import copy, move

import paths


class VggPreClassifier(object):
    dirs = [paths.N_SCOUT_DIR]
    fieldnames = ["image", "label", "percentage"]

    """
    These categories usually determine something inside a car 
    Not full list, but great for cleaning the train data set
    """
    super_duper_good_vgg_categories = [
        "beach_wagon", "jeep", "pickup", "minivan", "cab", "limousine", "police_van", "convertible", "Model_T",
        "minibus", "racer", "sports_car", "police_van", "moving_van", "freight_car", "streetcar"
    ]
    maybe_good_vgg_categories = [
        "grille", "vacuum", "tow_truck"
    ]
    definitely_bad_vgg_categories = [
        "odometer", "ashcan", "red_wine", "car_mirror", "neck_brace", "knee_pad", "odometer", "seat_belt", "gasmask",
        "backpack", "magnetic_compass",
        "can_opener", "carpenter's_kit", "dumbbell", "binoculars", "paper_towel", "mask", "cassette_player",
        "disk_brake", "radio", "oil_filter", "bulletproof_vest", "spotlight", "tape_player", "projector",
        "reel", "envelope", "wardrobe", "CD_player", "oxygen_mask", "sunglasses", "reflex_camera", "web_site",
        "parking_meter", "monitor", "hand_blower", "cassette", "binder", "rotisserie", "submarine", "refrigerator",
        "lotion", "stove", "hook", "lighter", "barber_chair", "radiator", "washer", "projector", "lighter",
        "projector", "Windsor_tie", "slide_rule", "espresso_maker", "suit", "whistle", "hook", "iPod", "street_sign",
        "paper_towel", "book_jacket", "cellular_telephone", "bookshop", "puck", "sunscreen",
        "bathing_cap", "cash_machine", "plastic_bag", "bathtub", "Band_Aid", "switch", "tennis_ball",
        "digital_clock",
        "binoculars", "ballpoint", "motor_scooter", "car_wheel", "tobacco_shop", "menu", "reel", "bobsled",
        "cinema", "crash_helmet", "window_screen", "television", "gas_pump", "hard_disc", "crane",
        "printer", "bathtub", "wallet", "sewing_machine", "wall_clock", "trolleybus", "home_theater",
        "holster", "safe", "combination_lock", "packet", "viaduct", "radio_telescope", "manhole_cover",
        "loudspeaker", "beaker", "hand-held_computer", "screen", "mailbag", "mousetrap", "lab_coat",
        "file"
    ]

    percentage_limit = 0.05

    def __init__(self):
        from keras.applications.vgg16 import VGG16

        self.model = VGG16()
        print("VGG pre classifier initialized")

    def classify(self, name, image):
        from keras.preprocessing.image import img_to_array
        from keras.applications.vgg16 import preprocess_input
        from keras.applications.vgg16 import decode_predictions

        image = img_to_array(image)
        image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
        image = preprocess_input(image)
        yhat = self.model.predict(image)
        label = decode_predictions(yhat)
        label = label[0][0]
        return label

    def prepare(self):
        from keras.preprocessing.image import load_img
        vgg_classes = set()
        for source in self.dirs:
            for make in os.listdir(source):
                if len(os.listdir(source + make)) > 0 and not os.path.isdir(
                        source + make + '/' + os.listdir(source + make)[0]):
                    print("Classifying make: ", make)
                    with open(source + make + '/vgg_classifications.csv', 'w') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                        writer.writeheader()
                        for image in os.listdir(source + make):
                            try:
                                label = self.classify(image,
                                                      load_img(source + make + "\\" + image, target_size=(224, 224)))
                                vgg_classes.add(label[1])
                                writer.writerow({self.fieldnames[0]: image, self.fieldnames[1]: label[1],
                                                 self.fieldnames[2]: label[2]})
                            except Exception as e:
                                print("Error in file: %s. %s" % (image, str(e)))
                else:
                    for model in os.listdir(source + make):
                        if model.endswith('.csv'):
                            continue
                        print("Classifying make: %s model: %s" % (make, model))
                        with open(source + make + '/' + model + '/vgg_classifications.csv', 'w') as csvfile:
                            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames)
                            writer.writeheader()
                            for image in os.listdir(source + make + '/' + model):
                                try:
                                    if image.endswith('.csv'):
                                        continue
                                    label = self.classify(image,
                                                          load_img(source + make + "/" + model + "/" + image,
                                                                   target_size=(224, 224)))
                                    vgg_classes.add(label[1])
                                    writer.writerow({self.fieldnames[0]: image, self.fieldnames[1]: label[1],
                                                     self.fieldnames[2]: label[2]})
                                except Exception as e:
                                    print("Error in file: %s. %s" % (image, str(e)))
        print("Classifying done, found %d unique make" % len(vgg_classes))
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
                try:
                    with open(source + category + '/vgg_classifications.csv', 'r') as csvfile:
                        reader = csv.DictReader(csvfile, fieldnames=self.fieldnames)
                        for row in reader:
                            image, cat, percentage = row[self.fieldnames[0]], row[self.fieldnames[1]], row[
                                self.fieldnames[2]]
                            if cat not in self.super_duper_good_vgg_categories or (
                                    cat in self.maybe_good_vgg_categories and float(
                                    percentage) < self.percentage_limit):
                                # os.remove(source + category + "/" + image)
                                try:
                                    move(source + category + '/' + image, source + "deleted/" + image)
                                    deleted_from_category += 1
                                except Exception as e:
                                    print("Skipping file %s. Error: %s " % (image, str(e)))
                except Exception as e:
                    print("Skipping category %s because it do not exists" % category)
                print("%d images deleted from category %s " % (deleted_from_category, category))
                all_deleted += deleted_from_category
