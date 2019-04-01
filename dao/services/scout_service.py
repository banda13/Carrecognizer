from dao.base import connection
from dao.models.base_tables import Make, Model


def makemodel_lookup_for_id(make_v, model_v):
    s = connection.open_session()
    model_id, make_id = s.query(Make.make_id, Model.model_id)\
        .filter(Make.make_id == Model.make_id)\
        .filter(Make.name == make_v)\
        .filter(Model.name == model_v).one()
    return make_id, model_id