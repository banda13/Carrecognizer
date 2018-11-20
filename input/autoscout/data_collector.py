import os
import urllib.request

import requests
from random import uniform
from time import sleep

import paths

make_mappings = {
    # 2: "alfa_romeo",
    4: "aston_martin",
    5: "audi",
    7: "bentley",
    9: "bmw",
    13: "cadillac",
    15: "chevrolet",
    16: "chrysler",
    17: "citroen",
    18: "dacia",
    19: "daewoo",
    23: "dodge",
    25: "ferrari",
    26: "fiat",
    27: "ford",
    29: "honda",
    32: "hyundai",
    38: "jaguar",
    39: "jeep",
    40: "kia",
    42: "lada",
    43: "lamborghini",
    44: "lancia",
    45: "land_rover",
    46: "lexus",
    49: "maserati",
    50: "mazda",
    51: "mercedes",
    54: "mini",
    55: "mitsubishi",
    57: "nissan",
    59: "opel",
    60: "peugeot",
    62: "porsche",
    66: "renault",
    70: "seat",
    71: "skoda",
    72: "smart",
    74: "subaru",
    75: "suzuki",
    78: "toyota",
    81: "volvo",
    82: "volkswagen"
}

source_folder = paths.SCOUT_DIR
base_url = "https://www.autoscout24.ch"
list_url = "https://www.autoscout24.ch/de/autos/alle-marken?make=%d&page=%d"
sub_dir_pattern = 'href="/de/d/'
image_pattern = 'src="https://cas01.autoscout24.ch/'

result_list_pattern = 'href="/de/autos/alle-marken?make="'

for car_id, car_type in make_mappings.items():
    page = 1
    type_url = list_url % (car_id, page)
    path = source_folder + car_type
    if not os.path.exists(path):
        os.makedirs(path)
    print("Downloading images : ", car_type)

    resp = requests.get(type_url)
    counter = 0
    sleep(round(uniform(0.5, 0.9), 4))

    has_more_page = True
    page_txt = resp.text

    while has_more_page:
        try:
            print("%d image loaded to: %s !Loading images from next page: %d" % (counter, car_type, page))

            sub_pages = []
            images_in_page = 0
            for word in page_txt.split():
                if word.startswith(sub_dir_pattern):
                    try:
                        url = word.replace('href="', "").split('"', 1)[0]
                        if url in sub_pages:
                            continue

                        url = (base_url + url).replace("amp;", "")
                        r2 = requests.get(url)
                        sleep(round(uniform(0.1, 2.3), 4))

                        inner_body = r2.text
                        car_image_counter = 0
                        images_in_subpage = []
                        for word2 in inner_body.split():
                            if word2.startswith(image_pattern) and word2.endswith('.jpg"'):
                                try:
                                    img_url = word2.replace('src="', "").split('"', 1)[0]
                                    img_url = img_url.replace("/?71x53/0/90/custom/", "/?1024x2048/3/90/custom/")
                                    if img_url in images_in_subpage:
                                        continue

                                    file_name = source_folder + car_type + "/" + car_type + "_" + str(counter) + ".jpg"
                                    img = urllib.request.urlretrieve(img_url, file_name)
                                    sleep(round(uniform(0.2, 1.2), 4))

                                    counter += 1
                                    images_in_page += 1
                                    car_image_counter += 1

                                    images_in_subpage.append(img_url)

                                    if car_image_counter > 3:
                                        break
                                except Exception as e:
                                    print("%s error while downloading image: %s" % (str(e), word2))
                        sub_pages.append(url)
                        # if len(sub_pages) > 3:
                        #      print("Debug mod, downloading from page %d ended" % page)
                        #     break
                    except Exception as e:
                        print("%s error while loading from page: %s. " % (str(e), word))

            page += 1
            end_of_category = False
            new_url = list_url % (car_id, page)
            new_page = requests.get(new_url)
            page_txt = new_page.text
            sleep(round(uniform(0.1, 0.9), 4))

            if images_in_page == 0:
                print("No new image found on page %s going to next category" % (str(page)))
                end_of_category = True

            if page > 100:
                print("50th page reached, going to next category")
                end_of_category = True

            has_more_page = (not end_of_category)
        except Exception as e:
            print("Failed to load more image from category: %s. %d image downloaded. Error: %s" % (car_type, counter, str(e)))

    print("%d images downloaded to category %s" % (counter, car_type))