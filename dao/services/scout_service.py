from sqlalchemy import and_, text

from dao.base import connection
from dao.models.base_tables import Make, Model
from dao.models.scout_tables import ScoutCar


def makemodel_lookup_for_id(make_v, model_v):
    s = connection.open_session()
    model_id, make_id = s.query(Make.make_id, Model.model_id)\
        .filter(Make.make_id == Model.make_id)\
        .filter(Make.name == make_v)\
        .filter(Model.name == model_v).one()
    s.close()
    return make_id, model_id


def lookup_for_id(id):
    s = connection.open_session()
    r = s.query(ScoutCar).get(id)
    s.close()
    return r


def lookup_property_distinct_values(property_name):
    s = connection.open_session()
    o = getattr(ScoutCar, property_name)
    values = s.query(o).distinct().all()
    s.close()
    return values


def query_for_property_value(property_name, property_value):
    s = connection.open_session()
    results = s.query(ScoutCar).filter(property_name + "= '" + str(property_value) + "'").all() # this can be very big
    s.close()
    return results


def query_for_properties_values(property_dict):
    s = connection.open_session()
    q = s.query(ScoutCar)
    cond = and_(*[p['name'] + " " + p['operation'] + " {}".format(p['value']) for p in property_dict])
    q = q.filter(cond)
    results = q.all()
    s.close()
    return results


def execute_sql(sql):
    sql = text(sql)
    s = connection.open_session()
    result = s.execute(sql).fetchall()
    s.close()
    return result