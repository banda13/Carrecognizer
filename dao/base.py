import datetime

from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.class_utils import Singleton


class Connection(metaclass=Singleton):
    username = 'cr_admin'
    password = 'earlengine'
    db_name = 'car_recognizer'
    Base = declarative_base()

    def __init__(self):
        self.engine = create_engine('postgresql://%s:%s@localhost:5432/%s' % (self.username, self.password, self.db_name))
        self.Session = sessionmaker(bind=self.engine)

        # these define the order of the creation, please don't change it!
        import dao.models.base_tables, dao.models.scout_tables
        dao.models.base_tables.init()
        dao.models.scout_tables.init()
        print('DB connection initialized')

    def drop_and_create(self):
        self.drop_db()
        self.create_db()

    def drop_db(self):
        self.Base.metadata.drop_all(self.engine)
        print("DB dropped")

    def create_db(self):
        self.Base.metadata.create_all(self.engine)
        print("DB created")

    def open_session(self):
        print("Opening new session")
        return self.Session()


connection = Connection()
