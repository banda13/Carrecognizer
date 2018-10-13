import os
import random

from shutil import copy


def sort_train_vs_text(p_train, p_test, limit):
    root_dir = "../../data/hasznaltauto/"
    train_dir = "../../data/train/"
    test_dir = "../../data/test/"

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

        print("%d train and %d test data determined in category %s" % (train_count, test_count, category))

        if not os.path.exists(train_dir + category + "/"):
            os.makedirs(train_dir + category + "/")
        if not os.path.exists(test_dir + category + "/"):
            os.makedirs(test_dir + category + "/")

        for i in range(limit):
            if i <= train_count:
                copy(root_dir + category + "/" + files_in_category[i], train_dir + category)
            else:
                copy(root_dir + category + "/" + files_in_category[i], test_dir + category)

        print("%s category done" % category)


sort_train_vs_text(0.8, 0.2, 5000)
