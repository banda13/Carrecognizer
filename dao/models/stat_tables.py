from sqlalchemy import Column, Integer, String, DateTime

from dao.base import Connection


class ScoutStat(Connection.Base):
    __tablename__ = 'scout_statistics'

    model = Column(String)
    make = Column(String)
    country = Column(String(10))
    start_date = Column(DateTime)
    run_time = Column(Integer) # in seconds
    cars = Column(Integer)
    images = Column(Integer)
    errors = Column(Integer)


def init():
    print('Stat tables initialized')
    return ScoutStat()