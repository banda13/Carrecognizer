from bs4 import BeautifulSoup

scout_car_fields_map = [
    {
        "en_pattern": ">Make<",
        "hu_pattern": ">Márka<",
        "field_name": "make"
    },

    {

    }
]



def read_file(file_name):
    text_file = None
    car_properties = {}
    with open(file_name, "rb") as fp:
        text_file = fp.read()
    if text_file is None:
        raise Exception('Could not read file %s ' % file_name)

    print("Text file read, processing started")
    parsed_html = BeautifulSoup(text_file, 'html.parser')#.encode("utf-8")
    print("Html parsed")

    try:
        price_container = parsed_html.find('div', 'cldt-price')
        price_value = price_container.find('h2').get_text().split()
        car_properties['price'] = float(price_value[1][:-2])
        car_properties['currency'] = price_value[0]
    except Exception as e:
        print("Skipping price: %s" % e)

    try:
        basic_data_container = parsed_html.find('div', 'cldt-stage-basic')
        if basic_data_container is not None:
            if basic_data_container.children is not None:
                basic_datas = list(basic_data_container.childer)
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
                    title = prop_title.get_text().strip()
                    value = prop_value.get_text().strip()
                    car_properties[title] = value
    except Exception as e:
        print("Skipping main properties:")

    equipment_container = parsed_html.find_all('div', class_='cldt-equipment-block')
    for equipment_block in equipment_container:
        title_html = equipment_block.find('h3')
        if title_html is not None:
            title = title_html.get_text().strip()
            equipment_values = []
            for equipment in equipment_block.find_all('span'):
                eq = equipment.get_text()
                if eq is not None:
                    equipment_values.append(equipment.get_text().strip())
            car_properties[title] = equipment_values

    print('Car processed')


read_file(r'C:\Users\Szabó András\Desktop\Használt Audi TT kupé itt_ Taranto ehhez_ € 1.549,-.html')



