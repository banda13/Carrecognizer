import os
import re
import csv
import json
import time
import paths
import requests
import threading
import urllib.request
from time import sleep
from random import uniform
from datetime import datetime
from bs4 import BeautifulSoup

# consts
language = 'EN' #just remember..

cache_field_names = ['model_id', 'model', 'make_id', 'make']
stat_field_names = ['model', 'make', 'country', 'start_date', 'run_time', 'cars', 'images', 'errors']
debug = False

desc = 1  # true=1 NOTE: expensive cars are more relevant.. or?
sort = 'price'  # price, age, mileage, power, year
country_codes = [['A', 'AT'], ['B', 'BE'], ['D', 'DE'], ['E', 'ES'], ['F', 'FR'], ['I', 'IT'], ['L', 'LU'], ['NL', 'NE']] # Austria, Belgium, Germany, Spain, France, Italy, Luxemburg, Holland

# autoscout consts
make_graphql_request_body = '{"query":"query ModelModelLineQuery($vehicleTypeId: String!, $makeId: Int!, $modelLineId: Int, $bg_BG: Boolean = false, $cs_CZ: Boolean = false, $de_AT: Boolean = false, $de_DE: Boolean = false, $en_GB: Boolean = false, $es_ES: Boolean = false, $fr_BE: Boolean = false, $fr_FR: Boolean = false, $fr_LU: Boolean = false, $hr_HR: Boolean = false, $hu_HU: Boolean = false, $it_IT: Boolean = false, $nl_BE: Boolean = false, $nl_NL: Boolean = false, $pl_PL: Boolean = false, $ro_RO: Boolean = false, $ru_RU: Boolean = false, $sv_SE: Boolean = false, $tr_TR: Boolean = false, $uk_UA: Boolean = false) {  filters {    model {      values(vehicleTypeId: $vehicleTypeId, makeId: $makeId, modelLineId: $modelLineId) {        id        name        modelLineId        label {          ...labelFields        }      }    }    modelLine {      values(vehicleTypeId: $vehicleTypeId, makeId: $makeId) {        id        name        label {          ...labelFields        }      }    }  }}fragment labelFields on LocalizedMessage {  bg_BG @include(if: $bg_BG)  cs_CZ @include(if: $cs_CZ)  de_AT @include(if: $de_AT)  de_DE @include(if: $de_DE)  en_GB @include(if: $en_GB)  es_ES @include(if: $es_ES)  fr_BE @include(if: $fr_BE)  fr_FR @include(if: $fr_FR)  fr_LU @include(if: $fr_LU)  hr_HR @include(if: $hr_HR)  hu_HU @include(if: $hu_HU)  it_IT @include(if: $it_IT) nl_BE @include(if: $nl_BE) nl_NL @include(if: $nl_NL)  pl_PL @include(if: $pl_PL)  ro_RO @include(if: $ro_RO)  ru_RU @include(if: $ru_RU)  sv_SE @include(if: $sv_SE)  tr_TR @include(if: $tr_TR)  uk_UA @include(if: $uk_UA)}","variables":{"vehicleTypeId":"C","makeId":%d,"hu_HU":true}}'
make_request_graphql_url = "https://search-filters-provider.a.autoscout24.com/graphql"

# TODO english url's and pattern's - to run webcrawers paralell..
# this will cause multilanguage db + lot of other problems, but will double the download speed, so its worth...
en_base_url = "https://www.autoscout24.com/"
en_list_url = 'https://www.autoscout24.com/lst/%s/%s?sort=price&desc=1&page=%d&cy=%s&sort=%s&desc=%d'

hu_base_url = 'https://www.autoscout24.hu/'
hu_list_url = 'https://www.autoscout24.hu/lst/%s/%s?sort=price&desc=1&page=%d&cy=%s&sort=%s&desc=%d' # model-make-pagenum-country code-sort-desc?

hu_cache_csv_name = 'autoscout_makemodel_cache_hu.csv'
hu_stat_csv_name = 'autoscout_datasucker_stat_hu.csv'

