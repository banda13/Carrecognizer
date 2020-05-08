import requests
from bs4 import BeautifulSoup

main_page_content = ""
with open("input.txt", "r") as file:
    main_page_content = file.read()
parsed_main_page_content = BeautifulSoup(main_page_content)
makes_container = parsed_main_page_content.find("ul", {"class" : "search-filters__flyout__list search-filters__flyout__list--three-column"})

for cat in makes_container.find_all("span", {"class": "search-filters__flyout__list__option__name"}):
    print(cat.text)

temp = requests.get("https://www.parkers.co.uk/abarth/for-sale/").text
print(temp)