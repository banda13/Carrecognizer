import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, Boolean, Enum, Float, Text, Time

from dao.base import Connection


class ScoutCar(Connection.Base):
    __tablename__ = 'scout_car'

    id = Column(Integer, primary_key=True)
    model = Column(String, nullable=False)
    make = Column(String, nullable=False)
    country = Column(String(5), nullable=False)
    scout_id = Column(String)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)

    # basic properties
    full_name = Column(String)
    body = Column(String) #karosszéria formája
    color = Column(String)
    doors = Column(Integer)
    seats = Column(Integer)

    # drive
    gear_type = Column(String(20)) # váltó
    gears = Column(Integer) # sebességfokozatok száma
    #etc..

    def __init__(self, scout_id):
        self.scout_id = scout_id

def init():
    print('Scout tables initialized')
    return ScoutCar('-')