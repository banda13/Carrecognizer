import os
import urllib.request
from random import uniform, randint
from time import sleep
import requests

import paths
from input.proxy_config import get_random_proxy

'''AFTER A FEW 1000 IMAGE I GOT BANNED... Xd'''

base_url = "https://www.autovit.ro/autoturisme/"
root_dir = paths.VIT_DIR
categories = os.listdir(paths.HASZNALT_DIR)


def maybe_change_proxy(proxy, proxyhandler):
    if randint(0, 100) < 2:
        p = get_random_proxy(base_url)
        ph = urllib.request.ProxyHandler(proxy)
        opener = urllib.request.build_opener(proxyhandler)
        urllib.request.install_opener(opener)
        return p, ph
    return proxy, proxyhandler


sub_dir_pattern = 'href="https://www.autovit.ro/anunt/'
image_pattern = 'src="https://apollo-ireland.akamaized.net/v1/files/'
result_list_pattern = 'href="https://www.autovit.ro/autoturisme/'

proxy = get_random_proxy(base_url)
proxyhandler = urllib.request.ProxyHandler(proxy)

for car_type in categories:

    path = root_dir + car_type
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        print("Path already exits, skipped: " + path)
        continue
    print("Downloading images : ", car_type)

    proxy, proxyhandler = maybe_change_proxy(proxy, proxyhandler)

    resp = requests.get(base_url + car_type, proxies = proxy)
    counter = 0
    sleep(round(uniform(0.5, 0.9), 4))

    has_more_page = True
    page = 1
    page_txt = resp.text
    while has_more_page:
        try:
            print("%d image loaded to: %s !Loading images from next page: %d" % (counter, car_type, page))

            proxy, proxyhandler = maybe_change_proxy(proxy, proxyhandler)
            sub_pages = []
            images_in_page = 0
            for word in page_txt.split():
                if word.startswith(sub_dir_pattern):
                    try:
                        url = word.replace('href="', "").split('"', 1)[0]
                        if url in sub_pages:
                            continue

                        r2 = requests.get(url, proxies = proxy)
                        sleep(round(uniform(0.1, 0.4), 4))

                        inner_body = r2.text
                        car_image_counter = 0
                        images_in_subpage = []
                        for word2 in inner_body.split():
                            if word2.startswith(image_pattern):
                                try:
                                    img_url = word2.replace('src="', "").split('"', 1)[0]
                                    if img_url in images_in_subpage:
                                        continue

                                    file_name = root_dir + car_type + "/" + car_type + "_" + str(counter) + ".jpg"
                                    img = urllib.request.urlretrieve(img_url, file_name)
                                    sleep(round(uniform(0.2, 0.6), 4))

                                    counter += 1
                                    car_image_counter += 1

                                    images_in_subpage.append(img_url)

                                    # TODO dont need this limit more due to clever preprocessing
                                    # if car_image_counter > 3:
                                    #    break
                                except Exception as e:
                                    print("%s error while downloading image: %s" % (str(e), word2))
                        sub_pages.append(url)
                        # if len(sub_pages) > 3:
                        #    print("Debug mod, downloading from page %d ended" % page)
                        #    break
                    except Exception as e:
                        print("%s error while loading from page: %s. " % (str(e), word))
            page += 1
            end_of_category = True
            for word in page_txt.split():
                if word.startswith(result_list_pattern) and word.__contains__("?page=" + str(page)):
                    new_url = word.replace('href="', "").split('"', 1)[0]
                    proxy, proxyhandler = maybe_change_proxy(proxy, proxyhandler)
                    new_page = requests.get(new_url, proxies=proxy)
                    page_txt = new_page.text
                    end_of_category = False
                    sleep(round(uniform(0.1, 0.5), 4))
                    break

            has_more_page = (not end_of_category)
        except Exception as e:
            proxy, proxyhandler = maybe_change_proxy(proxy, proxyhandler)
            print("Failed to load more image from category: %s. %d image downloaded. Error: %s" % (
                car_type, counter, str(e)))

