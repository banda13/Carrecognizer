import re
import csv
import json
import time
import requests
from datetime import datetime
from random import uniform
from time import sleep

# consts
language = 'HU' #just remember..
cache_csv_name = 'autoscout_makemodel_cache.csv'
cache_field_names = ['model_id', 'model', 'make_id', 'make']

list_url = 'https://www.autoscout24.hu/lst/%s/%s?page=%d' # model-make-pagenum
sub_dir_pattern = 'href="/ajanlat/'

# autoscout consts
make_graphql_request_body = '{"query":"query ModelModelLineQuery($vehicleTypeId: String!, $makeId: Int!, $modelLineId: Int, $bg_BG: Boolean = false, $cs_CZ: Boolean = false, $de_AT: Boolean = false, $de_DE: Boolean = false, $en_GB: Boolean = false, $es_ES: Boolean = false, $fr_BE: Boolean = false, $fr_FR: Boolean = false, $fr_LU: Boolean = false, $hr_HR: Boolean = false, $hu_HU: Boolean = false, $it_IT: Boolean = false, $nl_BE: Boolean = false, $nl_NL: Boolean = false, $pl_PL: Boolean = false, $ro_RO: Boolean = false, $ru_RU: Boolean = false, $sv_SE: Boolean = false, $tr_TR: Boolean = false, $uk_UA: Boolean = false) {  filters {    model {      values(vehicleTypeId: $vehicleTypeId, makeId: $makeId, modelLineId: $modelLineId) {        id        name        modelLineId        label {          ...labelFields        }      }    }    modelLine {      values(vehicleTypeId: $vehicleTypeId, makeId: $makeId) {        id        name        label {          ...labelFields        }      }    }  }}fragment labelFields on LocalizedMessage {  bg_BG @include(if: $bg_BG)  cs_CZ @include(if: $cs_CZ)  de_AT @include(if: $de_AT)  de_DE @include(if: $de_DE)  en_GB @include(if: $en_GB)  es_ES @include(if: $es_ES)  fr_BE @include(if: $fr_BE)  fr_FR @include(if: $fr_FR)  fr_LU @include(if: $fr_LU)  hr_HR @include(if: $hr_HR)  hu_HU @include(if: $hu_HU)  it_IT @include(if: $it_IT) nl_BE @include(if: $nl_BE) nl_NL @include(if: $nl_NL)  pl_PL @include(if: $pl_PL)  ro_RO @include(if: $ro_RO)  ru_RU @include(if: $ru_RU)  sv_SE @include(if: $sv_SE)  tr_TR @include(if: $tr_TR)  uk_UA @include(if: $uk_UA)}","variables":{"vehicleTypeId":"C","makeId":%d,"hu_HU":true}}'
make_request_graphql_url = "https://search-filters-provider.a.autoscout24.com/graphql"

# Autoscout secrets... noobs :D
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

