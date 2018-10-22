import os
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


print("reduce")
reduce_data_size(1000)