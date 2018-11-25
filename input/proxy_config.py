import csv
import random
import requests

import paths

proxies_csv = paths.ROOT_DIR + "/input/proxies.csv"


def get_random_proxy(url):
    proxies = []
    with open(proxies_csv, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proxies.append({'ip': row['ip'], 'port': row['port']})
    proxy = get_proxy(proxies)
    while not test_proxy(url, proxy):
        print("%s proxy failed, getting new one..")
        proxy = get_proxy(proxies)
    print("using http proxy: ", proxy)
    return proxy


def get_proxy(proxies):
    proxy = random.choice(proxies)
    http_proxy = "http://" + proxy['ip'] + ":" + proxy['port']
    https_proxy = "https://" + proxy['ip'] + ":" + proxy['port']
    ftp_proxy = "ftp://" + proxy['ip'] + ":" + proxy['port']

    proxy = {
        "http": http_proxy,
        "https": https_proxy,
        "ftp": ftp_proxy
    }
    return proxy


def test_proxy(url, proxie):
    try:
        resp = requests.get(url, proxies=proxie)
        if resp.status_code == 200:
            return True
        else:
            print("Bad proxy : %s" % resp.text)
            return False
    except Exception as e:
        print(e)
        return False

