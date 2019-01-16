import datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from dao.base import Connection


class Model(Connection.Base):
    __tablename__ = 'model'

    model_id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, nullable=False)
    makes = relationship("Make")

    def __init__(self, model_name):
        self.name = model_name

    def set_model(self, model_id, name):
        self.model_id = model_id
        self.name = name


class Make(Connection.Base):
    __tablename__ = 'make'

    make_id = Column(Integer, primary_key=True)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())
    name = Column(String, nullable=False)
    model_id = Column(Integer, ForeignKey('model.model_id'))

    def __init__(self, make_name):
        self.name = make_name

    def set_make(self, make_id, name, model_id):
        self.make_id = make_id
        self.name = name
        self.model_id = model_id


def init():
    print('Base tables initialized')
    return Model('-'), Make('-')
