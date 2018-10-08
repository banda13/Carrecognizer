import os
import math
import random

import matplotlib.pyplot as plt
import numpy as np
from utils import largest_prime_factor

test_dir = "data/test/"
limit_per_class = 50
safty = 10

def safer_manual_accuracy_test(classifier):
    results = []
    for i in range(safty):
        results.append(manual_accuracy_test(classifier))
    acc = np.mean(results)
    print("%f accuracy measured" % acc)

# Important to classifier have use function
def manual_accuracy_test(classifier):
    categories = os.listdir(test_dir)
    total = len(categories) * limit_per_class
    correct_images = []

    # p = [ a.append(x) for x in range(10) ]
    for i in range(len(categories)):
        category = categories[i]
        print("Testing images from category:", category)
        sub_dir = test_dir + category + "/"
        correct_images.extend([img for img in random.sample(os.listdir(sub_dir), limit_per_class) if (round(classifier.use(sub_dir + img)) == i)])

    acc = len(correct_images) / float(total)
    print("There was %d matches from %d image. %f measured accuracy" % (len(correct_images), total, acc))
    return acc