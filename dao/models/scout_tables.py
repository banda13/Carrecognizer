import re
import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Enum, Float, Text, Time, ARRAY, ForeignKey, JSON
from sqlalchemy.orm import validates

from dao.base import Connection
from dao.dao_utils import MColumn


class ScoutCar(Connection.Base):
    __tablename__ = 'scout_car'

    id = MColumn(Integer, "id", "id", primary_key=True)
    model_id = Column(Integer, ForeignKey('model.model_id'))
    make_id = Column(Integer, ForeignKey('make.make_id'))
    model = MColumn(String, "Model", "Modell", nullable=False)
    make = MColumn(String, "Make", "Márka", nullable=False)
    country = MColumn(String(5), "Country", "Ország", nullable=False)
    scout_id = MColumn(String, "Scout_id", "Scout_id")
    create_date = MColumn(DateTime, "Create_date", "Létrehozás időpontja", nullable=False,
                               default=datetime.datetime.utcnow)

    # base properties
    makemodel = MColumn(String, "MakeModel", "ModellMárka")
    version = MColumn(String, "Version", "Verzió")
    price = MColumn(Float, "Price", "Ár")
    currency = MColumn(String, "Currency", "Pénznem")
    km = MColumn(Integer, "Km", "Km")
    first_registration = MColumn(String, "FirstRegistration", "Első forgalomba helyezés")
    power_kw = MColumn(Integer, "Kilo Watt", "Kiló Watt")
    power_hp = MColumn(Integer, "Horse Power", "Ló erő")
    highlight_properties = MColumn(ARRAY(String), "Highlights", "Highlights")

    # main properties
    type = MColumn(String, "Type", "Állapot")
    body_color = MColumn(String, "Body Color", "Külső szín")
    paint_type = MColumn(String, "Paint Type", "Fényezés")
    body = MColumn(String, "Body", "A karosszéria formája")
    doors = MColumn(Integer, "Nr. of Doors", "Ajtók száma")
    seats = MColumn(Integer, "Nr. of Seats", "Ülőhelyek száma")

    gear_type = MColumn(String, "Gearing Type", "Váltó típusa")
    gears = MColumn(Integer, "Gears", "Sebességfokozatok száma")
    displacement = MColumn(Integer, "Displacement", "Hengerűrtartalom")
    cylinders = MColumn(Integer, "Cylinders", "Hengerek száma")
    weight = MColumn(Integer, "Weight", "Tömege üres állapotban")

    fuel = MColumn(String(20), "Fuel", "Üzemanyag")
    consumption_comb = MColumn(Integer, "Consumption Comb", "Üzemanyagfogyasztás kombinált")
    consumption_city = MColumn(Integer, "Consumption City", "Üzemanyagfogyasztás városi")
    consumption_country = MColumn(Integer, "Consumption Country", "Üzemanyagfogyasztás országúti")
    emission = MColumn(String, "Emission Class", "Károsanyag-kibocsátási kategória")

    # equipment
    comfort_convenience = MColumn(ARRAY(String), "Comfort & Convenience", "Kényelem")
    entertainment_media = MColumn(ARRAY(String), "Entertainment & Media", "Szórakozás / Média")
    extras = MColumn(ARRAY(String), "Extras", "Extrák")
    safety_security = MColumn(ARRAY(String), "Safety & Security", "Biztonság")

    def __init__(self, mid, scout_id, model_id, make_id, model, make, country):
        self.id = mid
        self.scout_id = scout_id
        self.model_id = model_id
        self.make_id = make_id
        self.model = model
        self.make = make
        self.country = country

    def attribute_lookup(self, name):
        for attr in dir(ScoutCar):
            if not attr.startswith('__'):
                try:
                    field = getattr(ScoutCar, attr)
                    if field.en_pattern == name or field.hu_pattern == name:
                        return attr
                except Exception as e:
                    pass

    # validators used as converters because i did not find any other solution to add setter and this way is clean
    @validates('displacement')
    def validate_displacement(self, title, displacement):
        try:
            return int(re.sub('[^0-9]','', displacement))
        except Exception:
            return 0

    @validates('weight')
    def validate_weight(self, title, weight):
        try:
            return int(re.sub('[^0-9]', '', weight))
        except Exception:
            return 0

def init():
    print('Scout tables initialized')
    return ScoutCar(0, '-', 0, 0, '-', '-', '-')
