import os
import shutil

import paths
import random
from shutil import copy
from dao.services.scout_service import lookup_property_distinct_values, query_for_property_value, \
    query_for_properties_values, execute_sql

# WITH THIS SCRIPT YOU EXAMINE THE DATAS FROM A DIFFERENT PERSPECTIVE
# SELECT AN ANOTHER PROPERTY, AND CREATE A NEW DATASET ON WHICH YOU CAN BUILD A NEW MODEL

# settings
# specify the main separation property on which you'd like to build the new database
separation_property = 'body'
# set the limit of for each category
max_img_in_category = 300

# will throw away the irrelevant small categories and will keep the dataset balanced
force_balance_data = True

# select a group by property and a limit
# the items where this property occurrence is below this limit will be ignored
black_sheep_filter = True  # enable the filter
black_sheep_property = 'model'  # specify the group by property
black_sheep_limit = 0.3  # set the limit. ex: 0.2 -> if the occurrence is below 20% will be ignored
black_sheep_valid = {}  # don't change, used to select valid categories

# None if nothing, otherwise follow the specified formula:
# [{'name': 'make_id', 'value': '9', 'operation': '='}, {'name': None, 'value': None, 'operation': None}]
extra_condition = None

# TODO create csv label file instead of directory hierarchy

# obvious
destination_dir = '..\\temp2\\' + separation_property
source_dir = paths.N_SCOUT_DIR

if not os.path.exists(destination_dir):
    os.mkdir(destination_dir)

if len(os.listdir(destination_dir)) > 0:
    if input('The following directory is not empty: %s. Type yes if you would like to delete the content'
             % destination_dir) == 'yes':
        shutil.rmtree(destination_dir, ignore_errors=True)
        os.makedirs(destination_dir)

if black_sheep_filter:
    black_sheep = {}
    print('Black sheep filter is active, preparing filter')
    # phase 1: query values
    for black_sheep_value in lookup_property_distinct_values(black_sheep_property):
        results = execute_sql("select %s, count(%s) from scout_car where %s = '%s' group by %s, %s" %
                              (separation_property,
                               separation_property,
                               black_sheep_property,
                               black_sheep_value[0],
                               separation_property,
                               black_sheep_property))
        summ = 0
        results_in_category = {}
        for row in results:
            summ += row[1]
            results_in_category[row[0]] = row[1]
        results_in_category['sum'] = summ
        black_sheep[black_sheep_value[0]] = results_in_category
    # phase 2: invert dictionary

    for type, dictionary in black_sheep.items():
        s = dictionary['sum']
        for key, value in dictionary.items():
            if key == 'sum':
                continue
            if key not in black_sheep_valid:
                black_sheep_valid[key] = []
            dist = value / s
            if dist > black_sheep_limit:
                black_sheep_valid[key].append(type)

for l in lookup_property_distinct_values(separation_property):
    if l[0] is not None:
        origin_name = l[0]
        name = l[0].replace('/', '')
        if not os.path.exists(destination_dir + "\\" + name):
            os.mkdir(destination_dir + "\\" + name)

        if black_sheep_filter:

            if extra_condition is None:
                extra_condition = [({'name': black_sheep_property, 'operation': 'in', 'value': tuple(black_sheep_valid[origin_name])})]
            else:
                for cond in extra_condition:
                    if cond['name'] == black_sheep_property:
                        extra_condition.remove(cond)
                extra_condition.append({'name': black_sheep_property, 'operation': 'in', 'value':tuple(black_sheep_valid[origin_name])})

        if extra_condition is None:
            values = query_for_property_value(separation_property, origin_name)
        else:
            for cond in extra_condition:
                if cond['name'] == separation_property:
                    extra_condition.remove(cond)
            extra_condition.append({'name': separation_property, 'value': "'"+origin_name+"'", 'operation': '='})
            values = query_for_properties_values(extra_condition)
        i = 0

        print('There are {} images in category {} which fulfills the conditions'.format(len(values), origin_name))
        if force_balance_data and len(values) < max_img_in_category:
            if os.path.exists(destination_dir + "\\" + name):
                print('Deleting directory {} because the lack of the images'.format(destination_dir + "\\" + name))
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
