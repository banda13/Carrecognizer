import os
import paths
import random
from shutil import copy
from dao.services.scout_service import lookup_property_distinct_values, query_for_property_value, \
    query_for_properties_values

separation_property = 'body'
max_img_in_category = 500
balance_data = True
force_balance_data = True # will throw away the irrelevant small categories
extra_condition = [{'name': 'make_id', 'value': '9'}, {'name': None, 'value': None}]

destination_dir = '..\\temp2\\' + separation_property
source_dir = paths.N_SCOUT_DIR

if not os.path.exists(destination_dir):
    os.mkdir(destination_dir)

for l in lookup_property_distinct_values(separation_property):
    if l[0] is not None:
        origin_name = l[0]
        name = l[0].replace('/', '')
        if not os.path.exists(destination_dir + "\\" + name):
            os.mkdir(destination_dir + "\\" + name)
        if extra_condition is None:
            values = query_for_property_value(separation_property, origin_name)
        else:
            extra_condition[-1] = ({'name': separation_property, 'value': origin_name})
            values = query_for_properties_values(extra_condition)
        i = 0

        if force_balance_data and len(values) < max_img_in_category:
            if os.path.exists(destination_dir + "\\" + name):
                os.rmdir(destination_dir + "\\" + name)
            continue

        random.shuffle(values)
        for car in values:
            try:
                if i >= max_img_in_category:
                    break
                d = source_dir + car.make + '-' + car.model
                for f in os.listdir(d):
                    if f.__contains__('_%d_' % car.id):
                        copy(d + '\\' + f, destination_dir + '\\' + name)
                        i += 1
                        break
            except Exception as e:
                print(e)
