import csv
import random
import requests

proxies_csv = "../proxies.csv"

def get_random_proxy():
    proxies = []
    with open(proxies_csv, encoding='utf8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            proxies.append({'ip': row['ip'], 'port': row['port']})
    proxy = random.choice(proxies)
    http_proxy = "http://" + proxy['ip'] + ":" + proxy['port']
    https_proxy = "https://" + proxy['ip'] + ":" + proxy['port']
    ftp_proxy = "ftp://" + proxy['ip'] + ":" + proxy['port']

    print("using http proxy: ", http_proxy)

    return {
        "http": http_proxy,
        "https": https_proxy,
        "ftp": ftp_proxy
    }

def test_proxy():
    resp = requests.get("https://index.hu", proxies=get_random_proxy())
    print(resp.text)

test_proxy()