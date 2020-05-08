import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from dao.base import Connection


class Make(Connection.Base):
    __tablename__ = 'make'

    make_id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, nullable=False)
    models = relationship("Model")

    def __init__(self, model_name):
        self.name = model_name

    def set_make(self, make_id, name):
        self.make_id = make_id
        self.name = name


class Model(Connection.Base):
    __tablename__ = 'model'

    model_id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, nullable=False)
    make_id = Column(Integer, ForeignKey('make.make_id'))

    def __init__(self, make_name):
        self.name = make_name

    def set_model(self, model_id, name, make_id):
        self.make_id = make_id
        self.name = name
        self.model_id = model_id


def init():
    print('Base tables initialized')
    return Make('-'), Model('-')
