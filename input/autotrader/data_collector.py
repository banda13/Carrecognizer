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
            images_in_page = 0
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
                                        images_in_page += 1
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
                    if images_in_page == 0:
                        print("No new image found on page %s going to next category" % (str(page)))
                        end_of_category = True
                        break
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

    print("%d images downloaded to category %s" % (counter, car_type))
