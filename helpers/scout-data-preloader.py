import os
from shutil import copy

source_base_dir = "../data2/autoscout/images/"
destination_base_dir = "../data2/autoscout-data/"

for make in os.listdir(source_base_dir):
    make_dir = source_base_dir + make + '/'
    # if make <= 'Buick':
    #     print("Skipping make %s " % make)
    #     continue

    for sub_d in os.listdir(make_dir):
        model = sub_d
        model_dir =  make_dir + model + '/'

        print("Doing %s %s"% (make, model))
        for f in os.listdir(model_dir):
            destination = destination_base_dir + ( make + '-' + model ) + '/'
            if not os.path.isdir(destination):
                os.makedirs(destination)
            source = model_dir + f
            try:
                copy(source, destination)
            except Exception as e:
                print(e)
