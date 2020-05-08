import requests
from bs4 import BeautifulSoup

base_url = "https://market.kz/rabota/"
advert_pattern = 'href="https://market.kz/a/advert-'

main_page = requests.get(base_url)
main_page_text = main_page.text

processed_id = []

for word in main_page_text.split():
    if word.startswith(advert_pattern):
        advert_page = word.replace('href="', "").split('"', 1)[0]
        page_id = word.replace(advert_pattern, '')[:-2]
        if page_id in processed_id:
            continue

        processed_id.append(page_id)
        print("Get for " + advert_page)
        advert_page_text = requests.get(advert_page).text
        parsed_html = BeautifulSoup(advert_page_text, 'html.parser')

        salary_container = parsed_html.find('div', 'misc-fields field-price')
        salaries = salary_container.findChildren('dd')
        print("salary: " + salaries[0].get_text().strip())