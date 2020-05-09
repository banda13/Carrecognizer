from bs4 import BeautifulSoup
import requests

main_page = 'https://www.cars.com/'

# phase 1 collect meta data and ids for webcrawing

main_page_raw = requests.get(main_page).text
main_page = BeautifulSoup(main_page_raw, 'html.parser')

stockType_select = main_page.find("select", {"name": "stockType"})
stockTypes = [(o['value'], o.text) for o in stockType_select.find_all('option')]
print('Stock types: {}'.format(stockTypes))

make_select = main_page.find("select", {"name": "makeId"})
makeTypes = [(o['value'], o.text) for o in make_select.find_all('option')]
print('Makes: {}'.format(makeTypes))

model_select = main_page.find("select", {"name": "modelId"})
modelTypes = [(o['value'], o.text) for o in model_select.find_all('option')]
print('Models: {}'.format(modelTypes))