en_cache_csv_name = 'autoscout_makemodel_cache_en.csv'
en_stat_csv_name = 'autoscout_datasucker_stat_en.csv'

if language == 'HU':
    base_url = hu_base_url
    list_url = hu_list_url
    cache_csv_name = hu_cache_csv_name
    stat_csv_name = hu_stat_csv_name
elif language == 'EN':
    base_url = hu_base_url
    list_url = hu_list_url
    cache_csv_name = en_cache_csv_name
    stat_csv_name = en_stat_csv_name
else:
    raise Exception('Language not specified!')

sub_dir_pattern = 'href="/ajanlat/'
image_pattern = 'data-fullscreen-src="https://prod.pictures.autoscout24.net/listing-images/'

thumbnail_pattern = '120x90.jpg'

# Autoscout secrets... hah noobs :D
user_name = "revolistion"
super_secret_password = "23695c1bd68c543e26f58a00d62e97ce"
basic_auth_key = "Basic cmV2b2xpc3Rpb246MjM2OTVjMWJkNjhjNTQzZTI2ZjU4YTAwZDYyZTk3Y2U="

def get_make_for_model(category):
    print('Getting makes for model %s' % category['label'])
    parsed_body = json.loads(make_graphql_request_body % int(category['id']))
    resp = requests.post(make_request_graphql_url, json=parsed_body, auth=(user_name, super_secret_password))
    makes_json = json.loads(resp.text)
    return makes_json['data']['filters']['model']['values']

def cache_results(model, makes):
    with open(cache_csv_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=cache_field_names)
        for make in makes:
            writer.writerow({'model_id': model['id'], 'model': model['label'], 'make_id': make['id'], 'make': make['name']})
        print('%d make cached for model %s' % (len(makes), model['label']))

def init():
    with open(cache_csv_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=cache_field_names)
        writer.writeheader()
        print('Cache initialized')

def init_stats():
    with open(stat_csv_name, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=stat_field_names)
        writer.writeheader()
        print('Statistics cache initialized')

def save_statistic(model, make, country,start_date, run_time, cars, images, errors):
    with open(stat_csv_name, 'a', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, delimiter=';', fieldnames=stat_field_names)
        writer.writerow({'model': model, 'make':make, 'country': country, 'start_date': start_date, 'run_time': run_time, 'cars': cars, 'images': images, 'errors': errors})
        print('%s model %s make from %s country results saved' % (model, make, country))

def cache_make_models():
    print('Getting all models')
    raw_html = requests.get("https://www.autoscout24.hu/").text
    json_finder = re.compile('window.As24HomeCarConfig.config = ({.*?});', re.DOTALL)

    matches = json_finder.search(raw_html)
    raw_json = matches.group(1)
    if raw_json is None:
        raise Exception('Initial json not found')

    initial_json = json.loads(raw_json)
    models = initial_json['taxonomy']['makes']
    print('%d make parsed from initial json' % len(models))

    init()
    for model in models:
        makes = get_make_for_model(model)
        cache_results(model, makes)

def load_cache_to_db():
    pass


def load_cache_to_memory():
    # chill its small enough
    make_models = []
    with open(cache_csv_name, 'r', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';',fieldnames=cache_field_names)
        next(reader)
        for row in reader:
            make_models.append(row)
        return make_models

def write_html_file(car_file_name, inner_body):
    with open(car_file_name, "wb") as fp:
        # fp.write(BeautifulSoup(inner_body, 'html.parser').encode("utf-8")) -> this is fcking slow.. useless
        fp.write(inner_body.encode('utf8'))

