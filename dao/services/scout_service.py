from dao.base import connection
from dao.models.base_tables import Model, Make


def makemodel_lookup_for_id(model_v, make_v):
    s = connection.open_session()
    model_id, make_id = s.query(Model.model_id, Make.make_id)\
        .filter(Model.model_id == Make.model_id)\
        .filter(Model.name == model_v)\
        .filter(Make.name == make_v).one()
    return model_id, make_id