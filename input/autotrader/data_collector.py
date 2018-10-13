import urllib.request
from time import sleep
import requests
import os
from random import uniform
import substring
import cv2
import re

source_folder = "../../data/autotrader/"
sub_dir_pattern = '/classified/advert/'
sub_dir_start = "https://www.autotrader.co.uk/classified/advert/"
image_pattern = "data-src='https://m.atcdn.co.uk/a/media/"
result_list_pattern = 'href="https://www.autotrader.co.uk/car-search/page/'

car_types = {
    "abarth": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=ABARTH&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "aston martin": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=ASTON%20MARTIN&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "bentley": "https://www.autotrader.co.uk/car-search?sort=sponsored&radius=1500&postcode=ec1a1bb&onesearchad=Used&onesearchad=Nearly%20New&onesearchad=New&make=BENTLEY&page=1",
    "chevrolet": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=CHEVROLET&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "chrysler": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=CHRYSLER&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "citroen": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=CITROEN&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "dacia": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=DACIA&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "dodge": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=DODGE&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "ferrari": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=FERRARI&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "fiat": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=FIAT&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "honda": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=HONDA&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "hyundai": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=HYUNDAI&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "jaguar": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=JAGUAR&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "jeep": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=JEEP&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "kia": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=KIA&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "lamborghini": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=LAMBORGHINI&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "land_rover": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=LAND%20ROVER&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "lexus": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=LEXUS&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "maserati": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=MASERATI&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "mini": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&postcode=EC1A+1BB&radius=&make=MINI&model=&price-search-type=total-price&price-from=&price-to=&search-used-vehicles=&page=1",
    "mitsubishi": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=MITSUBISHI&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "nissan": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=NISSAN&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "porsche": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=PORSCHE&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "smart": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=SMART&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "subaru": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=SUBARU&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "suzuki": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=SUZUKI&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "volvo": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=VOLVO&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "seat": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=SEAT&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "peugeot": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=PEUGEOT&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "skoda": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=SKODA&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "alfa_romeo": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=ALFA%20ROMEO&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "mazda": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=MAZDA&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "renault": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=RENAULT&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "mercedes": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=MERCEDES-BENZ&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "ford": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=FORD&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "audi": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=AUDI&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "volkswagen": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=VOLKSWAGEN&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
    "bmw": "https://www.autotrader.co.uk/car-search?advertising-location=at_cars&search-target=usedcars&is-quick-search=true&radius=&make=BMW&model=&price-search-type=total-price&price-from=&price-to=&postcode=ec1a1bb&page=1",
}

for car_type, type_url in car_types.items():
    path = source_folder + car_type
    if not os.path.exists(path):
        os.makedirs(path)
    print("Downloading images : ", car_type)
    resp = requests.get(type_url)
    counter = 0
    sleep(round(uniform(0.5, 0.9), 4))

    has_more_page = True
    page = 1
    page_txt = resp.text

    while has_more_page:
        try:
            print("%d image loaded to: %s !Loading images from next page: %d" % (counter, car_type, page))

            """First we iterate trough the cars in the page, and download 4 image from each car"""

            sub_pages = []
            for word in page_txt.split():
                if word.__contains__(sub_dir_pattern):
                    try:
                        m = re.search('href="/classified/advert/(.+?)"', word)
                        if m:
                            url = sub_dir_start + m.group(1)
                            if url in sub_pages or url.endswith("#check-history"):
                                continue

                            r2 = requests.get(url)
                            sleep(round(uniform(0.1, 0.4), 4))

                            inner_body = r2.text
                            car_image_counter = 0
                            images_in_subpage = []
                            for word2 in inner_body.split():
                                if word2.__contains__(image_pattern):
                                    try:
                                        if word2 in images_in_subpage:
                                            continue
                                        from_str = "data-src=\'"
                                        img_url = word2.replace(from_str, "").split("\'", 1)[0]
                                        url_parts = word2.split("/")
                                        temp = substring.substringByInd(url_parts[5],
                                                                        startInd=url_parts[5].index('w') + 1,
                                                                        endInd=url_parts[5].index('h') - 1)
                                        width = int(temp)
                                        height = int(
                                            substring.substringByInd(url_parts[5], startInd=url_parts[5].index('h') + 1,
                                                                     endInd=(url_parts[5].index('h') + len(temp))))
                                        if width < 300 or height < 300:
                                            continue
                                        file_name = source_folder + car_type + "/" + car_type + "_" + str(
                                            counter) + ".jpg"
                                        img = urllib.request.urlretrieve(img_url, file_name)
                                        sleep(round(uniform(0.2, 0.6), 4))

                                        counter += 1
                                        car_image_counter += 1

                                        images_in_subpage.append(img_url)

                                        if car_image_counter > 3:
                                            break
                                    except Exception as e:
                                        print("%s error while downloading image: %s" % (str(e), word2))
                            sub_pages.append(url)
                            # if len(sub_pages) > 3:
                            #     print("Debug mod, downloading from page %d ended" % page)
                            #     break
                    except Exception as e:
                        print("%s error while loading from page: %s. " % (str(e), word))

            """Than we check, if there are more pages to the category, and if yes, we go to the next"""
            page += 1
            end_of_category = True
            print()
            for word in page_txt.split():
                if word.startswith(result_list_pattern) and word.__contains__("page/" + str(page)):
                    new_url = type_url[:-1] + str(page)
                    new_page = requests.get(new_url)
                    page_txt = new_page.text
                    end_of_category = False
                    sleep(round(uniform(0.1, 0.5), 4))
                    break

            has_more_page = (not end_of_category)
        except Exception as e:
            print("Failed to load more image from category: %s. %d image downloaded. Error: %s" % (
                car_type, counter, str(e)))



        except Exception as e:
            print("Failed to load more image from category: %s. %d image downloaded. Error: %s" % (
            car_type, counter, str(e)))

    print("%d images downloaded to category %s" % (counter, car_type))
