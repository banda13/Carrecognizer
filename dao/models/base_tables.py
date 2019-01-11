import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from dao.base import Connection


class Model(Connection.Base):
    __tablename__ = 'model'

    model_id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String, nullable=False)
    makes = relationship("Make")

    def __init__(self, model_name):
        self.name = model_name


class Make(Connection.Base):
    __tablename__ = 'make'

    make_id = Column(Integer, primary_key=True)
    create_date = Column(DateTime, default=datetime.datetime.utcnow)
    name = Column(String, nullable=False)
    model_id = Column(Integer, ForeignKey('model.model_id'))

    def __init__(self, make_name):
        self.name = make_name


def init():
    print('Base tables initialized')
    return Model('-'), Make('-')
