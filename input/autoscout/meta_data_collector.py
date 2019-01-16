import re
import datetime
from pathlib import Path

from sqlalchemy import select, String, Integer
from sqlalchemy.sql.elements import and_

from dao.base import connection
from dao.dao_utils import load_basic_tables
from dao.models.scout_tables import ScoutCar

from bs4 import BeautifulSoup
from dao.services.scout_service import makemodel_lookup_for_id

connection.drop_and_create()
load_basic_tables()
session = connection.open_session()


def read_file(file_name):
    text_file = None
    with open(file_name, "rb") as fp:
        text_file = fp.read()
    if text_file is None:
        raise Exception('Could not read file %s ' % file_name)

    print("Text file read, parsing started")
    parsed_html = BeautifulSoup(text_file, 'html.parser')#.encode("utf-8")
    print("Html parsed, processing started")

    model, make, id = Path(file_name).stem.split('_')
    id=157
    model_id, make_id = makemodel_lookup_for_id(model, make)
    tags = parsed_html.find_all(lambda tag: tag.has_attr('data-classified-guid'))
    scout_id = tags[0].attrs.get("data-classified-guid")
    country = parsed_html.find("html").attrs.get("lang")
    car = ScoutCar(id, scout_id, model_id, make_id, model, make, country)

    try:
        price_container = parsed_html.find('div', 'cldt-price')
        price_value = price_container.find('h2').get_text().split()
        car.price = int(re.sub('[^0-9]','', price_value[1]))
        car.currency = price_value[0]
    except Exception as e:
        print("Skipping price: %s" % e)

    try:
        basic_data_container = parsed_html.find('div', 'cldt-stage-basic-data')
        if basic_data_container is not None:
            if basic_data_container.children is not None:
                basic_datas = list(basic_data_container.findChildren("div"))
                try:
                    car.km = int(re.sub('[^0-9]','', basic_datas[0].find('span', 'sc-font-l cldt-stage-primary-keyfact').get_text()))
                except Exception as e:
                    print('Failed to get basic data: %s' % e)

                try:
                    car.first_registration = datetime.datetime.strptime(basic_datas[1].find('span', 'sc-font-l cldt-stage-primary-keyfact').get_text().strip(), "%m/%Y")
                except Exception as e:
                    print('Failed to get basic data: %s' % e)

                try:
                    car.power_kw = int(re.sub('[^0-9]','', basic_datas[2].find('span', 'sc-font-l cldt-stage-primary-keyfact').get_text()))
                except Exception as e:
                    print('Failed to get basic data: %s' % e)

                try:
                    car.power_hp = int(re.sub('[^0-9]','', basic_datas[2].find('span', 'sc-font-m cldt-stage-primary-keyfact').get_text()))
                except Exception as e:
                    print('Failed to get basic data: %s' % e)
    except Exception as e:
        print("Skipping basic data: %s" % e)

    try:
        main_properties_container = parsed_html.find_all('dl')
        for main_property_container in main_properties_container:
            sub_properties_titles = main_property_container.find_all('dt')
            sub_properties_values = main_property_container.find_all('dd')
            prop_main_title = main_property_container.find_previous_sibling('h3')
            for prop_title, prop_value in zip(sub_properties_titles, sub_properties_values):
                if prop_title is not None and prop_value is not None:
                    try:
                        title = prop_title.get_text().strip()
                        value = prop_value.get_text().strip()
                        setattr(car, car.attribute_lookup(title), value)
                    except Exception as e:
                        print("Property %s not set: %s" % (prop_title.get_text(),e))
    except Exception as e:
        print("Skipping main properties: %s" % e)

    try:
        equipment_container = parsed_html.find_all('div', class_='cldt-equipment-block')
        for equipment_block in equipment_container:
            try:
                title_html = equipment_block.find('h3')
                if title_html is not None:
                    title = title_html.get_text().strip()
                    equipment_values = []
                    for equipment in equipment_block.find_all('span'):
                        eq = equipment.get_text()
                        if eq is not None:
                            equipment_values.append(equipment.get_text().strip())
                    setattr(car, car.attribute_lookup(title), equipment_values)
            except Exception as e:
                print("Skipping equipment block: %s" % e)
    except Exception as e:
        print("Skipping equipment properties: %s" % e)

    print('Html processing done')
    session.add(car)
    session.commit()
    session.close()

read_file(r'C:\Users\Andy\Desktop\Audi_90_145.html')
