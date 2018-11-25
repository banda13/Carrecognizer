import os
import csv
import random
from collections import Counter
import input.autotrader.utils as autotrader
import input.hasznaltauto.utils as hasznaltauto

def summ_categories(limit = 0):
    hasznaltauto_input = hasznaltauto.count_images_per_class()
    autotrader_input = autotrader.count_images_per_class()
    input_summ = Counter(hasznaltauto_input) + Counter(autotrader_input)
    input_summ_with_limit = {}
    for key, value in input_summ.items():
        if int(value) > limit:
            print(key + ": " + str(value))
            input_summ_with_limit[key] = value
    return input_summ_with_limit, hasznaltauto_input, autotrader_input

def reduce_data_size(limit_in_categories):
    directories = ["../data/train/",  "../data/test/"]
    for d in directories:
        print("Reducing directory size %s " %d)
        for category in os.listdir(d):
            print("Reducing category %s size" % category)
            category_dir = d + category + "/"
            files_in_category = os.listdir(category_dir)
            files_selected_for_delete = random.sample(files_in_category, (len(files_in_category) - limit_in_categories))
            print("%d file selected for delete" % len(files_selected_for_delete))
            for f in files_selected_for_delete:
                if os.path.exists(category_dir + f):
                    os.remove(category_dir + f)
                else:
                    print("The file does not exist: %s " % (category_dir + f))

def get_all_make_model():
    csv_resources = ["../resources/cars(1992-1999).csv", "../resources/cars(2000-2008).csv", "../resources/cars(2008-2018).csv"]
    model_make_dict = {}
    for file in csv_resources:
        print("Reading make&model pairs from resource: %s " % file)
        with open(file, newline='') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                if row['model'] not in model_make_dict:
                    model_make_dict[row['model']] = row['make']

    print("%d unique model-make pair found (years ignored)" % len(model_make_dict.keys()))
    return model_make_dict

summ_categories(1000)



