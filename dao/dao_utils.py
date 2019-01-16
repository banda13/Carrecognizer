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



