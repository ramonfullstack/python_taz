from datetime import datetime
from decimal import Decimal
from uuid import UUID

from bson import ObjectId


def custom_json_encoder(obj):
    if isinstance(obj, Decimal):
        return '{0:.2f}'.format(obj)
    elif isinstance(obj, UUID):
        return str(obj)
    elif isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, ObjectId):
        return str(obj)
    raise TypeError('{} is not JSON serializable'.format(repr(obj)))
