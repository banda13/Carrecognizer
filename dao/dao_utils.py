import csv

from sqlalchemy import Column

import paths



class MColumn(Column):

    def __init__(self, type, en_pattern, hu_pattern, primary_key=False, nullable=True, default=None):
        self.en_pattern = en_pattern
        self.hu_pattern = hu_pattern
        self.type = type
        if default is not None:
            super(MColumn, self).__init__(type, primary_key=primary_key, nullable=nullable, default=default)
        else:
            super(MColumn, self).__init__(type, primary_key=primary_key, nullable=nullable)


def rebuild_db():
    from dao.base import connection
    connection.drop_and_create()


def load_basic_tables():
    from dao.base import connection
    from dao.models.base_tables import Model, Make

    session = connection.open_session()
    model_data_filename = paths.ROOT_DIR + '/model_backup.csv'
    make_data_filename = paths.ROOT_DIR + '/make_backup.csv'

    with open(model_data_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            m = Model(row['model'])
            m.model_id = row['model_id']
            session.add(m)
    session.commit()
    print("Model table data loaded")

    with open(make_data_filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            m = Make(row['make'])
            m.set_make(row['make_id'], row['make'], row['model_id'])
            session.add(m)
    session.commit()
    print("Make table data loaded")
    session.close()
