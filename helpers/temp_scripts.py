import os
import random
from shutil import copyfile

root = "D:\Projects\CarRecognizer\data\\"

dirs = ["train", "test", 'validation']
results = {}

for d in dirs:
    cat_folders = os.listdir(root + d)
    random.shuffle(cat_folders)
    for cat in cat_folders:
        parts = cat.split("-")
        if len(parts) == 2:
            make, model = cat.split("-")
        elif len(parts) == 3:
            make = ''.join(cat.split("-")[:2])
            model = ''.join(cat.split("-")[2:])
        else:
            raise Exception("Gond van ..")

        if not make in results:
            results[make] = []

        for f in os.listdir(root + d + "//" + cat):
            results[make].append((root + d + "//" + cat + '//' + f, root + d + "_new//" + make + "//" + f))

    for make, value in results.items():
        if not os.path.isdir(root + d + "_new//" + make):
            os.mkdir(root + d + "_new//" + make)
        random.shuffle(value)
        for f in value[:3000]:
            copyfile(f[0], f[1])