def data_sucker():
    print("Data sucking started..")
    make_models = load_cache_to_memory()

    init_stats()

    # counter's
    id_counter = 200000 # summ of all car
    img_counter = 0  # images on country level
    err_counter = 0 # errors on country level in image download
    car_counter_in_country = 0 # cars in country level
    car_image_counter = 0 # images to 1 car

    for make_model in make_models:
        model = make_model['model']
        make = make_model['make']
        print("Collecting: %s - %s " % (model, make))

        meta_path = paths.N_SCOUT_META_DIR + model + '/' + make + '/'
        image_path = paths.N_SCOUT_IMG_DIR + model + '/' + make + '/'
        if not os.path.exists(meta_path):
            os.makedirs(meta_path)
            print("Meta directory created %s" % meta_path)
        else:
            print("Skipping category, because Mate path already exists: " + meta_path)
            continue

        if not os.path.exists(image_path):
            os.makedirs(image_path)
            print("Image directory created %s" % image_path)
        else:
            print("Skipping category, because Image path already exists: " + meta_path)
            continue

        for country in country_codes:
            start_time = time.time()
            start_datetime = datetime.now()
            img_counter = 0
            err_counter = 0
            car_counter_in_country = 0

            print('Downloading from country: %s' % country[1])
            page = 1
            url = list_url % (model, make, page, country[0], sort, desc)
            resp = requests.get(url)
            sleep(round(uniform(0.5, 0.9), 4))
            has_more_page = True
            page_txt = resp.text

            while has_more_page:
                try:
                    print("Loading images from page: %d. %d image already downloaded to model: %s make %s" % (page, img_counter, model, make))

                    sub_pages = []
                    images_in_page = 0
                    for word in page_txt.split():
                        if word.startswith(sub_dir_pattern):
                            try:
                                car_url = base_url + word.replace('href="', "").split('"', 1)[0]
                                if car_url in sub_pages:
                                    continue

                                r2 = requests.get(car_url)
                                sleep(round(uniform(0.1, 0.4), 4))

                                inner_body = r2.text
                                car_image_counter = 0
                                images_in_subpage = []
                                car_id = model + "_" + make + '_' + str(id_counter)
                                car_file_name = meta_path + str(car_id) + ".txt"

                                thread = threading.Thread(target=write_html_file, args=(car_file_name, inner_body))
                                thread.start()

                                car_counter_in_country += 1
                                id_counter += 1
                                for word2 in inner_body.split():
                                    if word2.startswith(image_pattern):
                                        try:
                                            img_url = word2.replace('data-fullscreen-src="', "").split('"', 1)[0]
                                            if img_url in images_in_subpage:
                                                continue
                                            if img_url.endswith(thumbnail_pattern):
                                                continue

                                            file_name = image_path + model + "_" + make + "_" + str(id_counter) + '_' + str(img_counter) + ".jpg"
                                            img = urllib.request.urlretrieve(img_url, file_name)
                                            sleep(round(uniform(0.2, 1.2), 4))

                                            images_in_page += 1
                                            car_image_counter += 1
                                            img_counter += 1

                                            images_in_subpage.append(img_url)

                                            if debug and car_image_counter > 3:
                                                break
                                        except Exception as e:
                                            print("%s error while downloading image: %s" % (str(e), word2))
                                            err_counter += 1
                                sub_pages.append(car_url)
                                if debug and len(sub_pages) > 3:
                                    print("Debug mod on, 3 saved from this page, but now its enough..")
                                    break
                            except Exception as e:
                                print("%s error while loading from page: %s. " % (str(e), word))
                                err_counter += 1
                    page += 1
                    end_of_category = False
                    new_page_url = list_url % (model, make, page, country[0], sort, desc)
                    new_page = requests.get(new_page_url)
                    page_txt = new_page.text
                    sleep(round(uniform(0.1, 0.9), 4))

                    if images_in_page == 0:
                        print("No new image found on page %s going to next category" % (str(page)))
                        end_of_category = True

                    if debug and page > 3:
                        print("Debug mod enable, page 3 processed, going to next category")
                        end_of_category = True

                    if page > 21:  # needed due to query limit, please check the docs
                        print("21th page reached (LOL How??!), going to next category")
                        end_of_category = True

                    has_more_page = (not end_of_category)
                except Exception as e:
                    print("Failed to load more image to: %s-%s. %d image downloaded. Error: %s" % (model,make, img_counter, str(e)))
            save_statistic(model, make, country[1], start_datetime, time.time()-start_time, car_counter_in_country, img_counter, err_counter)

# init()
# cache_make_models()
data_sucker()





