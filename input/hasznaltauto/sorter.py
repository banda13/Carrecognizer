import os
import random

from shutil import copy, copy2


def sort_train_vs_text(p_train, p_test, limit, categories = None):
    root_dir = "data/hasznaltauto/"
    train_dir = "data/train/"
    test_dir = "data/test/"

    if categories is None:
        categories = os.listdir(root_dir)
        print("%d category founded" % len(categories))
    for category in categories:
        files_in_category = os.listdir(root_dir + category)

        if len(files_in_category) < limit:
            print("Category %s skipped because of the lack of images: %d" % (category, len(files_in_category)))
            continue

        category_length = len(files_in_category)
        random.shuffle(files_in_category)

        train_count = int(p_train * limit)
        test_count = int(p_test * limit)

        print("%d train and %d test data determined in category %s in hasznaltauto" % (train_count, test_count, category))

        if not os.path.exists(train_dir + category + "/"):
            os.makedirs(train_dir + category + "/")
        if not os.path.exists(test_dir + category + "/"):
            os.makedirs(test_dir + category + "/")

        for i in range(limit):
            if i <= train_count:
                copy2(root_dir + category + "/" + files_in_category[i], train_dir + category + "/hasznaltauto_" + files_in_category[i])
            else:
                copy2(root_dir + category + "/" + files_in_category[i], test_dir + category + "/hasznaltauto_" + files_in_category[i])

        print("%s category done in hasznaltauto" % category)


# sort_train_vs_text(0.8, 0.2, 5000)
