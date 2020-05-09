import datetime
import json
import dateutil.parser as dp
from enum import Enum
from keras import Sequential
from keras.engine.saving import model_from_json
from numpy import float32

from classifiers.cnn8 import Cnn8
from preprocess.clever_loader import LoaderFilter, PreClassificationState
import dateutil.parser as dp

PUBLIC_ENUMS = {
    'LoaderFilter': LoaderFilter,
    'PreClassificationState': PreClassificationState
}

class Encoder(json.JSONEncoder):
    def default(self, obj):
        if obj is not None:
            if isinstance(obj, Cnn8):
                return
            if isinstance(obj, Enum):
                return {"__enum__": str(obj)}
            if isinstance(obj, float32):
                return {"__float__": str(obj)}
            if isinstance(obj, Sequential):
                return {"__sequential__": obj.to_json()}
            if isinstance(obj, datetime.datetime):
                return {'__isoformat__': obj.isoformat()}
        return json.JSONEncoder.default(self, obj)


def decoder_hook(d):
    if d.get('__enum__'):
        name, member = d["__enum__"].split(".")
        return getattr(PUBLIC_ENUMS[name], member)
    if d.get('__sequential__'):
        return model_from_json(d["__sequential__"])
    if d.get('__sequential__'):
        return dp.parse(d.get('__isoformat__'))
    else:
        return d
